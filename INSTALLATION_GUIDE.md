# CareConnect Installation Guide

## 🛠 System Requirements

- **Python**: 3.8 or higher
- **Node.js**: 14 or higher (for React frontend)
- **Operating System**: Windows, macOS, or Linux
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Storage**: 2GB free disk space

## 🚀 Quick Installation

### Windows
1. Double-click `install_and_run.bat`
2. The script will automatically install dependencies and start the server

### Manual Installation
```bash
# Clone the repository (if not already downloaded)
git clone <repository-url>
cd CareConnect

# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install the package in development mode
pip install -e .

# For audio features (optional)
pip install librosa pyttsx3

# Install frontend dependencies
cd frontend/react-dashboard
npm install
```

## 📦 Detailed Installation Steps

### 1. Python Dependencies

Install all required Python packages:
```bash
pip install -r requirements.txt
```

This installs:
- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **OpenCV**: Computer vision
- **MediaPipe**: Pose detection
- **Scikit-learn**: Machine learning
- **TensorFlow**: Deep learning
- **SQLAlchemy**: Database ORM
- **Psycopg2**: PostgreSQL adapter
- **WebSockets**: Real-time communication
- **Twilio**: SMS/Voice services
- **JWT**: Authentication tokens
- **Passlib**: Password hashing
- **Aiofiles**: Async file handling

### 2. Audio Processing Dependencies

For audio-based fall detection:
```bash
pip install librosa
```

### 3. Text-to-Speech Dependencies

For AI voice assistance:
```bash
pip install pyttsx3
```

**Note for Linux users**: You may need to install additional system dependencies:
```bash
sudo apt-get install espeak ffmpeg
```

**Note for macOS users**: You may need to install additional dependencies:
```bash
brew install espeak ffmpeg
```

### 4. Database Setup

CareConnect uses SQLite by default for development:
- No additional setup required
- Database file: `careconnect.db` (auto-created)

For production PostgreSQL:
```bash
# Install PostgreSQL adapter
pip install psycopg2

# Set environment variable
export DATABASE_URL=postgresql://user:password@localhost:5432/careconnect
```

### 5. Frontend Dependencies

For the React dashboard:
```bash
cd frontend/react-dashboard
npm install
```

## ⚙️ Configuration

### Environment Variables

Copy the example configuration:
```bash
cp .env.example .env
```

Edit `.env` with your settings:
```bash
# Database
DATABASE_URL=sqlite:///./careconnect.db

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Twilio (for SMS and voice calls)
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

# WhatsApp Configuration
WHATSAPP_ENABLED=false

# Frontend URL (for CORS)
FRONTEND_URL=http://localhost:3000
```

## ▶️ Running the Application

### Backend Server
```bash
# Method 1: Using the run script
python run.py

# Method 2: Direct FastAPI command
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Method 3: Python module
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The backend will be available at: http://localhost:8000

API Documentation: http://localhost:8000/docs

### Frontend Dashboard

#### Simple HTML Dashboard
Open `frontend/index.html` in a web browser

Or serve it with Python:
```bash
python -m http.server 8080
# Visit http://localhost:8080/frontend/
```

#### React Dashboard
```bash
cd frontend/react-dashboard
npm start
```

The frontend will be available at: http://localhost:3000

## 🐳 Docker Deployment (Production)

### Prerequisites
- Docker installed
- Docker Compose installed

### Deployment
```bash
# Build and start all services
docker-compose up -d

# Services will be available at:
# - Backend API: http://localhost:8000
# - Frontend: http://localhost:3000
# - Database: localhost:5432
```

### Stopping Services
```bash
docker-compose down
```

## 🧪 Testing

### Run Unit Tests
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/
```

### API Testing
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test root endpoint
curl http://localhost:8000/
```

## 🔧 Troubleshooting

### Common Issues

1. **Missing Dependencies**
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

2. **Port Already in Use**
   ```bash
   # Windows
   netstat -ano | findstr :8000
   taskkill /PID <process_id> /F
   
   # macOS/Linux
   lsof -i :8000
   kill -9 <process_id>
   ```

3. **Database Connection Error**
   ```bash
   # Check if database file exists
   ls careconnect.db
   
   # Or recreate database
   rm careconnect.db
   python run.py
   ```

4. **Audio Module Issues**
   ```bash
   # Reinstall audio dependencies
   pip uninstall pyttsx3
   pip install pyttsx3
   ```

5. **Frontend Not Loading**
   ```bash
   # Check if backend is running
   curl http://localhost:8000/health
   
   # Verify CORS settings in main.py
   ```

### Verification Script
Run the verification script to check installation:
```bash
python verify_installation.py
```

## 📈 Performance Optimization

### Production Settings
```bash
# Disable debug mode
export DEBUG=False

# Use production server
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Database Optimization
- Use PostgreSQL in production
- Enable connection pooling
- Configure appropriate indexes

### Caching
- Implement Redis for frequent queries
- Use CDN for static assets

## 🔒 Security Best Practices

1. **Change Default Secrets**
   ```bash
   # Generate a new secret key
   openssl rand -hex 32
   ```

2. **Use HTTPS in Production**
   - Configure SSL certificates
   - Use Nginx reverse proxy

3. **Database Security**
   - Use strong passwords
   - Limit database permissions
   - Enable encryption

4. **API Security**
   - Implement rate limiting
   - Use authentication for all endpoints
   - Validate all inputs

## 🎯 Success Verification

After installation, you should be able to:

✅ Access the backend at http://localhost:8000
✅ View API documentation at http://localhost:8000/docs
✅ See the database file created (careconnect.db)
✅ Run the verification script successfully
✅ Access the frontend dashboard
✅ Test API endpoints

## 📞 Support

For installation issues, contact:
- Email: support@careconnect.health
- GitHub: [Issues Page](https://github.com/yourusername/CareConnect/issues)

---

**CareConnect - Saving Lives Through Technology**