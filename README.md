
# ModemPower 🔋 - Airtel Modem Control with Tuya Smart Plug

![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)

## Overview

ModemPower is an intelligent modem management system that automatically controls your Airtel modem using a Tuya Smart Plug. It monitors battery levels, manages power consumption, and provides automated control through a web API and scheduled tasks.

## Features

- **🔋 Battery Monitoring**: Automatically checks modem battery levels via local network
- **⚡ Smart Power Management**: Automatically turns off modem when battery > 80%, turns on when < 20%
- **🌐 FastAPI**: Modern RESTful API with automatic Swagger UI documentation
- **⏰ Simple Cron Scheduling**: Uses standard crontab for easy schedule management
- **🔌 Tuya Integration**: Seamless control via Tuya Smart Plug
- **🐳 Docker Support**: Easy deployment with Docker Compose
- **📱 Cross-Platform**: Works on macOS, Linux, and Windows
- **🛡️ Internet Connectivity Check**: Only operates when connected to modem network
- **📧 Email Notifications**: Sends email alerts when modem is unreachable

## Prerequisites

Before you get started, ensure you have the following:

- **Airtel Modem**: Compatible with local network access (192.168.1.1)
- **Tuya Smart Plug**: Connected to your network and configured
- **Tuya IoT Platform Account**: For API access
- **Python 3.x**: Installed on your system
- **macOS or Linux**: For cron job support

## Installation

### Option 1: Docker (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/bewithdhanu/modem-power.git
   cd ModemPower
   ```

2. **Configure environment:**
   ```bash
   cp env.example .env
   # Edit .env with your Tuya credentials and modem IP
   ```

3. **Start with Docker:**
   ```bash
   ./start.sh
   # Or manually: docker-compose up -d
   ```

### Option 2: Manual Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/bewithdhanu/modem-power.git
   cd ModemPower
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Copy environment file:**
   ```bash
   cp env.py.example env.py
   ```

2. **Update `.env` with your credentials:**
   ```bash
   ACCESS_ID=your_tuya_access_id
   ACCESS_KEY=your_tuya_access_key
   USERNAME=your_tuya_username
   PASSWORD=your_tuya_password
   DEVICE_ID=your_tuya_device_id
   ENDPOINT=https://openapi.tuyain.com
   MODEM_IP=192.168.1.1  # Your modem's IP address
   # Brevo email configuration:
   BREVO_API_KEY=your_brevo_api_key
   SENDER_EMAIL=your_email@example.com
   RECIPIENT_EMAIL=recipient@example.com
   TZ=Asia/Kolkata  # Indian timezone
   ```

## Usage


### Docker Usage (Recommended)

1. **Start services:**
   ```bash
   docker-compose up -d
   ```

2. **Access the API:**
   - Main API: `http://localhost:8765`
   - **Swagger UI**: `http://localhost:8765/docs` (Interactive API documentation)
   - **ReDoc**: `http://localhost:8765/redoc` (Alternative API documentation)

3. **View logs:**
   ```bash
   docker-compose logs -f
   ```

4. **Stop services:**
   ```bash
   docker-compose down
   ```

### Manual Usage

1. **Start the Flask service:**
   ```bash
   source venv/bin/activate
   python service.py
   ```

2. **Access the web interface:**
   - Open your browser and go to `http://127.0.0.1:8765`

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | **Redirects to Swagger UI** |
| `/docs` | GET | **Swagger UI** - Interactive API documentation |
| `/redoc` | GET | **ReDoc** - Alternative API documentation |
| `/automate-modem` | GET | Run modem automation (check battery, turn on/off) |
| `/turn-on-charger` | GET | Turn on charger (with modem reachability check) |
| `/turn-off-charger` | GET | Turn off charger |
| `/restart-modem` | GET | Restart the modem |

> **🎯 Pro Tip**: Visit `http://localhost:8765/docs` to see the interactive Swagger UI where you can test all endpoints directly from your browser!


## Troubleshooting

