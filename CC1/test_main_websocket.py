import asyncio
import websockets
import json

async def test_simple_websocket():
    uri = "ws://127.0.0.1:8000/ws"
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to main WebSocket server")
            
            # Wait for welcome message
            try:
                welcome = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                print(f"Received welcome: {welcome}")
            except asyncio.TimeoutError:
                print("No welcome message received within 5 seconds")
                
            # Send a test message
            test_msg = {
                "type": "test",
                "message": "Hello from client"
            }
            await websocket.send(json.dumps(test_msg))
            print("Sent test message")
            
            # Wait for response
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                print(f"Received response: {response}")
            except asyncio.TimeoutError:
                print("No response received within 5 seconds")
                
            # Test registration
            register_msg = {
                "type": "register_client",
                "client_id": "test_client_123"
            }
            await websocket.send(json.dumps(register_msg))
            print("Sent registration message")
            
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                print(f"Received response: {response}")
            except asyncio.TimeoutError:
                print("No response received within 5 seconds")
                
    except Exception as e:
        print(f"Failed to connect: {e}")

if __name__ == "__main__":
    asyncio.run(test_simple_websocket())