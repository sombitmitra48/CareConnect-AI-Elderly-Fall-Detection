// CareConnect Frontend JavaScript
// Handle real-time updates and user interactions

// Use the correct backend URL
const BACKEND_URL = 'http://127.0.0.1:8000';
const WEBSOCKET_URL = 'ws://127.0.0.1:8000'; // WebSocket URL

let websocket;
let isDetecting = false;
let clientId = 'frontend_' + Date.now(); // Unique client ID
let reconnectAttempts = 0;
const MAX_RECONNECT_ATTEMPTS = 5;
let reconnectTimeout;

// DOM Elements
const statusElement = document.getElementById('status');
const detectionButton = document.getElementById('toggleDetection');
const alertButton = document.getElementById('emergencyBtn');
const responseTeam = document.querySelector('.response-team');
const systemStatus = document.querySelector('.status-grid');

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('CareConnect Frontend Loaded');
    initializeWebSocket();
    updateSystemStatus();
});

// Initialize WebSocket connection
function initializeWebSocket() {
    try {
        // Clear any existing reconnect timeout
        if (reconnectTimeout) {
            clearTimeout(reconnectTimeout);
            reconnectTimeout = null;
        }
        
        // Close existing connection if any
        if (websocket) {
            console.log('Closing existing WebSocket connection');
            websocket.close();
        }
        
        // Create WebSocket connection
        console.log(`Attempting to connect to WebSocket at: ${WEBSOCKET_URL}/ws`);
        websocket = new WebSocket(`${WEBSOCKET_URL}/ws`);
        
        websocket.onopen = function(event) {
            console.log('WebSocket connected successfully');
            reconnectAttempts = 0; // Reset reconnect attempts
            updateStatus('Connected to CareConnect system', 'online');
            showNotification('Connected to CareConnect system', 'success');
            
            // Register this client with the backend
            sendWebSocketMessage({
                type: 'register_client',
                client_id: clientId
            });
        };
        
        websocket.onmessage = function(event) {
            try {
                const data = JSON.parse(event.data);
                console.log('Received WebSocket message:', data);
                handleWebSocketMessage(data);
            } catch (e) {
                console.error('Error parsing WebSocket message:', e, event.data);
            }
        };
        
        websocket.onclose = function(event) {
            console.log('WebSocket disconnected. Code:', event.code, 'Reason:', event.reason);
            updateStatus('Disconnected from CareConnect system', 'offline');
            
            // Attempt to reconnect with exponential backoff
            if (reconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
                reconnectAttempts++;
                const reconnectDelay = Math.min(1000 * Math.pow(2, reconnectAttempts), 10000); // Max 10 seconds
                console.log(`Reconnecting in ${reconnectDelay/1000} seconds... (Attempt ${reconnectAttempts}/${MAX_RECONNECT_ATTEMPTS})`);
                showNotification(`Connection lost. Reconnecting in ${reconnectDelay/1000} seconds...`, 'warning');
                
                reconnectTimeout = setTimeout(initializeWebSocket, reconnectDelay);
            } else {
                console.log('Max reconnect attempts reached');
                showNotification('Failed to reconnect after multiple attempts', 'error');
            }
        };
        
        websocket.onerror = function(error) {
            console.error('WebSocket error:', error);
            updateStatus('Connection error', 'error');
            showNotification('Connection error occurred', 'error');
        };
    } catch (error) {
        console.error('Failed to initialize WebSocket:', error);
        updateStatus('Connection failed', 'error');
        showNotification('Failed to connect to backend services: ' + error.message, 'error');
    }
}

// Send message through WebSocket
function sendWebSocketMessage(message) {
    if (websocket && websocket.readyState === WebSocket.OPEN) {
        console.log('Sending WebSocket message:', message);
        websocket.send(JSON.stringify(message));
    } else {
        console.warn('WebSocket not connected. Message not sent:', message, 'Ready state:', websocket ? websocket.readyState : 'null');
        // Try to reconnect if not connected
        if (!websocket || websocket.readyState === WebSocket.CLOSED) {
            console.log('Attempting to reconnect WebSocket');
            initializeWebSocket();
        }
    }
}

// Handle WebSocket messages
function handleWebSocketMessage(data) {
    console.log('Processing WebSocket message:', data);
    
    switch(data.type) {
        case 'welcome':
            console.log('Welcome message received:', data.message);
            break;
        case 'registration_confirm':
            console.log('Client registered successfully');
            break;
        case 'status_update':
            updateSystemStatus(data.data);
            break;
        case 'fall_detected':
            handleFallDetection(data.data);
            break;
        case 'alert_sent':
            showNotification('Alert sent to emergency contacts', 'success');
            break;
        case 'ai_assistant':
            handleAIAssistant(data.data);
            break;
        case 'heartbeat_response':
            // Handle heartbeat response if needed
            break;
        case 'echo':
            console.log('Echo response:', data.message);
            break;
        default:
            console.log('Unknown message type:', data.type);
    }
}

