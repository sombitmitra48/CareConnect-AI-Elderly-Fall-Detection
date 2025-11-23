import sys
sys.path.append("CC1")
try:
    from app.core.fall_detection.video_detector import VideoFallDetector
    print("VideoFallDetector imported successfully!")
    detector = VideoFallDetector()
    print("VideoFallDetector initialized successfully!")
    print("MediaPipe available:", getattr(detector, 'mp_pose', None) is not None)
except Exception as e:
    print(f"Error importing VideoFallDetector: {e}")