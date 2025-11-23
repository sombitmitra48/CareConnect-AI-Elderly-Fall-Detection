import mediapipe as mp
import cv2
import numpy as np

print("MediaPipe version:", mp.__version__)
print("OpenCV version:", cv2.__version__)

# Test MediaPipe Pose
mp_pose = mp.solutions.pose
print("MediaPipe Pose module loaded successfully")

# Create a simple black image to test
image = np.zeros((480, 640, 3), dtype=np.uint8)

# Initialize pose detector
with mp_pose.Pose(static_image_mode=True, model_complexity=1, enable_segmentation=False, min_detection_confidence=0.5) as pose:
    results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    print("Pose detection test completed successfully")
    print("MediaPipe is working correctly!")