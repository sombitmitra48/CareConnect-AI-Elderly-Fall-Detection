import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://127.0.0.1:8000/ws"
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket server")
            
            # Send registration message
            registration_msg = {
                "type": "register_client",
                "client_id": "python_test_client"
            }
            await websocket.send(json.dumps(registration_msg))
            print("Sent registration message")
            
            # Wait for a response
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                print(f"Received: {response}")
            except asyncio.TimeoutError:
                print("No response received within 5 seconds")
                
    except Exception as e:
        print(f"Failed to connect: {e}")

if __name__ == "__main__":
    asyncio.run(test_websocket())