// Update system status display
function updateSystemStatus(statusData = null) {
    if (!statusData) {
        // Default status
        statusData = {
            videoDetection: 'Limited (MediaPipe not available)',
            audioDetection: 'Active',
            alertSystem: 'Active',
            aiAssistant: 'Active',
            emergencyNetwork: 'Active'
        };
    }
    
    // Update status cards
    document.querySelectorAll('.status-card').forEach(card => {
        const title = card.querySelector('h3').textContent.toLowerCase();
        let status = 'Unknown';
        let statusClass = '';
        
        if (title.includes('video')) {
            status = statusData.videoDetection || 'Limited';
            statusClass = statusData.videoDetection === 'Active' ? 'status-active' : 'status-warning';
        } else if (title.includes('audio')) {
            status = statusData.audioDetection || 'Active';
            statusClass = 'status-active';
        } else if (title.includes('alert')) {
            status = statusData.alertSystem || 'Active';
            statusClass = 'status-active';
        } else if (title.includes('ai') || title.includes('assistant')) {
            status = statusData.aiAssistant || 'Active';
            statusClass = 'status-active';
        } else if (title.includes('network') || title.includes('emergency')) {
            status = statusData.emergencyNetwork || 'Active';
            statusClass = 'status-active';
        }
        
        const statusElement = card.querySelector('.status-indicator');
        if (statusElement) {
            statusElement.textContent = status;
            statusElement.className = 'status-indicator ' + statusClass;
        }
    });
}

// Toggle fall detection
function toggleDetection() {
    console.log('Toggle detection clicked. WebSocket state:', websocket ? websocket.readyState : 'null');
    if (!websocket || websocket.readyState !== WebSocket.OPEN) {
        showNotification('Not connected to backend services. Attempting to reconnect...', 'error');
        initializeWebSocket(); // Try to reconnect
        return;
    }
    
    isDetecting = !isDetecting;
    
    if (isDetecting) {
        // Start detection
        detectionButton.textContent = '⏹ Stop Detection';
        detectionButton.className = 'btn btn-danger';
        updateStatus('Fall detection active', 'active');
        
        // Send start detection message
        sendWebSocketMessage({
            type: 'start_detection',
            payload: {
                timestamp: new Date().toISOString()
            }
        });
    } else {
        // Stop detection
        detectionButton.textContent = '▶ Start Detection';
        detectionButton.className = 'btn btn-primary';
        updateStatus('Fall detection inactive', 'online');
        
        // Send stop detection message
        sendWebSocketMessage({
            type: 'stop_detection',
            payload: {
                timestamp: new Date().toISOString()
            }
        });
    }
}

// Handle fall detection events
function handleFallDetection(data) {
    console.log('Fall detected:', data);
    
    // Update UI
    updateStatus('FALL DETECTED!', 'alert');
    showNotification(`Fall detected with confidence: ${data.confidence}`, 'alert');
    
    // Visual alert
    document.body.classList.add('fall-alert');
    setTimeout(() => {
        document.body.classList.remove('fall-alert');
    }, 5000);
    
    // Try to trigger AI assistant
    sendWebSocketMessage({
        type: 'ai_assistant_request',
        payload: {
            message: 'Fall detected, provide assistance guidance',
            timestamp: new Date().toISOString()
        }
    });
}

// Handle AI assistant responses
function handleAIAssistant(data) {
    console.log('AI Assistant response:', data);
    showNotification(data.message, 'info');
    
    // If browser supports speech synthesis, speak the message
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(data.message);
        utterance.lang = 'en-US';
        speechSynthesis.speak(utterance);
    }
}

// Send emergency alert
function sendEmergencyAlert() {
    console.log('Emergency alert clicked. WebSocket state:', websocket ? websocket.readyState : 'null');
    if (!websocket || websocket.readyState !== WebSocket.OPEN) {
        showNotification('Not connected to backend services. Attempting to reconnect...', 'error');
        initializeWebSocket(); // Try to reconnect
        return;
    }
    
    // Confirm before sending
    if (confirm('Send emergency alert to all contacts?')) {
        sendWebSocketMessage({
            type: 'emergency_alert',
            payload: {
                message: 'Emergency alert triggered manually',
                timestamp: new Date().toISOString(),
                location: {
                    latitude: 0,
                    longitude: 0
                }
            }
        });
        
        showNotification('Emergency alert sent!', 'alert');
    }
}

// Update connection status display
function updateStatus(message, statusClass) {
    console.log('Updating status:', message, statusClass);
    if (statusElement) {
        statusElement.textContent = message;
        statusElement.className = `status ${statusClass}`;
    }
}

// Show notification message
function showNotification(message, type = 'info') {
    console.log('Showing notification:', message, type);
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Add to document
    document.body.appendChild(notification);
    
    // Remove after delay
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 5000);
}

// Event Listeners
if (detectionButton) {
    detectionButton.addEventListener('click', toggleDetection);
}

if (alertButton) {
    alertButton.addEventListener('click', sendEmergencyAlert);
}

// Handle page visibility changes
document.addEventListener('visibilitychange', function() {
    console.log('Page visibility changed. Hidden:', document.hidden);
    if (!document.hidden && (!websocket || websocket.readyState === WebSocket.CLOSED)) {
        // Reconnect when page becomes visible
        console.log('Page became visible, attempting to reconnect WebSocket');
        reconnectAttempts = 0; // Reset reconnect attempts
        initializeWebSocket();
    }
});

// Send heartbeat periodically to keep connection alive
setInterval(() => {
    if (websocket && websocket.readyState === WebSocket.OPEN) {
        sendWebSocketMessage({
            type: 'heartbeat',
            timestamp: new Date().toISOString()
        });
    }
}, 30000); // Every 30 seconds

console.log('CareConnect frontend initialized');