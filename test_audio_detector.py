import sys
sys.path.append("CC1")
try:
    from app.core.fall_detection.audio_detector import AudioFallDetector
    print("AudioFallDetector imported successfully!")
    detector = AudioFallDetector()
    print("AudioFallDetector initialized successfully!")
    print("Librosa available:", getattr(detector, 'model', None) is not None)
except Exception as e:
    print(f"Error importing AudioFallDetector: {e}")