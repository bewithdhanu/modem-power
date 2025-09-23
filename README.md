
# ModemPower - Airtel Modem Control with Tuya Smart Plug

![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)

## Overview

ModemPower is an intelligent modem management system that automatically controls your Airtel modem using a Tuya Smart Plug. It monitors battery levels, manages power consumption, and provides automated control through a web API and scheduled tasks.

## Features

- **🔋 Battery Monitoring**: Automatically checks modem battery levels via local network
- **⚡ Smart Power Management**: Automatically turns off modem when battery > 80%, turns on when < 20%
- **🌐 Web API**: RESTful API endpoints for remote control
- **⏰ Automated Scheduling**: Cron jobs for continuous monitoring and control
- **🔌 Tuya Integration**: Seamless control via Tuya Smart Plug
- **📱 Cross-Platform**: Works on macOS and Linux
- **🛡️ Internet Connectivity Check**: Only operates when connected to modem network

## Prerequisites

Before you get started, ensure you have the following:

- **Airtel Modem**: Compatible with local network access (192.168.1.1)
- **Tuya Smart Plug**: Connected to your network and configured
- **Tuya IoT Platform Account**: For API access
- **Python 3.x**: Installed on your system
- **macOS or Linux**: For cron job support

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/bewithdhanu/ModemPower.git
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

2. **Update `env.py` with your credentials:**
   ```python
   ACCESS_ID = "your_tuya_access_id"
   ACCESS_KEY = "your_tuya_access_key"
   USERNAME = "your_tuya_username"
   PASSWORD = "your_tuya_password"
   DEVICE_ID = "your_tuya_device_id"
   ENDPOINT = "https://openapi.tuyain.com"
   MODEM_WIFI_NAME = "airtel_coconut_ufi_169B9E"  # Your modem's WiFi name
   ```

## Usage

### Manual Usage

1. **Start the Flask service:**
   ```bash
   source venv/bin/activate
   python service.py
   ```

2. **Access the web interface:**
   - Open your browser and go to `http://127.0.0.1:5000`

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page |
| `/automate-modem` | GET | Run modem automation (check battery, turn on/off) |
| `/turn-off-device` | GET | Turn off device (with internet connectivity check) |
| `/restart-modem` | GET | Restart the modem |
| `/turn-on-speaker` | GET | Turn on speaker device |

### Automated Usage (Cron Jobs)

Set up automated tasks using the provided scripts:

1. **Setup all cron jobs:**
   ```bash
   ./scripts/manage_cron.sh setup
   ```

2. **Check status:**
   ```bash
   ./scripts/manage_cron.sh status
   ```

3. **Remove cron jobs:**
   ```bash
   ./scripts/manage_cron.sh remove
   ```

### Cron Job Schedule

The system automatically sets up the following cron jobs:

- **@reboot**: Start Flask service on system startup
- **@reboot + 30s**: Turn off device on system startup
- **Every 5 minutes**: Run modem automation (check battery, manage power)
- **Daily at 23:59**: Turn off device before sleep
- **Daily at 2:00 AM**: Restart service to ensure it keeps running

### Scripts Overview

| Script | Purpose |
|--------|---------|
| `scripts/setup_cron.sh` | Set up all cron jobs |
| `scripts/manage_cron.sh` | Manage cron jobs (setup/status/remove) |
| `scripts/start_service.sh` | Start Flask service in background |
| `scripts/turn_off_device.sh` | Turn off device via API |
| `scripts/automate_modem.sh` | Run modem automation via API |

### Logs

- **Cron logs**: `logs/cron.log`
- **Service logs**: `logs/service.log`

## Troubleshooting

### Common Issues

1. **Service not starting:**
   ```bash
   # Check if service is running
   ./scripts/manage_cron.sh status
   
   # Start service manually
   ./scripts/manage_cron.sh start-service
   ```

2. **Cron jobs not working:**
   ```bash
   # Check cron jobs
   crontab -l
   
   # Re-setup cron jobs
   ./scripts/manage_cron.sh setup
   ```

3. **Internet connectivity issues:**
   - Ensure you're connected to the modem's WiFi network
   - Check if the modem is accessible at `192.168.1.1`

4. **Tuya API errors:**
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

## File Structure

```
ModemPower/
├── scripts/                 # Automation scripts
│   ├── setup_cron.sh       # Set up cron jobs
│   ├── manage_cron.sh      # Manage cron jobs
│   ├── start_service.sh    # Start Flask service
│   ├── turn_off_device.sh  # Turn off device
│   └── automate_modem.sh   # Run automation
├── logs/                   # Log files
│   ├── cron.log           # Cron job logs
│   └── service.log        # Service logs
├── device.py              # Tuya device control
├── modem.py               # Modem management
├── service.py             # Flask web service
├── env.py                 # Configuration
└── requirements.txt       # Dependencies
```

## Security Notes

- Keep your `env.py` file secure and never commit it to version control
- The service runs on localhost (127.0.0.1) by default
- All API calls are made over your local network
- Tuya credentials are stored locally and encrypted by the Tuya SDK

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