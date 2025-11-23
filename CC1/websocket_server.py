import asyncio
import websockets
import json

async def handle_websocket(websocket, path):
    print(f"New WebSocket connection from {websocket.remote_address}")
    
    # Send welcome message
    await websocket.send(json.dumps({
        "type": "welcome",
        "message": "Connected to CareConnect WebSocket server"
    }))
    
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            
            try:
                data = json.loads(message)
                
                # Handle different message types
                if data.get("type") == "register_client":
                    client_id = data.get("client_id", "unknown")
                    print(f"Client registered: {client_id}")
                    
                    # Send confirmation
                    await websocket.send(json.dumps({
                        "type": "registration_confirmed",
                        "client_id": client_id,
                        "message": f"Client {client_id} registered successfully"
                    }))
                    
                elif data.get("type") == "start_detection":
                    print("Starting detection requested")
                    await websocket.send(json.dumps({
                        "type": "detection_status",
                        "status": "started",
                        "message": "Fall detection started"
                    }))
                    
                elif data.get("type") == "stop_detection":
                    print("Stopping detection requested")
                    await websocket.send(json.dumps({
                        "type": "detection_status",
                        "status": "stopped",
                        "message": "Fall detection stopped"
                    }))
                    
                elif data.get("type") == "emergency_call":
                    print("Emergency call requested")
                    await websocket.send(json.dumps({
                        "type": "emergency_response",
                        "status": "acknowledged",
                        "message": "Emergency call received and being processed"
                    }))
                    
                else:
                    # Echo back any other messages
                    await websocket.send(json.dumps({
                        "type": "echo",
                        "message": f"Echo: {message}"
                    }))
                    
            except json.JSONDecodeError:
                # Echo back non-JSON messages
                await websocket.send(json.dumps({
                    "type": "echo",
                    "message": f"Echo: {message}"
                }))
                
    except websockets.exceptions.ConnectionClosed:
        print("WebSocket connection closed")
    except Exception as e:
        print(f"WebSocket error: {e}")

async def main():
    # Start the WebSocket server
    server = await websockets.serve(handle_websocket, "127.0.0.1", 8001)
    print("WebSocket server started on ws://127.0.0.1:8001")
    await server.wait_closed()

# Create a new event loop and run the server
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped")