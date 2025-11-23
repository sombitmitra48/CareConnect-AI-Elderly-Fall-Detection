import sys
sys.path.append("CC1")

print("\n=== CareConnect System Status ===")

# Check MediaPipe
try:
    import mediapipe as mp
    print("✓ Video Detection: FULLY OPERATIONAL")
except Exception as e:
    print("⚠ Video Detection: LIMITED (MediaPipe not available)")
    print(f"  Error: {e}")
    print("  Recommendation: Use Python 3.11 for full video detection functionality")

# Check TensorFlow
try:
    import tensorflow as tf
    print("✓ AI Features: FULLY OPERATIONAL")
except Exception as e:
    print("⚠ AI Features: LIMITED (TensorFlow not available)")
    print(f"  Error: {e}")

# Check Librosa
try:
    import librosa
    print("✓ Audio Detection: FULLY OPERATIONAL")
except Exception as e:
    print("⚠ Audio Detection: LIMITED (Librosa not available)")
    print(f"  Error: {e}")

print("================================\n")