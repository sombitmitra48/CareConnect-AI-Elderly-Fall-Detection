import pyttsx3
import logging
from typing import List, Dict
import time
import threading

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIAssistant:
    def __init__(self):
        """
        Initialize the AI Assistant for providing voice guidance
        """
        try:
            self.engine = pyttsx3.init()
            self.setup_voice_properties()
            self.is_speaking = False
            logger.info("AI Assistant initialized")
        except Exception as e:
            logger.error(f"Failed to initialize text-to-speech engine: {str(e)}")
            self.engine = None

    def setup_voice_properties(self):
        """
        Configure voice properties for clear, elderly-friendly speech
        """
        if not self.engine:
            return
            
        # Get available voices
        voices = self.engine.getProperty('voices')
        
        # Select a clear, friendly voice (typically female voices are clearer)
        if voices:
            # Try to select a female voice if available
            for voice in voices:
                if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
            else:
                # Use the first available voice
                self.engine.setProperty('voice', voices[0].id)
        
        # Set speech rate (slower for elderly users)
        self.engine.setProperty('rate', 180)  # Words per minute
        
        # Set volume
        self.engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)

    def speak_guidance(self, text: str, blocking: bool = True):
        """
        Speak guidance text to the user
        
        Args:
            text: Text to speak
            blocking: Whether to wait for speech to complete
        """
        if not self.engine:
            logger.warning("Text-to-speech engine not available")
            return
            
        try:
            self.is_speaking = True
            if blocking:
                self.engine.say(text)
                self.engine.runAndWait()
            else:
                self.engine.say(text)
                self.engine.startLoop(False)
                # Small delay to ensure speech starts
                time.sleep(0.1)
            self.is_speaking = False
            logger.info(f"Spoke guidance: {text}")
        except Exception as e:
            logger.error(f"Failed to speak guidance: {str(e)}")
            self.is_speaking = False

    def provide_fall_recovery_guidance(self):
        """
        Provide step-by-step guidance for fall recovery
        """
        guidance_steps = [
            "Stay calm. Help is on the way.",
            "Try to assess if you are injured.",
            "If you can move, try to roll onto your side slowly.",
            "Use your hands to push yourself up to a kneeling position.",
            "Find a sturdy chair or wall for support.",
            "Slowly rise to your feet using the support.",
            "If you feel dizzy or injured, stay still and wait for help."
        ]
        
        for i, step in enumerate(guidance_steps, 1):
            message = f"Step {i}: {step}"
            self.speak_guidance(message)
            # Wait a moment before next instruction
            time.sleep(2)

    def provide_general_assistance(self, situation: str = "general"):
        """
        Provide general assistance based on situation
        
        Args:
            situation: Type of assistance needed
        """
        assistance_messages = {
            "fall_recovery": [
                "Take a deep breath and stay calm.",
                "Try to move your limbs to check for injuries.",
                "If you feel pain, do not move abruptly.",
                "Call for help if you have a personal emergency device.",
                "If you feel able, try to get into a comfortable position."
            ],
            "panic_reduction": [
                "Breathe slowly and deeply.",
                "Count to ten with me: one, two, three, four, five, six, seven, eight, nine, ten.",
                "Focus on your breathing.",
                "Help is on the way. You are safe."
            ],
            "medical_emergency": [
                "Stay perfectly still.",
                "Do not try to move if you feel severe pain.",
                "Keep breathing steadily.",
                "Medical help is coming soon."
            ],
            "general": [
                "Hello, I'm your CareConnect assistant.",
                "I'm here to help you stay safe.",
                "If you need assistance, please let me know.",
                "Remember to stay hydrated and take your medications."
            ]
        }
        
        messages = assistance_messages.get(situation, assistance_messages["general"])
        
        for message in messages:
            self.speak_guidance(message)
            time.sleep(1)

    def emergency_guidance_protocol(self):
        """
        Execute the complete emergency guidance protocol
        """
        # Initial calming message
        self.speak_guidance("Emergency detected. Please stay calm. I am here to help you.")
        time.sleep(1)
        
        # Breathing exercise
        self.speak_guidance("Let's begin with some breathing exercises to help you relax.")
        time.sleep(1)
        
        breathing_exercises = [
            "Breathe in slowly through your nose for four seconds.",
            "Hold your breath for four seconds.",
            "Breathe out slowly through your mouth for six seconds.",
            "Repeat this pattern three times."
        ]
        
        for exercise in breathing_exercises:
            self.speak_guidance(exercise)
            # Wait for user to complete the exercise
            time.sleep(5)
        
        # Recovery guidance
        self.speak_guidance("Now, let me guide you through assessing your condition.")
        time.sleep(1)
        
        self.provide_fall_recovery_guidance()
        
        # Final reassurance
        self.speak_guidance("Help has been notified and is on the way. Please stay calm and follow these instructions.")

    def is_busy(self) -> bool:
        """
        Check if the assistant is currently speaking
        
        Returns:
            True if speaking, False otherwise
        """
        return self.is_speaking

    def stop_speaking(self):
        """
        Stop current speech output
        """
        if self.engine and self.is_speaking:
            try:
                self.engine.stop()
                self.is_speaking = False
                logger.info("Stopped speaking")
            except Exception as e:
                logger.error(f"Failed to stop speaking: {str(e)}")

# Example usage
if __name__ == "__main__":
    assistant = AIAssistant()
    
    # Test the assistant
    # assistant.provide_general_assistance("general")
    
    print("AI Assistant ready for use")