/**
 * Main Application Logic
 * Coordinates USB and Socket handlers
 */

// DOM elements
const detectBtn = document.getElementById('detect-btn');
const disconnectBtn = document.getElementById('disconnect-btn');
const dongleStatus = document.getElementById('dongle-status');
const deviceInfoSection = document.getElementById('device-info-section');
const deviceInfo = document.getElementById('device-info');
const communicationSection = document.getElementById('communication-section');
const connectionStatus = document.getElementById('connection-status');
const logBox = document.getElementById('log');
const clearLogBtn = document.getElementById('clear-log-btn');

// Initialize handlers when page loads
window.addEventListener('DOMContentLoaded', () => {
    // Connect to WebSocket server
    socketHandler.connect();

    // Setup button listeners
    detectBtn.addEventListener('click', handleDetectClick);
    disconnectBtn.addEventListener('click', handleDisconnectClick);
    clearLogBtn.addEventListener('click', () => {
        logBox.innerHTML = '';
        addLog('Log cleared');
    });

    // Setup command button listeners
    document.querySelectorAll('.command-controls .btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const command = e.target.dataset.command;
            handleCommandClick(command);
        });
    });

    // Listen for USB events
    setupUSBEventListeners();

    // Listen for Socket events
    setupSocketEventListeners();

    // Check for already connected devices
    checkExistingDevice();

    addLog('Application initialized');
});

/**
 * Setup USB event listeners
 */
function setupUSBEventListeners() {
    window.addEventListener('carlinkit-connected', (e) => {
        addLog('Carlinkit dongle connected!', 'success');
        updateDongleStatus(true);
    });

    window.addEventListener('carlinkit-disconnected', (e) => {
        addLog('Carlinkit dongle disconnected', 'warning');
        updateDongleStatus(false);
        socketHandler.emitDongleDisconnected();
    });

    window.addEventListener('usb-data-received', (e) => {
        const data = e.detail.data;
        addLog(`Received USB data: ${data.length} bytes`);
        socketHandler.sendUSBData(data);
    });
}

/**
 * Setup Socket event listeners
 */
function setupSocketEventListeners() {
    window.addEventListener('socket-connection-status', (e) => {
        const connected = e.detail.connected;
        updateConnectionStatus(connected);
        addLog(connected ? 'Connected to server' : 'Disconnected from server', 
               connected ? 'success' : 'error');
    });

    window.addEventListener('server-dongle-status', (e) => {
        addLog(`Server acknowledged dongle status: ${e.detail.connected ? 'connected' : 'disconnected'}`);
    });

    window.addEventListener('server-usb-response', (e) => {
        addLog(`Server response: ${e.detail.status}`);
    });

    window.addEventListener('server-send-command', async (e) => {
        const command = e.detail.command;
        addLog(`Server requests command: ${command}`);
        try {
            await sendCommandToDongle(command);
        } catch (error) {
            addLog(`Error sending command: ${error.message}`, 'error');
        }
    });
}

/**
 * Handle detect button click
 */
async function handleDetectClick() {
    if (!usbHandler.isWebUSBSupported()) {
        addLog('WebUSB not supported. Please use Chrome, Edge, or Opera on HTTPS.', 'error');
        alert('WebUSB is not supported in this browser.\n\nPlease use:\n- Chrome\n- Edge\n- Opera\n\nAnd ensure you\'re using HTTPS.');
        return;
    }

    try {
        detectBtn.disabled = true;
        detectBtn.textContent = 'Connecting...';
        addLog('Requesting USB device...');

        const device = await usbHandler.requestDevice();
        
        if (device) {
            addLog('Device connected successfully!', 'success');
            updateDongleStatus(true);
            displayDeviceInfo(usbHandler.getDeviceInfo());
            
            // Notify server
            socketHandler.emitDongleConnected(usbHandler.getDeviceInfo());
        }
    } catch (error) {
        addLog(`Error: ${error.message}`, 'error');
        console.error(error);
    } finally {
        detectBtn.disabled = false;
        detectBtn.textContent = 'Detect Carlinkit Dongle';
    }
}

/**
 * Handle disconnect button click
 */
async function handleDisconnectClick() {
    try {
        await usbHandler.disconnect();
        addLog('Device disconnected', 'warning');
        updateDongleStatus(false);
        socketHandler.emitDongleDisconnected();
    } catch (error) {
        addLog(`Error disconnecting: ${error.message}`, 'error');
    }
}

/**
 * Handle command button click
 */
function handleCommandClick(command) {
    addLog(`Sending command: ${command}`);
    socketHandler.sendCommand(command);
}

/**
 * Send command directly to dongle
 */
async function sendCommandToDongle(command) {
    if (!usbHandler.isConnected) {
        throw new Error('Device not connected');
    }

    // Convert command to bytes (this is simplified - actual protocol may differ)
    const encoder = new TextEncoder();
    const data = encoder.encode(command);
    
    await usbHandler.sendData(data);
    addLog(`Sent command to dongle: ${command}`, 'success');
}

/**
 * Check for existing device on page load
 */
async function checkExistingDevice() {
    try {
        const device = await usbHandler.findDevice();
        if (device) {
            addLog('Found existing paired device', 'success');
            updateDongleStatus(true);
            displayDeviceInfo(usbHandler.getDeviceInfo());
            socketHandler.emitDongleConnected(usbHandler.getDeviceInfo());
        }
    } catch (error) {
        console.error('Error checking for existing device:', error);
    }
}

/**
 * Update connection status display
 */
function updateConnectionStatus(connected) {
    const statusText = connectionStatus.querySelector('.status-text');
    connectionStatus.classList.toggle('connected', connected);
    connectionStatus.classList.toggle('disconnected', !connected);
    statusText.textContent = connected ? 'Server Connected' : 'Server Disconnected';
}

/**
 * Update dongle status display
 */
function updateDongleStatus(connected) {
    if (connected) {
        dongleStatus.innerHTML = '<p class="success">✓ Carlinkit dongle detected and connected!</p>';
        deviceInfoSection.style.display = 'block';
        communicationSection.style.display = 'block';
        detectBtn.style.display = 'none';
    } else {
        dongleStatus.innerHTML = '<p>No dongle detected</p>';
        deviceInfoSection.style.display = 'none';
        communicationSection.style.display = 'none';
        detectBtn.style.display = 'block';
    }
}

/**
 * Display device information
 */
function displayDeviceInfo(info) {
    if (!info) return;

    deviceInfo.innerHTML = `
        <div class="info-row"><strong>Vendor ID:</strong> 0x${info.vendorId.toString(16).padStart(4, '0')}</div>
        <div class="info-row"><strong>Product ID:</strong> 0x${info.productId.toString(16).padStart(4, '0')}</div>
        <div class="info-row"><strong>Manufacturer:</strong> ${info.manufacturerName || 'N/A'}</div>
        <div class="info-row"><strong>Product:</strong> ${info.productName || 'N/A'}</div>
        <div class="info-row"><strong>Serial Number:</strong> ${info.serialNumber || 'N/A'}</div>
    `;
}

/**
 * Add log entry
 */
function addLog(message, type = 'info') {
    const timestamp = new Date().toLocaleTimeString();
    const entry = document.createElement('p');
    entry.className = `log-entry ${type}`;
    entry.textContent = `[${timestamp}] ${message}`;
    logBox.appendChild(entry);
    logBox.scrollTop = logBox.scrollHeight;
}
