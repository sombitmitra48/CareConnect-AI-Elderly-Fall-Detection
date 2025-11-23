from app.core.fall_detection.video_detector import VideoFallDetector
from app.core.fall_detection.audio_detector import AudioFallDetector
import logging
from typing import Tuple, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HybridFallDetector:
    def __init__(self):
        """
        Initialize the Hybrid Fall Detector with both video and audio detectors
        """
        self.video_detector = VideoFallDetector()
        self.audio_detector = AudioFallDetector()
        
        # Hybrid detection parameters
        self.VIDEO_WEIGHT = 0.6
        self.AUDIO_WEIGHT = 0.4
        self.HYBRID_THRESHOLD = 0.65  # Threshold for hybrid fall detection
        
        logger.info("HybridFallDetector initialized")

    def detect_fall(self, video_frame=None, audio_data=None) -> Tuple[bool, float, dict]:
        """
        Detect fall using both video and audio data
        
        Args:
            video_frame: Video frame for pose analysis
            audio_data: Audio data for sound analysis
            
        Returns:
            Tuple of (is_fall, confidence_score, details)
        """
        video_fall = False
        video_confidence = 0.0
        audio_fall = False
        audio_confidence = 0.0
        
        # Video-based detection
        if video_frame is not None and hasattr(self.video_detector, 'mp_pose') and self.video_detector.mp_pose is not None:
            try:
                pose_result = self.video_detector.detect_pose(video_frame)
                if pose_result["visibility"]:
                    # For simplicity, we're not tracking previous landmarks here
                    # In a real implementation, you'd need to maintain state
                    video_fall, video_confidence = self.video_detector.is_fall_detected(
                        pose_result["landmarks"], None)
            except Exception as e:
                logger.error(f"Error in video fall detection: {str(e)}")
        
        # Audio-based detection
        if audio_data is not None and hasattr(self.audio_detector, 'model') and self.audio_detector.model is not None:
            try:
                audio_fall, audio_confidence = self.audio_detector.detect_fall_sound(audio_data)
            except Exception as e:
                logger.error(f"Error in audio fall detection: {str(e)}")
        
        # Combine results using weighted average
        hybrid_confidence = (
            self.VIDEO_WEIGHT * video_confidence + 
            self.AUDIO_WEIGHT * audio_confidence
        )
        
        # Determine if fall is detected based on hybrid threshold
        is_fall = hybrid_confidence >= self.HYBRID_THRESHOLD
        
        details = {
            "video_fall": video_fall,
            "video_confidence": video_confidence,
            "audio_fall": audio_fall,
            "audio_confidence": audio_confidence,
            "hybrid_confidence": hybrid_confidence
        }
        
        return is_fall, hybrid_confidence, details

    def update_audio_model(self, audio_samples, labels):
        """
        Update the audio detection model with new samples
        
        Args:
            audio_samples: List of audio samples
            labels: Corresponding labels for the samples
        """
        try:
            self.audio_detector.train_model(audio_samples, labels)
            logger.info("Audio model updated successfully")
        except Exception as e:
            logger.error(f"Error updating audio model: {str(e)}")

# Example usage
if __name__ == "__main__":
    detector = HybridFallDetector()
    # For testing (uncomment to use)
    # is_fall, confidence, details = detector.detect_fall()
    # print(f"Fall detected: {is_fall}, Confidence: {confidence}")