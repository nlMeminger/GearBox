/**
 * USB Handler for Carlinkit Dongle Communication
 * Handles WebUSB API interactions with automatic detection
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
    }

    /**
     * Check if WebUSB is supported in this browser
     */
    isWebUSBSupported() {
        return 'usb' in navigator;
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

            await this.connectToDevice(device);
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
                await this.connectToDevice(carlinkit);
            }

            return carlinkit;
        } catch (error) {
            console.error('Error finding USB device:', error);
            return null;
        }
    }

    /**
     * Connect to a specific USB device
     */
    async connectToDevice(device) {
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

            // Dispatch connection event
            window.dispatchEvent(new CustomEvent('carlinkit-connected', {
                detail: { device: this.device }
            }));

            // Start reading data
            this.startReading();

            return device;
        } catch (error) {
            console.error('Error connecting to device:', error);
            this.device = null;
            this.isConnected = false;
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
                
                // Dispatch disconnection event
                window.dispatchEvent(new CustomEvent('carlinkit-disconnected'));
                
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
        
        // Dispatch custom event with the received data
        window.dispatchEvent(new CustomEvent('usb-data-received', {
            detail: { data: data }
        }));
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
            manufacturerName: this.device.manufacturerName,
            productName: this.device.productName,
            serialNumber: this.device.serialNumber
        };
    }
}

// Create global instance
const usbHandler = new USBHandler();