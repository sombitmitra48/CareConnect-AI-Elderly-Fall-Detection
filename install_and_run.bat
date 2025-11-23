@echo off
echo 🌟 CareConnect - AI Guardian for the Elderly
echo ========================================
echo.

echo 🔧 Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install requirements
    pause
    exit /b %errorlevel%
)

echo 🔧 Installing development dependencies...
pip install -r requirements-dev.txt
if %errorlevel% neq 0 (
    echo ⚠️  Warning: Failed to install development requirements (optional)
)

echo 📦 Installing CareConnect package...
pip install -e .
if %errorlevel% neq 0 (
    echo ❌ Failed to install CareConnect package
    pause
    exit /b %errorlevel%
)

echo ✅ Installation complete!
echo.

echo 🚀 Starting CareConnect backend server...
echo Server will be available at http://localhost:8000
echo Documentation at http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python run.py

pause