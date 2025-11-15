# CarPlay Dongle Manager - Flask + WebUSB

A Python Flask application with WebUSB frontend for detecting and communicating with Carlinkit CarPlay dongles.

## Features

- 🔌 WebUSB integration for direct browser-to-USB communication
- 🌐 Real-time WebSocket communication between frontend and backend
- 🚗 Automatic Carlinkit dongle detection
- 📡 Bidirectional data streaming
- 📝 Activity logging
- 🎨 Modern, responsive UI

## Requirements

- Python 3.8+
- Chrome, Edge, or Opera browser (WebUSB support)
- HTTPS connection (required for WebUSB)

## Installation

1. **Clone or download this project**

2. **Create a virtual environment (recommended)**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

## Running the Application

### Development Mode (Self-Signed Certificate)

```bash
python app.py
```

The app will automatically generate a self-signed SSL certificate and run on `https://localhost:5000`

**Important:** Your browser will show a security warning. Click "Advanced" → "Proceed to localhost" to continue.

### Production Mode (Proper SSL Certificate)

1. Obtain SSL certificate and key (e.g., from Let's Encrypt)

2. Modify `app.py` to use your certificates:
```python
socketio.run(app, 
             host='0.0.0.0', 
             port=5000,
             ssl_context=('path/to/cert.pem', 'path/to/key.pem'))
```

## Usage

1. **Open the application**
   - Navigate to `https://localhost:5000` in Chrome, Edge, or Opera

2. **Connect to Carlinkit dongle**
   - Plug in your Carlinkit dongle via USB
   - Click "Detect Carlinkit Dongle" button
   - Select your device from the browser popup
   - Grant USB permissions when prompted

3. **View device information**
   - Once connected, device details will be displayed
   - Activity log shows real-time communication events

4. **Send commands**
   - Use the command buttons to interact with the dongle
   - Commands are sent via WebUSB to the device

## Project Structure

```
carplay-flask/
├── app.py                  # Flask application & WebSocket handlers
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html         # Main HTML template
└── static/
    ├── css/
    │   └── style.css      # Styling
    └── js/
        ├── usb-handler.js     # WebUSB communication logic
        ├── socket-handler.js  # WebSocket communication logic
        └── main.js            # Application coordination
```

## USB Device IDs

The application is configured to detect Carlinkit dongles with:
- **Vendor ID:** `0x1314` (4884)
- **Product IDs:** `0x1520` (5408), `0x1521` (5409)

## WebUSB Requirements

WebUSB requires:
- **HTTPS connection** (or localhost)
- **Supported browser** (Chrome, Edge, Opera)
- **User permission** (browser will prompt)

## Troubleshooting

### "WebUSB not supported" error
- Use Chrome, Edge, or Opera browser
- Ensure you're accessing via HTTPS

### Device not detected
- Check USB cable connection
- Try a different USB port
- Ensure device is Carlinkit dongle
- Check browser console for errors

### Certificate errors
- Accept self-signed certificate in browser
- For production, use proper SSL certificate

### WebSocket connection fails
- Check if Flask server is running
- Verify HTTPS connection
- Check browser console for errors

## Development

### Modifying USB Communication

Edit `static/js/usb-handler.js` to change:
- Device filters (vendor/product IDs)
- Data parsing logic
- Endpoint configuration

### Modifying WebSocket Events

Edit `app.py` to add server-side event handlers:
```python
@socketio.on('your_event')
def handle_your_event(data):
    # Process data
    emit('response_event', {'result': 'success'})
```

Edit `static/js/socket-handler.js` to handle client-side events.

### Adding New Commands

1. Add button in `templates/index.html`
2. Add event listener in `static/js/main.js`
3. Handle command in `app.py`

## Security Notes

- Change `SECRET_KEY` in `app.py` for production
- Use proper SSL certificates for production
- Validate all data received from USB devices
- Implement authentication if exposing publicly

## License

This project is provided as-is for educational purposes.

## Credits

Based on the architecture of [react-carplay](https://github.com/rhysmorgan134/react-carplay)
