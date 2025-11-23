import math
from typing import List, Dict, Tuple, Optional
from app import models, schemas
from sqlalchemy.orm import Session
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmergencyNetwork:
    def __init__(self, db_session: Session):
        """
        Initialize the Emergency Network with database session
        
        Args:
            db_session: SQLAlchemy database session
        """
        self.db = db_session
        logger.info("EmergencyNetwork initialized")

    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate the great circle distance between two points on the earth
        using the Haversine formula
        
        Args:
            lat1, lon1: Latitude and longitude of point 1 (in decimal degrees)
            lat2, lon2: Latitude and longitude of point 2 (in decimal degrees)
            
        Returns:
            Distance in kilometers
        """
        # Convert decimal degrees to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Radius of earth in kilometers
        r = 6371
        
        return c * r

    def find_nearest_volunteers(self, user_lat: float, user_lon: float, 
                              max_distance_km: float = 2.0, 
                              max_volunteers: int = 5) -> List[Dict]:
        """
        Find nearest volunteers within specified distance
        
        Args:
            user_lat: User's latitude
            user_lon: User's longitude
            max_distance_km: Maximum distance to search (in kilometers)
            max_volunteers: Maximum number of volunteers to return
            
        Returns:
            List of nearest volunteers with distance information
        """
        try:
            # Query all volunteers
            volunteers = self.db.query(models.user.User).filter(
                models.user.User.role == "volunteer",
                models.user.User.is_active == True
            ).all()
            
            # Calculate distances and filter by proximity
            nearby_volunteers = []
            
            for volunteer in volunteers:
                # Get volunteer's primary location
                primary_location = self.db.query(models.user.Location).filter(
                    models.user.Location.user_id == volunteer.id,
                    models.user.Location.is_primary == True
                ).first()
                
                if primary_location:
                    try:
                        vol_lat = float(primary_location.latitude)
                        vol_lon = float(primary_location.longitude)
                        
                        # Calculate distance
                        distance = self.calculate_distance(
                            user_lat, user_lon, vol_lat, vol_lon
                        )
                        
                        # Filter by maximum distance
                        if distance <= max_distance_km:
                            nearby_volunteers.append({
                                "volunteer_id": volunteer.id,
                                "name": volunteer.full_name,
                                "phone": volunteer.phone_number,
                                "distance_km": round(distance, 2),
                                "latitude": vol_lat,
                                "longitude": vol_lon
                            })
                    except ValueError:
                        # Skip volunteers with invalid location data
                        logger.warning(f"Invalid location data for volunteer {volunteer.id}")
                        continue
            
            # Sort by distance and limit results
            nearby_volunteers.sort(key=lambda x: x["distance_km"])
            return nearby_volunteers[:max_volunteers]
            
        except Exception as e:
            logger.error(f"Error finding nearest volunteers: {str(e)}")
            return []

    def find_available_doctors(self, specialty: str = "general", 
                              max_doctors: int = 3) -> List[Dict]:
        """
        Find available doctors (in real implementation, this would check availability)
        
        Args:
            specialty: Medical specialty required
            max_doctors: Maximum number of doctors to return
            
        Returns:
            List of available doctors
        """
        try:
            # Query all doctors
            doctors = self.db.query(models.user.User).filter(
                models.user.User.role == "doctor",
                models.user.User.is_active == True
            ).all()
            
            available_doctors = []
            
            for doctor in doctors:
                # In a real implementation, we would check:
                # - Doctor's schedule/availability
                # - Specialty match
                # - Current workload
                # - Location (for local doctors)
                
                available_doctors.append({
                    "doctor_id": doctor.id,
                    "name": doctor.full_name,
                    "phone": doctor.phone_number,
                    "email": doctor.email,
                    "specialty": specialty,  # Simplified for demo
                    "available": True  # Simplified for demo
                })
            
            return available_doctors[:max_doctors]
            
        except Exception as e:
            logger.error(f"Error finding available doctors: {str(e)}")
            return []

    def notify_emergency_contacts(self, user_id: int, alert_data: Dict) -> Dict:
        """
        Notify emergency contacts about an alert
        
        Args:
            user_id: ID of the user who triggered the alert
            alert_data: Dictionary containing alert information
            
        Returns:
            Dictionary with notification results
        """
        try:
            # Get user's caregivers
            caregivers = self.db.query(models.user.User).filter(
                models.user.User.role == "caregiver"
            ).all()
            
            # Get user's primary location
            user_location = self.db.query(models.user.Location).filter(
                models.user.Location.user_id == user_id,
                models.user.Location.is_primary == True
            ).first()
            
            location_str = "Unknown location"
            if user_location:
                location_str = user_location.address or f"{user_location.latitude}, {user_location.longitude}"
            
            # Prepare notification message
            message = (
                f"🚨 EMERGENCY ALERT 🚨\n"
                f"Fall detected for {alert_data.get('user_name', 'Unknown User')}\n"
                f"Time: {alert_data.get('timestamp', 'Unknown Time')}\n"
                f"Location: {location_str}\n"
                f"Status: {alert_data.get('status', 'Critical')}\n"
                f"Please check on them immediately!"
            )
            
            # Collect contact information
            sms_contacts = []
            email_contacts = []
            
            for caregiver in caregivers:
                if caregiver.phone_number:
                    sms_contacts.append(caregiver.phone_number)
                if caregiver.email:
                    email_contacts.append(caregiver.email)
            
            # In a real implementation, we would integrate with the AlertSystem
            # to send actual notifications
            
            logger.info(f"Notified {len(sms_contacts)} SMS contacts and {len(email_contacts)} email contacts")
            
            return {
                "success": True,
                "sms_contacts_notified": len(sms_contacts),
                "email_contacts_notified": len(email_contacts),
                "message": message
            }
            
        except Exception as e:
            logger.error(f"Error notifying emergency contacts: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    def create_emergency_response_team(self, user_id: int, 
                                     user_lat: float, user_lon: float) -> Dict:
        """
        Create an emergency response team consisting of nearest volunteers and doctors
        
        Args:
            user_id: ID of the user who needs assistance
            user_lat: User's latitude
            user_lon: User's longitude
            
        Returns:
            Dictionary with emergency response team information
        """
        try:
            # Find nearest volunteers
            nearest_volunteers = self.find_nearest_volunteers(user_lat, user_lon)
            
            # Find available doctors
            available_doctors = self.find_available_doctors()
            
            # Get user information
            user = self.db.query(models.user.User).filter(
                models.user.User.id == user_id
            ).first()
            
            response_team = {
                "user": {
                    "id": user.id if user else None,
                    "name": user.full_name if user else "Unknown",
                },
                "volunteers": nearest_volunteers,
                "doctors": available_doctors,
                "team_created": True
            }
            
            logger.info(f"Emergency response team created with {len(nearest_volunteers)} volunteers and {len(available_doctors)} doctors")
            
            return response_team
            
        except Exception as e:
            logger.error(f"Error creating emergency response team: {str(e)}")
            return {
                "user": {"id": user_id, "name": "Unknown"},
                "volunteers": [],
                "doctors": [],
                "team_created": False,
                "error": str(e)
            }

    def get_community_resources(self, user_lat: float, user_lon: float) -> Dict:
        """
        Get nearby community resources (hospitals, clinics, pharmacies)
        
        Args:
            user_lat: User's latitude
            user_lon: User's longitude
            
        Returns:
            Dictionary with nearby community resources
        """
        # In a real implementation, this would query external APIs or databases
        # for hospitals, clinics, pharmacies, etc.
        
        # Placeholder implementation with simulated data
        community_resources = {
            "nearest_hospital": {
                "name": "City General Hospital",
                "address": "123 Main Street",
                "phone": "+1-555-0123",
                "distance_km": 1.5,
                "estimated_time_minutes": 5
            },
            "nearest_clinic": {
                "name": "Downtown Medical Clinic",
                "address": "456 Oak Avenue",
                "phone": "+1-555-0456",
                "distance_km": 0.8,
                "estimated_time_minutes": 2
            },
            "nearest_pharmacy": {
                "name": "HealthPlus Pharmacy",
                "address": "789 Pine Road",
                "phone": "+1-555-0789",
                "distance_km": 0.3,
                "estimated_time_minutes": 1
            }
        }
        
        return community_resources

# Example usage
if __name__ == "__main__":
    # This would be used within the application context with a database session
    print("EmergencyNetwork ready for use")