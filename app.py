"""
Flask application for CarPlay dongle detection and communication.
Uses WebSockets for real-time communication with the frontend.
"""

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'

# Enable CORS for development
CORS(app)

# Initialize SocketIO with CORS settings
socketio = SocketIO(app, cors_allowed_origins="*")

# Store connected clients and their dongle status
connected_clients = {}


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@socketio.on('connect')
def handle_connect():
    """Handle new WebSocket connections"""
    print(f'Client connected: {request.sid}')
    connected_clients[request.sid] = {'dongle_connected': False}
    emit('connection_response', {'status': 'connected'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnections"""
    print(f'Client disconnected: {request.sid}')
    if request.sid in connected_clients:
        del connected_clients[request.sid]


@socketio.on('dongle_connected')
def handle_dongle_connected(data):
    """Handle dongle connection event from frontend"""
    print(f'Dongle connected: {data}')
    connected_clients[request.sid]['dongle_connected'] = True
    connected_clients[request.sid]['dongle_info'] = data
    
    # Broadcast to all clients (or just respond to sender)
    emit('dongle_status', {
        'connected': True,
        'device_info': data
    })


@socketio.on('dongle_disconnected')
def handle_dongle_disconnected():
    """Handle dongle disconnection event from frontend"""
    print('Dongle disconnected')
    if request.sid in connected_clients:
        connected_clients[request.sid]['dongle_connected'] = False
    
    emit('dongle_status', {'connected': False})


@socketio.on('usb_data')
def handle_usb_data(data):
    """Handle USB data received from the dongle"""
    print(f'Received USB data: {data}')
    
    # Process the data here
    # For now, just echo it back
    emit('usb_response', {
        'status': 'received',
        'data': data
    })


@socketio.on('send_command')
def handle_send_command(data):
    """Handle command to send to dongle"""
    command = data.get('command')
    print(f'Command to send to dongle: {command}')
    
    # Echo back to frontend, which will actually send via WebUSB
    emit('send_to_dongle', {
        'command': command,
        'timestamp': data.get('timestamp')
    })


if __name__ == '__main__':
    # Run with socketio
    print('Starting Flask-SocketIO server...')
    print('Open https://localhost:5000 in your browser')
    print('Note: WebUSB requires HTTPS. See README for certificate setup.')
    
    # For development with self-signed certificate:
    socketio.run(app, 
                 host='0.0.0.0', 
                 port=5000, 
                 debug=True,
                 ssl_context='adhoc')  # Creates self-signed cert
