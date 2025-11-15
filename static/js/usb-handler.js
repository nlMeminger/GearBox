/**
 * USB Handler for Carlinkit Dongle Communication
 * Handles WebUSB API interactions
 */

class USBHandler {
    constructor() {
        // Carlinkit dongle USB identifiers
        this.VENDOR_ID = 0x1314;  // 4884 in decimal
        this.PRODUCT_IDS = [0x1520, 0x1521];  // 5408, 5409 in decimal
        
        this.device = null;
        this.interfaceNumber = 0;
        this.endpointIn = null;
        this.endpointOut = null;
        this.isConnected = false;
        
        // Setup USB connection/disconnection listeners
        this.setupUSBListeners();
    }

    /**
     * Check if WebUSB is supported in this browser
     */
    isWebUSBSupported() {
        return 'usb' in navigator;
    }

    /**
     * Setup listeners for USB device connection/disconnection
     */
    setupUSBListeners() {
        if (!this.isWebUSBSupported()) {
            console.warn('WebUSB not supported in this browser');
            return;
        }

        navigator.usb.addEventListener('connect', (event) => {
            console.log('USB device connected:', event.device);
            this.handleDeviceConnected(event.device);
        });

        navigator.usb.addEventListener('disconnect', (event) => {
            console.log('USB device disconnected:', event.device);
            this.handleDeviceDisconnected(event.device);
        });
    }

    /**
     * Request user to select a Carlinkit dongle
     */
    async requestDevice() {
        if (!this.isWebUSBSupported()) {
            throw new Error('WebUSB is not supported in this browser. Please use Chrome, Edge, or Opera.');
        }

        try {
            // Request device with Carlinkit filters
            const device = await navigator.usb.requestDevice({
                filters: [
                    { vendorId: this.VENDOR_ID, productId: this.PRODUCT_IDS[0] },
                    { vendorId: this.VENDOR_ID, productId: this.PRODUCT_IDS[1] }
                ]
            });

            await this.connect(device);
            return device;
        } catch (error) {
            console.error('Error requesting USB device:', error);
            throw error;
        }
    }

    /**
     * Find an already-paired Carlinkit dongle
     */
    async findDevice() {
        if (!this.isWebUSBSupported()) {
            return null;
        }

        try {
            const devices = await navigator.usb.getDevices();
            const carlinkit = devices.find(device => 
                device.vendorId === this.VENDOR_ID && 
                this.PRODUCT_IDS.includes(device.productId)
            );

            if (carlinkit) {
                await this.connect(carlinkit);
            }

            return carlinkit;
        } catch (error) {
            console.error('Error finding USB device:', error);
            return null;
        }
    }

    /**
     * Connect to a USB device
     */
    async connect(device) {
        try {
            this.device = device;

            // Open the device
            await device.open();
            console.log('Device opened:', device);

            // Select configuration (usually configuration 1)
            if (device.configuration === null) {
                await device.selectConfiguration(1);
            }

            // Claim the interface
            await device.claimInterface(this.interfaceNumber);
            console.log('Interface claimed:', this.interfaceNumber);

            // Find endpoints
            const iface = device.configuration.interfaces[this.interfaceNumber];
            const alternate = iface.alternate;

            // Find IN and OUT endpoints
            for (const endpoint of alternate.endpoints) {
                if (endpoint.direction === 'in') {
                    this.endpointIn = endpoint.endpointNumber;
                } else if (endpoint.direction === 'out') {
                    this.endpointOut = endpoint.endpointNumber;
                }
            }

            this.isConnected = true;
            console.log('USB device connected successfully');
            console.log('Endpoint IN:', this.endpointIn, 'Endpoint OUT:', this.endpointOut);

            // Start reading data
            this.startReading();

            return device;
        } catch (error) {
            console.error('Error connecting to device:', error);
            throw error;
        }
    }

    /**
     * Disconnect from the device
     */
    async disconnect() {
        if (this.device) {
            try {
                await this.device.releaseInterface(this.interfaceNumber);
                await this.device.close();
                this.isConnected = false;
                this.device = null;
                console.log('Device disconnected');
            } catch (error) {
                console.error('Error disconnecting:', error);
            }
        }
    }

    /**
     * Start reading data from the device
     */
    async startReading() {
        while (this.isConnected && this.device) {
            try {
                // Read data from IN endpoint
                const result = await this.device.transferIn(this.endpointIn, 64);
                
                if (result.data && result.data.byteLength > 0) {
                    this.handleDataReceived(result.data);
                }
            } catch (error) {
                if (this.isConnected) {
                    console.error('Error reading from device:', error);
                }
                break;
            }
        }
    }

    /**
     * Send data to the device
     */
    async sendData(data) {
        if (!this.isConnected || !this.device) {
            throw new Error('Device not connected');
        }

        try {
            // Convert data to Uint8Array if needed
            let buffer;
            if (data instanceof Uint8Array) {
                buffer = data;
            } else if (typeof data === 'string') {
                buffer = new TextEncoder().encode(data);
            } else {
                buffer = new Uint8Array(data);
            }

            await this.device.transferOut(this.endpointOut, buffer);
            console.log('Data sent to device:', buffer);
        } catch (error) {
            console.error('Error sending data:', error);
            throw error;
        }
    }

    /**
     * Handle data received from device
     */
    handleDataReceived(data) {
        console.log('Data received from device:', data);
        
        // Convert to array for easier handling
        const dataArray = new Uint8Array(data.buffer);
        
        // Notify via custom event
        window.dispatchEvent(new CustomEvent('usb-data-received', {
            detail: { data: dataArray }
        }));
    }

    /**
     * Handle device connected event
     */
    handleDeviceConnected(device) {
        if (device.vendorId === this.VENDOR_ID && 
            this.PRODUCT_IDS.includes(device.productId)) {
            
            window.dispatchEvent(new CustomEvent('carlinkit-connected', {
                detail: { device }
            }));
        }
    }

    /**
     * Handle device disconnected event
     */
    handleDeviceDisconnected(device) {
        if (this.device && device.serialNumber === this.device.serialNumber) {
            this.isConnected = false;
            this.device = null;
            
            window.dispatchEvent(new CustomEvent('carlinkit-disconnected', {
                detail: { device }
            }));
        }
    }

    /**
     * Get device information
     */
    getDeviceInfo() {
        if (!this.device) {
            return null;
        }

        return {
            vendorId: this.device.vendorId,
            productId: this.device.productId,
            serialNumber: this.device.serialNumber,
            manufacturerName: this.device.manufacturerName,
            productName: this.device.productName,
            isConnected: this.isConnected
        };
    }
}

// Create global instance
window.usbHandler = new USBHandler();
