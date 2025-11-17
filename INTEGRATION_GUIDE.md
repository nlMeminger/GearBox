# CarPlay Video Display Integration Guide

## Overview
This guide shows how to add CarPlay interface display to your GearBox Flask project.

## What You Need

### 1. Files to Add to Your Project

**JavaScript Files (in `static/js/`):**
- `carplay-video-handler.js` - Handles video streaming and H.264 decoding

**Updated Files:**
- `templates/index.html` - Add video element and jMuxer library
- `static/js/main.js` - Add video handler integration
- `static/css/style.css` - Add video section styling

### 2. External Dependencies

Add to your HTML `<head>`:
```html
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/jmuxer@2.0.3/dist/jmuxer.min.js"></script>
```

## How It Works

### Video Streaming Flow
```
iPhone/Dongle → USB Bulk Transfer → CarPlayVideoHandler → jMuxer → <video> element
```

### Key Components

1. **jMuxer Library**
   - Decodes H.264 video in browser
   - Handles MPEG-TS muxing
   - Renders to HTML5 video element

2. **CarPlayVideoHandler Class**
   - Manages USB video endpoint
   - Reads video data continuously
   - Parses video packets (4-byte duration + H.264 data)
   - Feeds data to jMuxer

3. **Video Data Format**
   ```
   [4 bytes: duration (little-endian)] [H.264 NAL units]
   ```

## Step-by-Step Integration

### Step 1: Copy Files
```bash
# In your GearBox project directory
cp carplay-video-handler.js static/js/
cp carplay-styles.css static/css/
```

### Step 2: Update Your HTML Template

Replace your `templates/index.html` with the updated version, or manually add:

```html
<!-- Add to video section -->
<section class="card" id="carplay-section" style="display: none;">
    <h2>CarPlay Display</h2>
    <div class="video-container">
        <video id="carplay-video" controls autoplay 
               style="width: 100%; max-width: 1280px; background: #000;">
        </video>
    </div>
    <div class="carplay-controls">
        <button id="start-carplay-btn" class="btn btn-success">Start CarPlay</button>
        <button id="stop-carplay-btn" class="btn btn-danger" style="display: none;">Stop CarPlay</button>
    </div>
</section>

<!-- Add before closing </body> -->
<script src="https://cdn.jsdelivr.net/npm/jmuxer@2.0.3/dist/jmuxer.min.js"></script>
<script src="{{ url_for('static', filename='js/carplay-video-handler.js') }}"></script>
```

### Step 3: Update main.js

Add after your existing initialization:

```javascript
// Initialize video handler
const videoHandler = new CarPlayVideoHandler();

// In DOMContentLoaded
videoHandler.initializeVideoPlayer('carplay-video');

// After successful device connection
videoHandler.setDevice(device);
carplaySection.style.display = 'block';

// Add button handlers
startCarplayBtn.addEventListener('click', async () => {
    await videoHandler.startVideoStream();
    startCarplayBtn.style.display = 'none';
    stopCarplayBtn.style.display = 'inline-block';
});

stopCarplayBtn.addEventListener('click', () => {
    videoHandler.stopVideoStream();
    stopCarplayBtn.style.display = 'none';
    startCarplayBtn.style.display = 'inline-block';
});
```

### Step 4: Update CSS

Add the video styles from `carplay-styles.css` to your `static/css/style.css`

## Configuration Options

### Video Endpoint Detection
The handler auto-detects the video endpoint (usually endpoint 2 or 3). If needed, manually specify:

```javascript
videoHandler.transferInEndpoint = 3; // Force endpoint 3
```

### Video Quality Settings
Adjust jMuxer configuration in `carplay-video-handler.js`:

```javascript
this.jmuxer = new JMuxer({
    node: videoElementId,
    mode: 'video',
    maxDelay: 100,      // Latency (ms)
    fps: 60,            // Target FPS
    flushingTime: 100,  // Buffer flush interval
    debug: false        // Enable debug logs
});
```

### Buffer Size
Adjust USB transfer buffer size for higher quality:

```javascript
const result = await this.device.transferIn(
    this.transferInEndpoint, 
    131072  // Increase from 65536 for 4K
);
```

## Troubleshooting

### No Video Appears
1. Check browser console for errors
2. Verify endpoint number: Try endpoints 2, 3, or 4
3. Check USB permissions
4. Ensure dongle is in CarPlay mode (phone connected)

### Video Stuttering/Lag
1. Increase buffer size
2. Adjust `maxDelay` and `flushingTime` in jMuxer
3. Check USB connection quality
4. Reduce FPS setting

### "Device disconnected" Errors
- USB cable issue
- Power supply insufficient
- Dongle needs reset

### Black Screen
- Phone not connected to dongle
- CarPlay not initialized on dongle
- Wrong video endpoint

## Testing

1. Start Flask server: `python app.py`
2. Open `https://localhost:5000`
3. Click "Detect Carlinkit Dongle"
4. Select device and grant permissions
5. Connect iPhone to dongle (CarPlay should start on phone)
6. Click "Start CarPlay" button
7. Video should appear in browser

## Advanced Features to Add Later

### Touch Input
Send touch events to dongle for interaction:
```javascript
// In CarPlayVideoHandler
async sendTouch(x, y, action) {
    // action: 0=down, 1=move, 2=up
    const touchData = new Uint8Array([/* touch command format */]);
    await this.device.transferOut(1, touchData);
}
```

### Audio Streaming
Capture and play audio from dongle:
```javascript
// Use Web Audio API
const audioContext = new AudioContext();
// Process audio packets from dongle
```

### Multi-Resolution Support
Dynamically adjust video based on screen size.

## Resources

- jMuxer docs: https://github.com/samirkumardas/jmuxer
- WebUSB API: https://developer.mozilla.org/en-US/docs/Web/API/USB
- react-carplay source: https://github.com/rhysmorgan134/react-carplay
- node-carplay: https://github.com/rhysmorgan134/node-carplay

## Next Steps

1. Test video streaming with your dongle
2. Add touch interaction for full CarPlay control
3. Implement audio streaming
4. Add error recovery and reconnection logic
5. Optimize for your target resolution/FPS
