import cv2
import numpy as np
from typing import List, Tuple
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import MediaPipe, but make it optional
try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
    logger.info("MediaPipe successfully imported")
except Exception as e:
    logger.warning(f"MediaPipe not available: {e}. Video fall detection will be limited. This is likely due to Python 3.13 compatibility issues. Consider using Python 3.11 for full functionality.")
    MEDIAPIPE_AVAILABLE = False
    mp = None

# Try to import TensorFlow, but make it optional
try:
    import tensorflow as tf
    TENSORFLOW_AVAILABLE = True
    logger.info("TensorFlow successfully imported")
except Exception as e:
    logger.warning(f"TensorFlow not available: {e}. Some AI features will be limited.")
    TENSORFLOW_AVAILABLE = False
    tf = None

class VideoFallDetector:
    def __init__(self):
        """
        Initialize the VideoFallDetector with MediaPipe Pose model
        """
        if MEDIAPIPE_AVAILABLE:
            try:
                self.mp_pose = mp.solutions.pose
                self.mp_drawing = mp.solutions.drawing_utils
                self.pose = self.mp_pose.Pose(
                    static_image_mode=False,
                    model_complexity=1,
                    enable_segmentation=False,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5
                )
                logger.info("MediaPipe Pose model initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize MediaPipe Pose model: {e}")
        else:
            self.mp_pose = None
            self.mp_drawing = None
            self.pose = None
        
        # Fall detection parameters
        self.FALL_THRESHOLD = 0.7  # Threshold for fall detection confidence
        self.VERTICAL_CHANGE_THRESHOLD = 0.3  # Significant vertical movement threshold
        self.ANGLE_CHANGE_THRESHOLD = 45  # Angle change threshold for unnatural poses
        
        logger.info("VideoFallDetector initialized")

    def detect_pose(self, frame: np.ndarray) -> dict:
        """
        Detect human pose in the given frame using MediaPipe
        
        Args:
            frame: Input image frame (BGR)
            
        Returns:
            Dictionary containing pose landmarks and detection results
        """
        if not MEDIAPIPE_AVAILABLE:
            # Return a basic result when MediaPipe is not available
            return {
                "landmarks": None,
                "visibility": False
            }
        
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        results = self.pose.process(rgb_frame)
        
        pose_data = {
            "landmarks": None,
            "visibility": False
        }
        
        if results.pose_landmarks:
            pose_data["landmarks"] = results.pose_landmarks
            pose_data["visibility"] = True
            
        return pose_data

    def calculate_vertical_movement(self, landmarks, prev_landmarks) -> float:
        """
        Calculate vertical movement between frames
        
        Args:
            landmarks: Current frame landmarks
            prev_landmarks: Previous frame landmarks
            
        Returns:
            Vertical movement value
        """
        if not prev_landmarks:
            return 0.0
            
        # Get hip positions (landmark indices 23 and 24)
        current_hip_y = (landmarks.landmark[23].y + landmarks.landmark[24].y) / 2
        prev_hip_y = (prev_landmarks.landmark[23].y + prev_landmarks.landmark[24].y) / 2
        
        # Calculate vertical change
        vertical_change = abs(current_hip_y - prev_hip_y)
        return vertical_change

    def calculate_body_angles(self, landmarks) -> List[float]:
        """
        Calculate key body angles for fall detection
        
        Args:
            landmarks: Pose landmarks
            
        Returns:
            List of calculated angles
        """
        angles = []
        
        # Calculate torso angle (between shoulders and hips)
        shoulder_midpoint = (
            (landmarks.landmark[11].x + landmarks.landmark[12].x) / 2,
            (landmarks.landmark[11].y + landmarks.landmark[12].y) / 2
        )
        
        hip_midpoint = (
            (landmarks.landmark[23].x + landmarks.landmark[24].x) / 2,
            (landmarks.landmark[23].y + landmarks.landmark[24].y) / 2
        )
        
        # Calculate angle with vertical axis
        delta_x = hip_midpoint[0] - shoulder_midpoint[0]
        delta_y = hip_midpoint[1] - shoulder_midpoint[1]
        
        if delta_y != 0:
            angle = np.degrees(np.arctan(delta_x / delta_y))
            angles.append(abs(angle))
        
        return angles

    def is_fall_detected(self, landmarks, prev_landmarks) -> Tuple[bool, float]:
        """
        Determine if a fall is detected based on pose analysis
        
        Args:
            landmarks: Current frame landmarks
            prev_landmarks: Previous frame landmarks
            
        Returns:
            Tuple of (is_fall, confidence_score)
        """
        if not MEDIAPIPE_AVAILABLE or not landmarks or not prev_landmarks:
            return False, 0.0
            
        # Calculate vertical movement
        vertical_movement = self.calculate_vertical_movement(landmarks, prev_landmarks)
        
        # Calculate body angles
        angles = self.calculate_body_angles(landmarks)
        
        # Analyze for fall indicators
        fall_indicators = 0
        confidence_score = 0.0
        
        # Check for significant vertical movement
        if vertical_movement > self.VERTICAL_CHANGE_THRESHOLD:
            fall_indicators += 1
            confidence_score += 0.3
            
        # Check for unnatural body angles (suggesting lying down)
        if angles and any(angle > self.ANGLE_CHANGE_THRESHOLD for angle in angles):
            fall_indicators += 1
            confidence_score += 0.4
            
        # Additional checks could be added here
            
        # Normalize confidence score
        confidence_score = min(confidence_score, 1.0)
        
        # Determine if fall is detected based on thresholds
        is_fall = confidence_score >= self.FALL_THRESHOLD
        
        return is_fall, confidence_score

    def process_video_stream(self, video_source=0):
        """
        Process video stream for fall detection (for testing purposes)
        
        Args:
            video_source: Camera source index or video file path
        """
        if not MEDIAPIPE_AVAILABLE:
            logger.error("MediaPipe not available. Cannot process video stream.")
            return
            
        cap = cv2.VideoCapture(video_source)
        
        if not cap.isOpened():
            logger.error("Cannot open video source")
            return
            
        prev_landmarks = None
        frame_count = 0
        
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                    
                # Detect pose
                pose_result = self.detect_pose(frame)
                
                if pose_result["visibility"]:
                    landmarks = pose_result["landmarks"]
                    
                    # Check for fall every few frames for performance
                    if frame_count % 5 == 0:
                        is_fall, confidence = self.is_fall_detected(landmarks, prev_landmarks)
                        
                        if is_fall:
                            logger.warning(f"FALL DETECTED! Confidence: {confidence:.2f}")
                            
                            # Draw red bounding box for fall
                            h, w, _ = frame.shape
                            cv2.rectangle(frame, (0, 0), (w, h), (0, 0, 255), 3)
                            cv2.putText(frame, f"FALL DETECTED! ({confidence:.2f})", 
                                      (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        else:
                            # Draw green bounding box for normal
                            h, w, _ = frame.shape
                            cv2.rectangle(frame, (0, 0), (w, h), (0, 255, 0), 2)
                            cv2.putText(frame, f"NORMAL ({confidence:.2f})", 
                                      (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
                    # Draw pose landmarks
                    self.mp_drawing.draw_landmarks(
                        frame, landmarks, self.mp_pose.POSE_CONNECTIONS)
                    
                    prev_landmarks = landmarks
                
                frame_count += 1
                
                # Display the frame
                cv2.imshow('CareConnect - Fall Detection', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
        except Exception as e:
            logger.error(f"Error processing video stream: {str(e)}")
        finally:
            cap.release()
            cv2.destroyAllWindows()

# Example usage
if __name__ == "__main__":
    detector = VideoFallDetector()
    # For testing with webcam (uncomment to use)
    # detector.process_video_stream()