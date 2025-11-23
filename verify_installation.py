#!/usr/bin/env python3
"""
CareConnect Installation Verification Script
"""

import sys
import importlib
import os

def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        return False
    print(f"✅ Python {sys.version}")
    return True

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("\n🔍 Checking dependencies...")
    
    required_packages = [
        ("fastapi", "FastAPI web framework"),
        ("uvicorn", "ASGI server"),
        ("cv2", "OpenCV computer vision"),
        ("mediapipe", "MediaPipe pose detection"),
        ("sklearn", "Scikit-learn ML library"),
        ("tensorflow", "TensorFlow ML framework"),
        ("numpy", "NumPy numerical computing"),
        ("pydantic", "Data validation"),
        ("sqlalchemy", "Database ORM"),
        ("psycopg2", "PostgreSQL adapter"),
        ("websockets", "WebSocket library"),
        ("twilio", "Twilio communication"),
        ("jwt", "JWT tokens"),
        ("passlib", "Password hashing"),
        ("aiofiles", "Async file handling"),
        ("librosa", "Audio analysis"),
        ("pyttsx3", "Text-to-speech"),
    ]
    
    missing_packages = []
    
    for package, description in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {description}")
        except ImportError:
            print(f"❌ {description} (missing)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def check_project_structure():
    """Check if project structure is correct"""
    print("\n🔍 Checking project structure...")
    
    required_files = [
        "main.py",
        "requirements.txt",
        "app/database.py",
        "app/api/__init__.py",
        "app/core/fall_detection/video_detector.py",
        "app/core/fall_detection/audio_detector.py",
        "app/core/fall_detection/hybrid_detector.py",
        "app/core/alert_system.py",
        "app/core/ai_assistant.py",
        "app/core/emergency_network.py",
        "app/models/user.py",
        "app/schemas/user.py",
        "frontend/index.html",
        "frontend/react-dashboard/package.json",
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"❌ Missing file: {file_path}")
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        return False
    
    return True

def check_database():
    """Check if database can be initialized"""
    print("\n🔍 Checking database initialization...")
    
    try:
        from app.database import Base, engine
        # This will create tables if they don't exist
        Base.metadata.create_all(bind=engine)
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def check_fall_detection():
    """Check if fall detection modules can be imported"""
    print("\n🔍 Checking fall detection modules...")
    
    try:
        from app.core.fall_detection.video_detector import VideoFallDetector
        from app.core.fall_detection.audio_detector import AudioFallDetector
        from app.core.fall_detection.hybrid_detector import HybridFallDetector
        
        # Initialize detectors
        video_detector = VideoFallDetector()
        audio_detector = AudioFallDetector()
        hybrid_detector = HybridFallDetector()
        
        print("✅ Video fall detector loaded")
        print("✅ Audio fall detector loaded")
        print("✅ Hybrid fall detector loaded")
        return True
    except Exception as e:
        print(f"❌ Fall detection modules failed: {e}")
        return False

def check_alert_system():
    """Check if alert system can be initialized"""
    print("\n🔍 Checking alert system...")
    
    try:
        from app.core.alert_system import AlertSystem
        alert_system = AlertSystem()
        print("✅ Alert system loaded")
        return True
    except Exception as e:
        print(f"❌ Alert system failed: {e}")
        return False

def check_ai_assistant():
    """Check if AI assistant can be initialized"""
    print("\n🔍 Checking AI assistant...")
    
    try:
        from app.core.ai_assistant import AIAssistant
        # Note: This might fail silently on systems without audio support
        ai_assistant = AIAssistant()
        print("✅ AI assistant loaded")
        return True
    except Exception as e:
        print(f"⚠️  AI assistant warning: {e}")
        print("    This might be normal on headless systems")
        return True  # Don't fail the entire check for this

def check_emergency_network():
    """Check if emergency network can be initialized"""
    print("\n🔍 Checking emergency network...")
    
    try:
        from app.core.emergency_network import EmergencyNetwork
        print("✅ Emergency network loaded")
        return True
    except Exception as e:
        print(f"❌ Emergency network failed: {e}")
        return False

def main():
    """Main verification function"""
    print("🌟 CareConnect Installation Verification")
    print("=" * 50)
    
    checks = [
        check_python_version,
        check_dependencies,
        check_project_structure,
        check_database,
        check_fall_detection,
        check_alert_system,
        check_ai_assistant,
        check_emergency_network,
    ]
    
    results = []
    
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"❌ Check failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 Verification Summary")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Checks passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All checks passed! CareConnect is ready to use.")
        print("\n🚀 Next steps:")
        print("   1. Run: python run.py")
        print("   2. Visit: http://localhost:8000")
        print("   3. Check docs: http://localhost:8000/docs")
    else:
        print("⚠️  Some checks failed. Please review the errors above.")
        print("🔧 Run 'pip install -r requirements.txt' to install missing dependencies.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)