/**
 * Socket Handler for WebSocket Communication with Flask Backend
 */

class SocketHandler {
    constructor() {
        this.socket = null;
        this.isConnected = false;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
    }

    /**
     * Initialize socket connection
     */
    connect() {
        // Connect to Flask-SocketIO server
        this.socket = io({
            transports: ['websocket'],
            reconnection: true,
            reconnectionDelay: 1000,
            reconnectionDelayMax: 5000,
            reconnectionAttempts: this.maxReconnectAttempts
        });

        this.setupEventListeners();
    }

    /**
     * Setup socket event listeners
     */
    setupEventListeners() {
        // Connection events
        this.socket.on('connect', () => {
            console.log('Connected to server');
            this.isConnected = true;
            this.reconnectAttempts = 0;
            this.notifyConnectionStatus(true);
        });

        this.socket.on('disconnect', () => {
            console.log('Disconnected from server');
            this.isConnected = false;
            this.notifyConnectionStatus(false);
        });

        this.socket.on('connect_error', (error) => {
            console.error('Connection error:', error);
            this.reconnectAttempts++;
        });

        // Custom events from server
        this.socket.on('connection_response', (data) => {
            console.log('Connection response:', data);
        });

        this.socket.on('dongle_status', (data) => {
            console.log('Dongle status update:', data);
            window.dispatchEvent(new CustomEvent('server-dongle-status', {
                detail: data
            }));
        });

        this.socket.on('usb_response', (data) => {
            console.log('USB response from server:', data);
            window.dispatchEvent(new CustomEvent('server-usb-response', {
                detail: data
            }));
        });

        this.socket.on('send_to_dongle', (data) => {
            console.log('Server requests sending to dongle:', data);
            window.dispatchEvent(new CustomEvent('server-send-command', {
                detail: data
            }));
        });
    }

    /**
     * Notify connection status change
     */
    notifyConnectionStatus(connected) {
        window.dispatchEvent(new CustomEvent('socket-connection-status', {
            detail: { connected }
        }));
    }

    /**
     * Emit dongle connected event
     */
    emitDongleConnected(deviceInfo) {
        if (this.isConnected) {
            this.socket.emit('dongle_connected', deviceInfo);
        }
    }

    /**
     * Emit dongle disconnected event
     */
    emitDongleDisconnected() {
        if (this.isConnected) {
            this.socket.emit('dongle_disconnected');
        }
    }

    /**
     * Send USB data to server
     */
    sendUSBData(data) {
        if (this.isConnected) {
            this.socket.emit('usb_data', {
                data: Array.from(data),  // Convert Uint8Array to regular array
                timestamp: Date.now()
            });
        }
    }

    /**
     * Send command request
     */
    sendCommand(command) {
        if (this.isConnected) {
            this.socket.emit('send_command', {
                command: command,
                timestamp: Date.now()
            });
        }
    }

    /**
     * Disconnect socket
     */
    disconnect() {
        if (this.socket) {
            this.socket.disconnect();
        }
    }
}

// Create global instance
window.socketHandler = new SocketHandler();
