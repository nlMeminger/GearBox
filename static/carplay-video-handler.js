/**
 * CarPlay Video Handler
 * Handles video streaming from Carlinkit dongle
 */

class CarPlayVideoHandler {
    constructor() {
        this.device = null;
        this.videoElement = null;
        this.jmuxer = null;
        this.isStreaming = false;
        this.transferInEndpoint = null;
    }

    /**
     * Initialize video player with jMuxer for H.264 playback
     */
    initializeVideoPlayer(videoElementId) {
        this.videoElement = document.getElementById(videoElementId);
        
        if (!this.videoElement) {
            throw new Error(`Video element ${videoElementId} not found`);
        }

        // Initialize jMuxer for H.264 video decoding
        this.jmuxer = new JMuxer({
            node: videoElementId,
            mode: 'video',
            maxDelay: 100,
            fps: 60,
            flushingTime: 100,
            debug: false
        });

        console.log('Video player initialized');
    }

    /**
     * Set the USB device for video streaming
     */
    setDevice(device) {
        this.device = device;
        this.findVideoEndpoint();
    }

    /**
     * Find the bulk IN endpoint for video data
     * Typically endpoint 2 or 3 for Carlinkit devices
     */
    findVideoEndpoint() {
        if (!this.device) return;

        // Carlinkit devices typically have video on interface 0 or 1
        const configuration = this.device.configurations[0];
        
        for (const iface of configuration.interfaces) {
            for (const alt of iface.alternates) {
                // Look for bulk IN endpoints
                for (const endpoint of alt.endpoints) {
                    if (endpoint.direction === 'in' && endpoint.type === 'bulk') {
                        // Video endpoint is usually the largest bulk IN
                        if (endpoint.packetSize >= 512) {
                            this.transferInEndpoint = endpoint.endpointNumber;
                            console.log(`Found video endpoint: ${this.transferInEndpoint}`);
                            return;
                        }
                    }
                }
            }
        }
    }

    /**
     * Start video streaming from dongle
     */
    async startVideoStream() {
        if (!this.device || !this.jmuxer) {
            throw new Error('Device and video player must be initialized first');
        }

        if (this.isStreaming) {
            console.log('Already streaming');
            return;
        }

        this.isStreaming = true;
        console.log('Starting video stream...');

        // Start reading video data in a loop
        this.readVideoLoop();
    }

    /**
     * Continuously read video data from USB endpoint
     */
    async readVideoLoop() {
        while (this.isStreaming && this.device) {
            try {
                // Read from bulk IN endpoint (typically endpoint 2 or 3)
                const result = await this.device.transferIn(
                    this.transferInEndpoint || 2, 
                    65536 // Buffer size for video data
                );

                if (result.status === 'ok' && result.data) {
                    this.processVideoData(result.data);
                }
            } catch (error) {
                console.error('Error reading video data:', error);
                
                // If device is disconnected, stop streaming
                if (error.message?.includes('disconnected')) {
                    this.stopVideoStream();
                    break;
                }
                
                // Small delay before retry
                await new Promise(resolve => setTimeout(resolve, 10));
            }
        }
    }

    /**
     * Process incoming video data
     * Video data typically has a header with duration followed by H.264 NAL units
     */
    processVideoData(data) {
        const uint8Array = new Uint8Array(data.buffer);
        
        // Parse the data structure
        // First 4 bytes are usually duration in milliseconds (little-endian)
        const dataView = new DataView(data.buffer);
        const duration = dataView.getUint32(0, true);
        
        // Rest is H.264 video data
        const videoData = uint8Array.subarray(4);

        // Feed to jMuxer
        if (videoData.length > 0) {
            this.jmuxer.feed({
                video: videoData,
                duration: duration
            });
        }
    }

    /**
     * Stop video streaming
     */
    stopVideoStream() {
        this.isStreaming = false;
        console.log('Video stream stopped');
    }

    /**
     * Clean up resources
     */
    destroy() {
        this.stopVideoStream();
        
        if (this.jmuxer) {
            this.jmuxer.destroy();
            this.jmuxer = null;
        }
        
        this.device = null;
        this.videoElement = null;
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CarPlayVideoHandler;
}
