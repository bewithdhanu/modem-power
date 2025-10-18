import os

# Get environment variables with fallback to env.py for backward compatibility
try:
    from env import ENDPOINT, ACCESS_ID, ACCESS_KEY, USERNAME, PASSWORD, DEVICE_ID
except ImportError:
    ENDPOINT = os.getenv('ENDPOINT')
    ACCESS_ID = os.getenv('ACCESS_ID')
    ACCESS_KEY = os.getenv('ACCESS_KEY')
    USERNAME = os.getenv('USERNAME')
    PASSWORD = os.getenv('PASSWORD')
    DEVICE_ID = os.getenv('DEVICE_ID')

from tuya_iot import TuyaOpenAPI, TUYA_LOGGER
import logging

# Initialization of tuya openapi
openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect(USERNAME, PASSWORD, "86", 'smartlife')

# # Uncomment the following lines to see logs.

TUYA_LOGGER.setLevel(logging.DEBUG)


def turnOff():
    try:
        logging.info("Turning off modem")
        commands = {'commands': [{"code": "switch_1", "value": False}, {"code": "countdown_1", "value": 0}]}
        response = openapi.post('/v1.0/devices/{}/commands'.format(DEVICE_ID), commands)
        logging.info(f"Turn off response: {response}")
        return True
    except Exception as e:
        logging.error(f"Failed to turn off modem: {e}")
        return False


def turnOn():
    try:
        logging.info("Turning on modem")
        commands = {'commands': [{"code": "switch_1", "value": True}, {"code": "countdown_1", "value": 0}]}
        response = openapi.post('/v1.0/devices/{}/commands'.format(DEVICE_ID), commands)
        logging.info(f"Turn on response: {response}")
        return True
    except Exception as e:
        logging.error(f"Failed to turn on modem: {e}")
        return False


def getStatus():
    try:
        resource = openapi.get('/v1.0/devices/{}/status'.format(DEVICE_ID))
        commands = resource.get('result')
        if commands:
            for command in commands:
                if command['code'] == 'switch_1':
                    return command['value']
        return False
    except Exception as e:
        logging.error(f"Failed to get device status: {e}")
        return None

