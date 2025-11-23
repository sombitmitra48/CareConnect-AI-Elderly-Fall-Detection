# CareConnect Demo Guide

## 🚀 Quick Start Demo

Follow these steps to run a complete demonstration of CareConnect:

### 1. System Requirements
- Python 3.8+
- Node.js 14+ (for React frontend)
- Git (optional, for cloning)

### 2. Installation

#### Option A: Windows (Recommended)
```cmd
# Double-click the install_and_run.bat file
# OR run from command prompt:
install_and_run.bat
```

#### Option B: Manual Installation
```bash
# Install Python dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install the package
pip install -e .

# For audio features, you might need:
pip install librosa pyttsx3
```

### 3. Running the Backend

```bash
# Start the backend server
python run.py

# OR alternatively:
python main.py

# The server will start at http://localhost:8000
# API documentation: http://localhost:8000/docs
```

### 4. Testing API Endpoints

#### Check System Health
```bash
curl http://localhost:8000/health
# Expected: {"status": "healthy"}
```

#### Create a Test User
```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "full_name": "Test User",
    "phone_number": "+1234567890",
    "role": "elderly",
    "password": "testpassword"
  }'
```

#### Trigger Manual Alert
```bash
curl -X POST http://localhost:8000/api/fall-detection/trigger-manual-alert \
  -F "user_id=1" \
  -F "notes=This is a test alert"
```

### 5. Running the Frontend

#### Simple HTML Dashboard
```bash
# Open frontend/index.html in a web browser
# OR serve it with a simple HTTP server:
python -m http.server 8080
# Then visit http://localhost:8080/frontend/
```

#### React Dashboard
```bash
# Navigate to React dashboard
cd frontend/react-dashboard

# Install dependencies
npm install

# Start development server
npm start
# Visit http://localhost:3000
```

### 6. Testing Fall Detection

#### Video Detection (Simulated)
```bash
# Send a test image for fall detection
curl -X POST http://localhost:8000/api/fall-detection/detect-video \
  -F "user_id=1" \
  -F "video_frame=@test_image.jpg"
```

#### Audio Detection (Simulated)
```bash
# Send a test audio file for fall detection
curl -X POST http://localhost:8000/api/fall-detection/detect-audio \
  -F "user_id=1" \
  -F "audio_file=@test_audio.wav"
```

### 7. Docker Deployment (Production)

```bash
# Build and start all services
docker-compose up -d

# Services will be available at:
# - Backend API: http://localhost:8000
# - Frontend: http://localhost:3000
# - Database: localhost:5432
```

## 🎯 Key Demo Features

### 1. Fall Detection System
- Video-based pose analysis
- Audio-based sound detection
- Hybrid confidence scoring

### 2. Multi-Channel Alerts
- SMS notifications (Twilio)
- Email alerts (SMTP)
- Voice calls (Twilio)
- WhatsApp messages (Twilio)

### 3. AI Self-Help Assistant
- Voice guidance for fall recovery
- Breathing exercise instructions
- Panic reduction techniques

### 4. Emergency Response Network
- Volunteer geolocation matching
- Doctor availability system
- Community resource integration

### 5. Real-time Dashboard
- System status monitoring
- Live detection feed
- Alert history tracking
- Emergency team display

## 🧪 Testing Scenarios

### Scenario 1: Normal Operation
1. Start the system
2. Verify all services are running
3. Check dashboard status shows "Active & Monitoring"

### Scenario 2: Fall Detection
1. Trigger video detection endpoint
2. Observe system response
3. Check alert creation in database
4. Verify notification system activation

### Scenario 3: Manual Emergency
1. Click "Emergency Call" button
2. Confirm alert creation
3. Verify caregiver notifications
4. Check emergency team formation

### Scenario 4: AI Assistance
1. Trigger emergency guidance protocol
2. Listen to voice instructions
3. Verify step-by-step guidance
4. Check breathing exercise sequence

## 📊 Monitoring Dashboard

### System Metrics
- Uptime status
- Response times
- Detection accuracy
- Alert processing rates

### User Analytics
- Active user count
- Alert frequency
- Response times
- System usage patterns

## 🔧 Configuration

### Environment Variables
Copy [.env.example](.env.example) to `.env` and configure:
```bash
# Database
DATABASE_URL=sqlite:///./careconnect.db

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256

# Twilio (for SMS/calls)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_phone_number

# Email
SMTP_SERVER=smtp.gmail.com
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Kill process using port 8000
   netstat -ano | findstr :8000
   taskkill /PID <process_id> /F
   ```

2. **Database Connection Error**
   ```bash
   # Check if database file exists
   ls careconnect.db
   
   # Or recreate database
   rm careconnect.db
   python run.py
   ```

3. **Missing Dependencies**
   ```bash
   # Reinstall requirements
   pip install -r requirements.txt --force-reinstall
   ```

4. **Frontend Not Loading**
   ```bash
   # Check if backend is running
   curl http://localhost:8000/health
   
   # Verify CORS settings in main.py
   ```

### Logs and Debugging
```bash
# Check backend logs
tail -f logs/app.log

# Enable debug mode
export DEBUG=True
python run.py
```

## 🎉 Success Metrics

After running the demo, you should see:

✅ Backend server running at http://localhost:8000
✅ API endpoints responding correctly
✅ Database created and accessible
✅ Frontend dashboard loading properly
✅ Alert system components initialized
✅ Fall detection modules loaded
✅ AI assistant ready for voice guidance

## 📞 Support

For issues with the demo, contact:
- Email: support@careconnect.health
- GitHub: [Issues Page](https://github.com/yourusername/CareConnect/issues)

---

**CareConnect - Because Every Second Counts in Elderly Care**