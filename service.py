import logging
import threading
import sys
from datetime import datetime
import os

from flask import Flask, jsonify

from modem import automateModem, restartModem, turnOffCharger, turnOnCharger
from speaker import turnOnSpeaker

# Configure logging
# Clear any existing handlers to ensure fresh configuration
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create log filename with current date
current_date = datetime.now().strftime('%Y-%m-%d')
log_filename = f'logs/service_{current_date}.log'

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

# Create file handler with append mode
file_handler = logging.FileHandler(log_filename, mode='a')
file_handler.setFormatter(formatter)

# Create console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

# Configure root logger
logging.root.setLevel(logging.INFO)
logging.root.addHandler(file_handler)
logging.root.addHandler(console_handler)

app = Flask(__name__)


@app.route('/turn-on-speaker', methods=['GET'])
def turn_on_speaker():
    turnOnSpeaker()
    return jsonify({
        "status": "success",
        "message": "Speaker turned on"
    })


@app.route('/automate-modem', methods=['GET'])
def automate_modem():
    result = automateModem()
    return jsonify(result)


@app.route('/restart-modem', methods=['GET'])
def restart_modem():
    restartModem()
    return jsonify([])


@app.route('/turn-off-charger', methods=['GET'])
def turn_off_charger():
    result = turnOffCharger()
    return jsonify(result)

@app.route('/turn-on-charger', methods=['GET'])
def turn_on_charger():
    result = turnOnCharger()
    return jsonify(result)


@app.route('/', methods=['GET'])
def main():
    return jsonify({
        "status": "success",
        "message": "Hello Dhanu!"
    })


if __name__ == '__main__':
    # Start the background task in a separate thread
    app.run(port=8765)
