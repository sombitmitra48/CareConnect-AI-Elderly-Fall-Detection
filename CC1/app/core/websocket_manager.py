import json
import logging
from typing import Dict, List, Optional
import asyncio
import websockets
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        """
        Initialize the WebSocket connection manager
        """
        # Store active connections
        self.active_connections: Dict[str, websockets.WebSocketServerProtocol] = {}
        # Store user sessions
        self.user_sessions: Dict[str, str] = {}  # user_id -> connection_id
        # Store client sessions
        self.client_sessions: Dict[str, str] = {}  # client_id -> connection_id
        logger.info("WebSocket ConnectionManager initialized")

    async def connect(self, websocket: websockets.WebSocketServerProtocol, client_id: str):
        """
        Register a new WebSocket connection
        
        Args:
            websocket: WebSocket connection
            client_id: Unique identifier for the client
        """
        self.active_connections[client_id] = websocket
        logger.info(f"Client {client_id} connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, client_id: str):
        """
        Unregister a WebSocket connection
        
        Args:
            client_id: Unique identifier for the client
        """
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            
        # Also remove from user sessions
        if client_id in self.user_sessions:
            user_id = self.user_sessions[client_id]
            del self.user_sessions[client_id]
            
        # Also remove from client sessions
        if client_id in self.client_sessions:
            del self.client_sessions[client_id]
            
        logger.info(f"Client {client_id} disconnected. Total connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, client_id: str):
        """
        Send a message to a specific client
        
        Args:
            message: Message to send
            client_id: Client identifier
        """
        if client_id in self.active_connections:
            try:
                await self.active_connections[client_id].send(message)
                logger.debug(f"Sent message to client {client_id}")
            except websockets.exceptions.ConnectionClosed:
                logger.warning(f"Connection closed for client {client_id}")
                self.disconnect(client_id)
            except Exception as e:
                logger.error(f"Error sending message to client {client_id}: {str(e)}")
                self.disconnect(client_id)
        else:
            logger.warning(f"Client {client_id} not found")

    async def broadcast(self, message: str):
        """
        Broadcast a message to all connected clients
        
        Args:
            message: Message to broadcast
        """
        if self.active_connections:
            # Create a list of tasks to send messages concurrently
            tasks = []
            disconnected_clients = []
            
            for client_id, websocket in self.active_connections.items():
                try:
                    task = asyncio.create_task(websocket.send(message))
                    tasks.append(task)
                except websockets.exceptions.ConnectionClosed:
                    disconnected_clients.append(client_id)
                except Exception as e:
                    logger.error(f"Error sending message to client {client_id}: {str(e)}")
                    disconnected_clients.append(client_id)
            
            # Wait for all messages to be sent
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
            
            # Clean up disconnected clients
            for client_id in disconnected_clients:
                self.disconnect(client_id)
                
            logger.debug(f"Broadcast message to {len(self.active_connections)} clients")
        else:
            logger.debug("No active connections to broadcast to")

    def register_user_session(self, user_id: str, client_id: str):
        """
        Register a user session
        
        Args:
            user_id: User identifier
            client_id: Client identifier
        """
        self.user_sessions[client_id] = user_id
        logger.info(f"Registered user {user_id} with client {client_id}")

    def register_client_session(self, client_id: str):
        """
        Register a client session
        
        Args:
            client_id: Client identifier
        """
        self.client_sessions[client_id] = client_id
        logger.info(f"Registered client session for {client_id}")

    def get_client_for_user(self, user_id: str) -> Optional[str]:
        """
        Get client ID for a user
        
        Args:
            user_id: User identifier
            
        Returns:
            Client ID or None if not found
        """
        for client_id, uid in self.user_sessions.items():
            if uid == user_id:
                return client_id
        return None

    async def send_alert_to_user(self, user_id: str, alert_data: Dict):
        """
        Send an alert to a specific user
        
        Args:
            user_id: User identifier
            alert_data: Alert data to send
        """
        client_id = self.get_client_for_user(user_id)
        if client_id:
            message = {
                "type": "alert",
                "data": alert_data,
                "timestamp": datetime.now().isoformat()
            }
            await self.send_personal_message(json.dumps(message), client_id)
        else:
            logger.warning(f"No active connection found for user {user_id}")

    async def send_status_update(self, user_id: str, status_data: Dict):
        """
        Send a status update to a specific user
        
        Args:
            user_id: User identifier
            status_data: Status data to send
        """
        client_id = self.get_client_for_user(user_id)
        if client_id:
            message = {
                "type": "status_update",
                "data": status_data,
                "timestamp": datetime.now().isoformat()
            }
            await self.send_personal_message(json.dumps(message), client_id)
        else:
            logger.warning(f"No active connection found for user {user_id}")

    async def send_guidance_message(self, user_id: str, guidance_data: Dict):
        """
        Send AI guidance message to a specific user
        
        Args:
            user_id: User identifier
            guidance_data: Guidance data to send
        """
        client_id = self.get_client_for_user(user_id)
        if client_id:
            message = {
                "type": "guidance",
                "data": guidance_data,
                "timestamp": datetime.now().isoformat()
            }
            await self.send_personal_message(json.dumps(message), client_id)
        else:
            logger.warning(f"No active connection found for user {user_id}")

    def get_active_users(self) -> List[str]:
        """
        Get list of currently active users
        
        Returns:
            List of user IDs
        """
        return list(set(self.user_sessions.values()))

    def get_connection_count(self) -> int:
        """
        Get the number of active connections
        
        Returns:
            Number of active connections
        """
        return len(self.active_connections)

# Global connection manager instance
manager = ConnectionManager()

# WebSocket endpoint handler
async def websocket_endpoint(websocket: websockets.WebSocketServerProtocol, path: str):
    """
    Handle incoming WebSocket connections
    
    Args:
        websocket: WebSocket connection
        path: Request path
    """
    # Extract client ID from path or generate one
    client_id = path.strip("/") if path.strip("/") else str(id(websocket))
    logger.info(f"New WebSocket connection attempt from client {client_id}")
    
    try:
        # Accept the connection (this should already be done by FastAPI)
        # But we'll do it here to be explicit
        # await websocket.accept()  # This is done by FastAPI decorator
        
        # Register the connection
        await manager.connect(websocket, client_id)
        logger.info(f"WebSocket connection established for client {client_id}")
        
        # Send a welcome message
        welcome_message = {
            "type": "welcome",
            "message": "Connected to CareConnect WebSocket server",
            "timestamp": datetime.now().isoformat()
        }
        await manager.send_personal_message(json.dumps(welcome_message), client_id)
        
        async for message in websocket:
            # Parse incoming message
            try:
                data = json.loads(message)
                message_type = data.get("type")
                logger.debug(f"Received message from client {client_id}: {message_type}")
                
                if message_type == "register_user":
                    user_id = data.get("user_id")
                    if user_id:
                        manager.register_user_session(user_id, client_id)
                        # Send confirmation
                        await manager.send_personal_message(
                            json.dumps({
                                "type": "registration_confirm",
                                "message": "User registered successfully"
                            }),
                            client_id
                        )
                        logger.info(f"User {user_id} registered for client {client_id}")
                        
                elif message_type == "register_client":
                    # Register client session
                    manager.register_client_session(client_id)
                    # Send confirmation
                    await manager.send_personal_message(
                        json.dumps({
                            "type": "registration_confirm",
                            "message": "Client registered successfully"
                        }),
                        client_id
                    )
                    logger.info(f"Client {client_id} registered")
                        
                elif message_type == "heartbeat":
                    # Respond to heartbeat
                    await manager.send_personal_message(
                        json.dumps({
                            "type": "heartbeat_response",
                            "timestamp": datetime.now().isoformat()
                        }),
                        client_id
                    )
                    logger.debug(f"Heartbeat response sent to client {client_id}")
                    
                elif message_type == "start_detection":
                    # Handle start detection request
                    await manager.send_personal_message(
                        json.dumps({
                            "type": "status_update",
                            "data": {
                                "videoDetection": "Active",
                                "audioDetection": "Active",
                                "alertSystem": "Active",
                                "aiAssistant": "Active",
                                "emergencyNetwork": "Active"
                            }
                        }),
                        client_id
                    )
                    logger.info(f"Start detection request handled for client {client_id}")
                    
                elif message_type == "stop_detection":
                    # Handle stop detection request
                    await manager.send_personal_message(
                        json.dumps({
                            "type": "status_update",
                            "data": {
                                "videoDetection": "Limited (MediaPipe not available)",
                                "audioDetection": "Active",
                                "alertSystem": "Active",
                                "aiAssistant": "Active",
                                "emergencyNetwork": "Active"
                            }
                        }),
                        client_id
                    )
                    logger.info(f"Stop detection request handled for client {client_id}")
                    
                else:
                    logger.warning(f"Unknown message type from client {client_id}: {message_type}")
                    
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON received from client {client_id}: {message}")
            except Exception as e:
                logger.error(f"Error processing message from client {client_id}: {str(e)}")
                
    except websockets.exceptions.ConnectionClosed:
        logger.info(f"Connection closed for client {client_id}")
    except Exception as e:
        logger.error(f"Error handling WebSocket connection for client {client_id}: {str(e)}")
    finally:
        # Unregister the connection
        manager.disconnect(client_id)
        logger.info(f"WebSocket connection cleanup completed for client {client_id}")

# Example usage
if __name__ == "__main__":
    print("WebSocket manager ready for use")