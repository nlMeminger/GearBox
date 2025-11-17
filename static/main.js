/**
 * Main Application Logic
 */

// DOM Elements
const detectBtn = document.getElementById('detect-btn');
const disconnectBtn = document.getElementById('disconnect-btn');
const dongleStatus = document.getElementById('dongle-status');
const deviceInfoSection = document.getElementById('device-info-section');
const carplaySection = document.getElementById('carplay-section');
const communicationSection = document.getElementById('communication-section');
const deviceInfo = document.getElementById('device-info');
const logBox = document.getElementById('log');
const clearLogBtn = document.getElementById('clear-log-btn');
const startCarplayBtn = document.getElementById('start-carplay-btn');
const stopCarplayBtn = document.getElementById('stop-carplay-btn');

// Initialize video handler
const videoHandler = new CarPlayVideoHandler();

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    addLog('Application started');
    
    // Initialize video player
    try {
        videoHandler.initializeVideoPlayer('carplay-video');
        addLog('Video player initialized');
    } catch (error) {
        addLog(`Failed to initialize video player: ${error.message}`, 'error');
    }
});

/**
 * Detect and connect to Carlinkit dongle
 */
detectBtn.addEventListener('click', async () => {
    try {
        addLog('Requesting USB device...');
        const device = await requestDevice();
        
        if (device) {
            addLog('Device selected, connecting...');
            const connected = await connectToDevice(device);
            
            if (connected) {
                addLog('Successfully connected to dongle!', 'success');
                updateDongleStatus(true);
                displayDeviceInfo(device);
                
                // Set device for video handler
                videoHandler.setDevice(device);
                
                // Show CarPlay section
                carplaySection.style.display = 'block';
                
                // Emit to server
                socketHandler.emit('dongle_connected', {
                    vendorId: device.vendorId,
                    productId: device.productId
                });
            }
        }
    } catch (error) {
        addLog(`Error: ${error.message}`, 'error');
        console.error('Detection error:', error);
    }
});

/**
 * Start CarPlay video streaming
 */
startCarplayBtn.addEventListener('click', async () => {
    try {
        addLog('Starting CarPlay interface...');
        await videoHandler.startVideoStream();
        
        startCarplayBtn.style.display = 'none';
        stopCarplayBtn.style.display = 'inline-block';
        
        addLog('CarPlay streaming started!', 'success');
        socketHandler.emit('carplay_started', {});
    } catch (error) {
        addLog(`Failed to start CarPlay: ${error.message}`, 'error');
    }
});

/**
 * Stop CarPlay video streaming
 */
stopCarplayBtn.addEventListener('click', () => {
    addLog('Stopping CarPlay interface...');
    videoHandler.stopVideoStream();
    
    stopCarplayBtn.style.display = 'none';
    startCarplayBtn.style.display = 'inline-block';
    
    addLog('CarPlay streaming stopped');
    socketHandler.emit('carplay_stopped', {});
});

/**
 * Disconnect from dongle
 */
disconnectBtn.addEventListener('click', async () => {
    try {
        addLog('Disconnecting from dongle...');
        
        // Stop video streaming first
        videoHandler.stopVideoStream();
        
        await disconnectDevice();
        updateDongleStatus(false);
        addLog('Disconnected from dongle');
        
        carplaySection.style.display = 'none';
        startCarplayBtn.style.display = 'inline-block';
        stopCarplayBtn.style.display = 'none';
        
        socketHandler.emit('dongle_disconnected', {});
    } catch (error) {
        addLog(`Disconnect error: ${error.message}`, 'error');
    }
});

/**
 * Clear log
 */
clearLogBtn.addEventListener('click', () => {
    logBox.innerHTML = '<p class="log-entry">Log cleared</p>';
});

/**
 * Handle command buttons
 */
document.querySelectorAll('[data-command]').forEach(btn => {
    btn.addEventListener('click', async () => {
        const command = btn.dataset.command;
        addLog(`Sending command: ${command}`);
        
        try {
            await sendCommand(command);
            addLog(`Command "${command}" sent successfully`, 'success');
        } catch (error) {
            addLog(`Failed to send command: ${error.message}`, 'error');
        }
    });
});

/**
 * Update server connection status
 */
function updateServerStatus(connected) {
    const statusElement = document.getElementById('connection-status');
    const statusText = statusElement.querySelector('.status-text');
    
    statusElement.className = connected ? 'status connected' : 'status disconnected';
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
        carplaySection.style.display = 'none';
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

// Listen for socket events
socketHandler.on('connect', () => {
    updateServerStatus(true);
    addLog('Connected to server', 'success');
});

socketHandler.on('disconnect', () => {
    updateServerStatus(false);
    addLog('Disconnected from server', 'error');
});

socketHandler.on('usb_data', (data) => {
    addLog(`Received: ${JSON.stringify(data)}`);
});

// Handle device disconnection
window.addEventListener('beforeunload', () => {
    videoHandler.destroy();
});