### Common Issues

1. **Internet connectivity issues:**
   - Ensure you're connected to the modem's WiFi network
   - Check if the modem is accessible at `192.168.1.1`

2. **Tuya API errors:**
   - Verify your credentials in `env.py`
   - Check if your Tuya subscription is active
   - Ensure device ID is correct

### Manual Testing

Test individual components:

```bash
# Test internet connectivity
python -c "from modem import is_wifi_connected; print('Connected:', is_wifi_connected())"

# Test battery reading
python -c "from modem import getBatteryPercent; print('Battery:', getBatteryPercent())"

# Test device control
python -c "from device import getStatus; print('Device status:', getStatus())"
```

## Docker Services

The Docker Compose setup includes two services:

1. **modem-power**: Flask web service running on port 8765
2. **cron**: Uses `willfarrell/crontab` image for simple scheduling:
   - Turn on modem every day at 1:00 PM
   - Check battery and auto-manage every 5 minutes
   - Standard crontab format for easy customization

### Network Configuration

The containers use **host networking** to access your router:
- Containers share the host's network interface
- Can directly access your modem at `192.168.1.1` (or configured IP)
- No port mapping needed for internal communication
- Flask service accessible at `http://localhost:8765`

### Simple Cron Scheduling

Edit the `crontab` file to customize schedules:

```bash
# Edit the crontab file
nano crontab

# Current default schedules:
# 0 13 * * * curl -s http://localhost:8765/turn-on-charger  # Daily 1PM
# */5 * * * * curl -s http://localhost:8765/automate-modem  # Every 5 minutes
```

**Cron Examples**:
- `0 13 * * *` - Every day at 1:00 PM
- `*/5 * * * *` - Every 5 minutes  
- `0 9 * * 1-5` - Weekdays at 9:00 AM
- `0 14 * * 0` - Every Sunday at 2:00 PM

### Brevo Email Service (Free & Easy)

When the modem is unreachable, the system will send you a beautiful HTML email notification via Brevo API.

#### Setup Brevo (2 minutes):
1. **Create free account**: Go to [brevo.com](https://brevo.com) and sign up
2. **Get API key**: Go to [API Keys](https://app.brevo.com/settings/keys/api) and create a new key
3. **Add to `.env`**:
   ```bash
   BREVO_API_KEY=your_brevo_api_key
   SENDER_EMAIL=your_email@example.com
   SENDER_NAME=ModemPower
   RECIPIENT_EMAIL=recipient@example.com
   RECIPIENT_NAME=Your Name
   ```

#### Why Brevo is Perfect:
- ✅ **Free**: 300 emails/day free forever
- ✅ **No SMTP**: Uses simple REST API
- ✅ **No passwords**: Just API key authentication
- ✅ **Beautiful emails**: HTML formatted notifications
- ✅ **Reliable**: Enterprise-grade email delivery
- ✅ **Easy setup**: 2 minutes to configure
- ✅ **No app passwords**: No complex authentication

## File Structure

```
ModemPower/
├── device.py              # Tuya device control
├── modem.py               # Modem management
├── service.py             # Flask web service
├── crontab                # Simple cron schedule file
├── env.py                 # Configuration (legacy)
├── env.example            # Environment template
├── docker-compose.yml     # Docker services configuration
├── Dockerfile             # Container definition
├── start.sh               # Startup script
└── requirements.txt       # Dependencies
```

## Security Notes

- Keep your `.env` file secure and never commit it to version control
- The service runs on localhost (127.0.0.1:8765) by default
- All API calls are made over your local network
- Tuya credentials are stored in environment variables
- Port 8765 is used to avoid conflicts with common services
- Docker containers run in isolated network environment

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Acknowledgments

- [Tuya Official Python SDK](https://github.com/tuya/tuya-iot-python-sdk)
- Flask web framework
- Airtel modem API

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors

|Name|Type|
|--|--|
|[Dhanu K](https://github.com/bewithdhanu)|Author|