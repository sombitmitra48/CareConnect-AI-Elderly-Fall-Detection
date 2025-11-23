from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import asyncio
import logging
from typing import Dict, List, Optional
import os
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AlertSystem:
    def __init__(self):
        """
        Initialize the AlertSystem with notification services
        """
        # Twilio configuration (would be loaded from environment variables)
        self.twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID", "")
        self.twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN", "")
        self.twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER", "")
        
        # Email configuration
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.email_username = os.getenv("EMAIL_USERNAME", "")
        self.email_password = os.getenv("EMAIL_PASSWORD", "")
        
        # WhatsApp configuration (using Twilio)
        self.whatsapp_enabled = os.getenv("WHATSAPP_ENABLED", "false").lower() == "true"
        
        logger.info("AlertSystem initialized")

    def send_sms_alert(self, phone_numbers: List[str], message: str) -> Dict[str, any]:
        """
        Send SMS alert to multiple phone numbers
        
        Args:
            phone_numbers: List of phone numbers to send alert to
            message: Alert message content
            
        Returns:
            Dictionary with success status and details
        """
        if not self.twilio_account_sid or not self.twilio_auth_token:
            logger.warning("Twilio credentials not configured")
            return {"success": False, "error": "Twilio not configured"}
            
        try:
            client = Client(self.twilio_account_sid, self.twilio_auth_token)
            results = []
            
            for phone_number in phone_numbers:
                try:
                    message_obj = client.messages.create(
                        body=message,
                        from_=self.twilio_phone_number,
                        to=phone_number
                    )
                    results.append({
                        "phone_number": phone_number,
                        "success": True,
                        "message_sid": message_obj.sid
                    })
                except Exception as e:
                    results.append({
                        "phone_number": phone_number,
                        "success": False,
                        "error": str(e)
                    })
            
            logger.info(f"SMS alerts sent to {len(phone_numbers)} recipients")
            return {"success": True, "results": results}
            
        except Exception as e:
            logger.error(f"Failed to send SMS alerts: {str(e)}")
            return {"success": False, "error": str(e)}

    def send_email_alert(self, email_addresses: List[str], subject: str, 
                        message: str, html_message: Optional[str] = None) -> Dict[str, any]:
        """
        Send email alert to multiple email addresses
        
        Args:
            email_addresses: List of email addresses to send alert to
            subject: Email subject
            message: Plain text message content
            html_message: HTML formatted message (optional)
            
        Returns:
            Dictionary with success status and details
        """
        if not self.email_username or not self.email_password:
            logger.warning("Email credentials not configured")
            return {"success": False, "error": "Email not configured"}
            
        try:
            results = []
            
            for email_address in email_addresses:
                try:
                    # Create message
                    msg = MIMEMultipart("alternative")
                    msg["Subject"] = subject
                    msg["From"] = self.email_username
                    msg["To"] = email_address
                    
                    # Add plain text part
                    part1 = MIMEText(message, "plain")
                    msg.attach(part1)
                    
                    # Add HTML part if provided
                    if html_message:
                        part2 = MIMEText(html_message, "html")
                        msg.attach(part2)
                    
                    # Send email
                    with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                        server.starttls()
                        server.login(self.email_username, self.email_password)
                        server.send_message(msg)
                        
                    results.append({
                        "email": email_address,
                        "success": True
                    })
                except Exception as e:
                    results.append({
                        "email": email_address,
                        "success": False,
                        "error": str(e)
                    })
            
            logger.info(f"Email alerts sent to {len(email_addresses)} recipients")
            return {"success": True, "results": results}
            
        except Exception as e:
            logger.error(f"Failed to send email alerts: {str(e)}")
            return {"success": False, "error": str(e)}

    def send_whatsapp_alert(self, phone_numbers: List[str], message: str) -> Dict[str, any]:
        """
        Send WhatsApp alert to multiple phone numbers
        
        Args:
            phone_numbers: List of phone numbers to send alert to (must be WhatsApp-enabled)
            message: Alert message content
            
        Returns:
            Dictionary with success status and details
        """
        if not self.whatsapp_enabled or not self.twilio_account_sid or not self.twilio_auth_token:
            logger.warning("WhatsApp not configured or disabled")
            return {"success": False, "error": "WhatsApp not configured"}
            
        try:
            client = Client(self.twilio_account_sid, self.twilio_auth_token)
            results = []
            
            for phone_number in phone_numbers:
                try:
                    message_obj = client.messages.create(
                        body=message,
                        from_=f"whatsapp:{self.twilio_phone_number}",
                        to=f"whatsapp:{phone_number}"
                    )
                    results.append({
                        "phone_number": phone_number,
                        "success": True,
                        "message_sid": message_obj.sid
                    })
                except Exception as e:
                    results.append({
                        "phone_number": phone_number,
                        "success": False,
                        "error": str(e)
                    })
            
            logger.info(f"WhatsApp alerts sent to {len(phone_numbers)} recipients")
            return {"success": True, "results": results}
            
        except Exception as e:
            logger.error(f"Failed to send WhatsApp alerts: {str(e)}")
            return {"success": False, "error": str(e)}

    def send_push_notification(self, device_tokens: List[str], title: str, 
                              message: str, data: Optional[Dict] = None) -> Dict[str, any]:
        """
        Send push notification to mobile devices
        
        Args:
            device_tokens: List of device tokens to send notification to
            title: Notification title
            message: Notification message
            data: Additional data payload (optional)
            
        Returns:
            Dictionary with success status and details
        """
        # This would integrate with Firebase Cloud Messaging or similar service
        logger.info(f"Push notifications would be sent to {len(device_tokens)} devices")
        
        # Placeholder implementation
        results = []
        for token in device_tokens:
            results.append({
                "device_token": token,
                "success": True,
                "message": "Notification sent (simulated)"
            })
        
        return {"success": True, "results": results}

    def send_voice_call(self, phone_numbers: List[str], message_url: str) -> Dict[str, any]:
        """
        Initiate voice call with pre-recorded message
        
        Args:
            phone_numbers: List of phone numbers to call
            message_url: URL to TwiML document with voice message
            
        Returns:
            Dictionary with success status and details
        """
        if not self.twilio_account_sid or not self.twilio_auth_token:
            logger.warning("Twilio credentials not configured")
            return {"success": False, "error": "Twilio not configured"}
            
        try:
            client = Client(self.twilio_account_sid, self.twilio_auth_token)
            results = []
            
            for phone_number in phone_numbers:
                try:
                    call = client.calls.create(
                        url=message_url,
                        to=phone_number,
                        from_=self.twilio_phone_number
                    )
                    results.append({
                        "phone_number": phone_number,
                        "success": True,
                        "call_sid": call.sid
                    })
                except Exception as e:
                    results.append({
                        "phone_number": phone_number,
                        "success": False,
                        "error": str(e)
                    })
            
            logger.info(f"Voice calls initiated to {len(phone_numbers)} recipients")
            return {"success": True, "results": results}
            
        except Exception as e:
            logger.error(f"Failed to initiate voice calls: {str(e)}")
            return {"success": False, "error": str(e)}

    async def send_multi_channel_alert(self, recipients: Dict, alert_data: Dict) -> Dict[str, any]:
        """
        Send alert through multiple channels simultaneously
        
        Args:
            recipients: Dictionary with recipient lists for different channels
            alert_data: Dictionary with alert content and metadata
            
        Returns:
            Dictionary with success status and details for all channels
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Prepare alert message
        message = (
            f"🚨 EMERGENCY ALERT 🚨\n"
            f"Fall detected for {alert_data.get('user_name', 'Unknown User')}\n"
            f"Time: {timestamp}\n"
            f"Location: {alert_data.get('location', 'Unknown Location')}\n"
            f"Status: {alert_data.get('status', 'Critical')}\n"
            f"Help is on the way!"
        )
        
        subject = f"Emergency Alert - Fall Detected for {alert_data.get('user_name', 'User')}"
        
        # Create tasks for concurrent execution
        tasks = []
        
        # SMS alerts
        if "sms" in recipients and recipients["sms"]:
            tasks.append(asyncio.create_task(
                asyncio.to_thread(self.send_sms_alert, recipients["sms"], message)
            ))
        else:
            tasks.append(None)
        
        # Email alerts
        if "email" in recipients and recipients["email"]:
            tasks.append(asyncio.create_task(
                asyncio.to_thread(self.send_email_alert, recipients["email"], subject, message)
            ))
        else:
            tasks.append(None)
        
        # WhatsApp alerts
        if "whatsapp" in recipients and recipients["whatsapp"]:
            tasks.append(asyncio.create_task(
                asyncio.to_thread(self.send_whatsapp_alert, recipients["whatsapp"], message)
            ))
        else:
            tasks.append(None)
        
        # Push notifications
        if "push" in recipients and recipients["push"]:
            tasks.append(asyncio.create_task(
                asyncio.to_thread(self.send_push_notification, recipients["push"], "Emergency Alert", message)
            ))
        else:
            tasks.append(None)
        
        # Execute all tasks concurrently
        results = await asyncio.gather(*[task for task in tasks if task is not None], return_exceptions=True)
        
        # Process results
        channel_results = {}
        channel_names = ["sms", "email", "whatsapp", "push"]
        result_index = 0
        
        for i, channel in enumerate(channel_names):
            if tasks[i] is not None:
                channel_results[channel] = results[result_index] if not isinstance(results[result_index], Exception) else {"success": False, "error": str(results[result_index])}
                result_index += 1
            else:
                channel_results[channel] = {"success": False, "error": "Not configured"}
        
        overall_success = any(result.get("success", False) for result in channel_results.values())
        
        logger.info(f"Multi-channel alert sent. Overall success: {overall_success}")
        return {
            "success": overall_success,
            "channels": channel_results,
            "timestamp": timestamp
        }

# Example usage
if __name__ == "__main__":
    alert_system = AlertSystem()
    
    # Example alert data
    recipients = {
        "sms": ["+1234567890"],
        "email": ["caregiver@example.com"],
        "whatsapp": ["+1234567890"]
    }
    
    alert_data = {
        "user_name": "John Doe",
        "location": "Living Room",
        "status": "Fall Detected"
    }
    
    # In a real application, you would run this asynchronously
    # result = asyncio.run(alert_system.send_multi_channel_alert(recipients, alert_data))
    # print(result)
    
    print("AlertSystem ready for use")