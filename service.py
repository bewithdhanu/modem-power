import logging
import threading
import sys

from flask import Flask, jsonify

from modem import automateModem, restartModem, turnOffDeviceByInternetCheck
from speaker import turnOnSpeaker

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/service.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

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


@app.route('/turn-off-device', methods=['GET'])
def turn_off_device():
    """
    Turn off the device by checking internet connectivity.
    Only turns off if internet is available (meaning we're connected to modem).
    """
    result = turnOffDeviceByInternetCheck()
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
