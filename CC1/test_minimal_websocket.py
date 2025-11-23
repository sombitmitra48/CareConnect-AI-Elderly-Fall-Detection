import asyncio
import websockets

async def test_minimal_websocket():
    uri = "ws://127.0.0.1:8001/ws"
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to minimal WebSocket server")
            
            # Send a test message
            await websocket.send("Hello World!")
            print("Sent message: Hello World!")
            
            # Wait for response
            response = await websocket.recv()
            print(f"Received response: {response}")
                
    except Exception as e:
        print(f"Failed to connect: {e}")

if __name__ == "__main__":
    asyncio.run(test_minimal_websocket())