from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Dict, Any
import numpy as np
import cv2
import io
import logging
from app import models, schemas
from app.database import get_db
# Try to import core components, but make them optional
try:
    from app.core.fall_detection.hybrid_detector import HybridFallDetector
    FALL_DETECTION_AVAILABLE = True
except Exception as e:
    logger.warning(f"Fall detection not available: {e}")
    FALL_DETECTION_AVAILABLE = False
    HybridFallDetector = None

try:
    from app.core.alert_system import AlertSystem
    ALERT_SYSTEM_AVAILABLE = True
except Exception as e:
    logger.warning(f"Alert system not available: {e}")
    ALERT_SYSTEM_AVAILABLE = False
    AlertSystem = None

try:
    from app.core.emergency_network import EmergencyNetwork
    EMERGENCY_NETWORK_AVAILABLE = True
except Exception as e:
    logger.warning(f"Emergency network not available: {e}")
    EMERGENCY_NETWORK_AVAILABLE = False
    EmergencyNetwork = None

try:
    from app.core.ai_assistant import AIAssistant
    AI_ASSISTANT_AVAILABLE = True
except Exception as e:
    logger.warning(f"AI assistant not available: {e}")
    AI_ASSISTANT_AVAILABLE = False
    AIAssistant = None

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize core components
fall_detector = HybridFallDetector() if FALL_DETECTION_AVAILABLE else None
alert_system = AlertSystem() if ALERT_SYSTEM_AVAILABLE else None
ai_assistant = AIAssistant() if AI_ASSISTANT_AVAILABLE else None

