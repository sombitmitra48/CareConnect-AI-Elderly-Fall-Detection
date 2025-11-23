from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import json
from app.api import router as api_router
from app.database import engine, Base

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CareConnect - AI Guardian for the Elderly")

# Add CORS middleware with more permissive settings for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")

# Simple WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket):
    await websocket.accept()
    print("WebSocket connection established")
    
    # Send welcome message
    await websocket.send_text(json.dumps({
        "type": "welcome",
        "message": "Connected to CareConnect WebSocket server"
    }))
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            print(f"Received message: {data}")
            
            try:
                message = json.loads(data)
                
                # Handle different message types
                if message.get("type") == "register_client":
                    client_id = message.get("client_id", "unknown")
                    print(f"Client registered: {client_id}")
                    
                    # Send confirmation
                    await websocket.send_text(json.dumps({
                        "type": "registration_confirmed",
                        "client_id": client_id,
                        "message": f"Client {client_id} registered successfully"
                    }))
                    
                elif message.get("type") == "start_detection":
                    print("Starting detection requested")
                    await websocket.send_text(json.dumps({
                        "type": "detection_status",
                        "status": "started",
                        "message": "Fall detection started"
                    }))
                    
                elif message.get("type") == "stop_detection":
                    print("Stopping detection requested")
                    await websocket.send_text(json.dumps({
                        "type": "detection_status",
                        "status": "stopped",
                        "message": "Fall detection stopped"
                    }))
                    
                elif message.get("type") == "emergency_call":
                    print("Emergency call requested")
                    await websocket.send_text(json.dumps({
                        "type": "emergency_response",
                        "status": "acknowledged",
                        "message": "Emergency call received and being processed"
                    }))
                    
                else:
                    # Echo back any other messages
                    await websocket.send_text(json.dumps({
                        "type": "echo",
                        "message": f"Echo: {data}"
                    }))
                    
            except json.JSONDecodeError:
                # Echo back non-JSON messages
                await websocket.send_text(json.dumps({
                    "type": "echo",
                    "message": f"Echo: {data}"
                }))
                
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        print("WebSocket connection closed")

@app.get("/")
async def root():
    return {"message": "CareConnect - AI Guardian for the Elderly"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )