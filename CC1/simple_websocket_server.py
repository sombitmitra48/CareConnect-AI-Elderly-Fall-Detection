import asyncio
import websockets
import json
from datetime import datetime

async def simple_websocket_handler(websocket):
    print(f"New connection from {websocket.remote_address}")
    
    # Send welcome message
    welcome_msg = {
        "type": "welcome",
        "message": "Connected to simple WebSocket server",
        "timestamp": datetime.now().isoformat()
    }
    await websocket.send(json.dumps(welcome_msg))
    
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                print(f"Received: {data}")
                
                # Echo the message back
                response = {
                    "type": "echo",
                    "original_message": data,
                    "timestamp": datetime.now().isoformat()
                }
                await websocket.send(json.dumps(response))
            except json.JSONDecodeError:
                await websocket.send(json.dumps({"error": "Invalid JSON"}))
    except websockets.exceptions.ConnectionClosed:
        print("Connection closed")
    except Exception as e:
        print(f"Error: {e}")

async def main():
    # Start the server on port 8002
    server = await websockets.serve(simple_websocket_handler, "127.0.0.1", 8002)
    print("Starting simple WebSocket server on ws://127.0.0.1:8002")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())