@router.post("/detect-video")
async def detect_fall_video(
    video_frame: UploadFile = File(...),
    user_id: int = Form(...),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Detect falls from uploaded video frames
    
    Args:
        video_frame: Uploaded video frame
        user_id: ID of the user
        db: Database session
        
    Returns:
        Detection results
    """
    if not FALL_DETECTION_AVAILABLE:
        raise HTTPException(status_code=501, detail="Fall detection system not available")
    
    try:
        # Read the uploaded frame
        contents = await video_frame.read()
        
        # Convert to numpy array
        nparr = np.frombuffer(contents, np.uint8)
        
        # Decode image
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            raise HTTPException(status_code=400, detail="Invalid image data")
        
        # Perform fall detection
        is_fall, confidence, details = fall_detector.detect_fall(video_frame=frame)
        
        result = {
            "is_fall_detected": is_fall,
            "confidence": confidence,
            "details": details
        }
        
        # If fall detected, trigger emergency response
        if is_fall:
            # Get user information
            user = db.query(models.user.User).filter(models.user.User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            # Get user location
            location = db.query(models.user.Location).filter(
                models.user.Location.user_id == user_id,
                models.user.Location.is_primary == True
            ).first()
            
            location_data = {
                "latitude": location.latitude if location else "Unknown",
                "longitude": location.longitude if location else "Unknown",
                "address": location.address if location else "Unknown location"
            }
            
            # Create alert
            alert = models.user.Alert(
                user_id=user_id,
                location_lat=location_data["latitude"],
                location_lng=location_data["longitude"],
                status="pending",
                alert_type="fall_detected",
                notes=f"Fall detected with confidence {confidence:.2f}"
            )
            db.add(alert)
            db.commit()
            
            # Prepare alert data
            alert_data = {
                "user_name": user.full_name,
                "user_id": user_id,
                "timestamp": alert.timestamp.isoformat() if alert.timestamp else "Unknown",
                "location": location_data["address"],
                "status": "Fall detected",
                "confidence": confidence
            }
            
            # Notify emergency network
            if EMERGENCY_NETWORK_AVAILABLE:
                emergency_network = EmergencyNetwork(db)
                emergency_team = emergency_network.create_emergency_response_team(
                    user_id, 
                    float(location_data["latitude"]) if location_data["latitude"] != "Unknown" else 0.0,
                    float(location_data["longitude"]) if location_data["longitude"] != "Unknown" else 0.0
                )
                
                # Send alerts to caregivers
                notification_result = emergency_network.notify_emergency_contacts(user_id, alert_data)
                
                result["emergency_team"] = emergency_team
                result["notifications_sent"] = notification_result
            
            # Send multi-channel alerts (in a real implementation, this would be async)
            # recipients = {
            #     "sms": [user.phone_number],
            #     "email": [user.email]
            # }
            # if ALERT_SYSTEM_AVAILABLE:
            #     await alert_system.send_multi_channel_alert(recipients, alert_data)
            
            result["alert_triggered"] = True
            
            # Provide AI assistance
            if AI_ASSISTANT_AVAILABLE:
                ai_assistant.emergency_guidance_protocol()
            
        return result
        
    except Exception as e:
        logger.error(f"Error in video fall detection: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/detect-audio")
async def detect_fall_audio(
    audio_file: UploadFile = File(...),
    user_id: int = Form(...),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Detect falls from uploaded audio files
    
    Args:
        audio_file: Uploaded audio file
        user_id: ID of the user
        db: Database session
        
    Returns:
        Detection results
    """
    try:
        # In a real implementation, we would:
        # 1. Process the audio file
        # 2. Extract features
        # 3. Run through the audio detector
        # 4. Trigger appropriate responses if fall detected
        
        result = {
            "is_fall_detected": False,
            "confidence": 0.0,
            "message": "Audio detection not fully implemented in this demo",
            "user_id": user_id
        }
        
        return result
        
    except Exception as e:
        logger.error(f"Error in audio fall detection: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/trigger-manual-alert")
async def trigger_manual_alert(
    user_id: int = Form(...),
    notes: str = Form(None),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Trigger a manual alert from the user
    
    Args:
        user_id: ID of the user
        notes: Optional notes from the user
        db: Database session
        
    Returns:
        Alert creation result
    """
    try:
        # Get user information
        user = db.query(models.user.User).filter(models.user.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get user location
        location = db.query(models.user.Location).filter(
            models.user.Location.user_id == user_id,
            models.user.Location.is_primary == True
        ).first()
        
        # Create alert
        alert = models.user.Alert(
            user_id=user_id,
            location_lat=location.latitude if location else "Unknown",
            location_lng=location.longitude if location else "Unknown",
            status="pending",
            alert_type="manual_trigger",
            notes=notes or "Manual alert triggered by user"
        )
        db.add(alert)
        db.commit()
        
        # Prepare alert data
        alert_data = {
            "user_name": user.full_name,
            "user_id": user_id,
            "timestamp": alert.timestamp.isoformat() if alert.timestamp else "Unknown",
            "location": location.address if location else "Unknown location",
            "status": "Manual alert triggered",
            "notes": notes
        }
        
        # Notify emergency network
        notification_result = {}
        if EMERGENCY_NETWORK_AVAILABLE:
            emergency_network = EmergencyNetwork(db)
            notification_result = emergency_network.notify_emergency_contacts(user_id, alert_data)
        
        # Send multi-channel alerts
        # recipients = {
        #     "sms": [user.phone_number],
        #     "email": [user.email]
        # }
        # if ALERT_SYSTEM_AVAILABLE:
        #     await alert_system.send_multi_channel_alert(recipients, alert_data)
        
        return {
            "success": True,
            "alert_id": alert.id,
            "message": "Manual alert triggered successfully",
            "notifications_sent": notification_result
        }
        
    except Exception as e:
        logger.error(f"Error triggering manual alert: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{user_id}")
async def get_detection_status(user_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Get current detection status for a user
    
    Args:
        user_id: ID of the user
        db: Database session
        
    Returns:
        Status information
    """
    try:
        # Get recent alerts for the user
        recent_alerts = db.query(models.user.Alert).filter(
            models.user.Alert.user_id == user_id
        ).order_by(models.user.Alert.timestamp.desc()).limit(5).all()
        
        # Get user information
        user = db.query(models.user.User).filter(models.user.User.id == user_id).first()
        
        return {
            "user_id": user_id,
            "user_name": user.full_name if user else "Unknown",
            "active_alerts": len([a for a in recent_alerts if a.status == "pending"]),
            "recent_alerts": [
                {
                    "id": alert.id,
                    "timestamp": alert.timestamp.isoformat() if alert.timestamp else None,
                    "type": alert.alert_type,
                    "status": alert.status,
                    "notes": alert.notes
                }
                for alert in recent_alerts
            ],
            "system_status": "operational"
        }
        
    except Exception as e:
        logger.error(f"Error getting detection status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))