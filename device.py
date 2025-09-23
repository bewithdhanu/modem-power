from env import ENDPOINT, ACCESS_ID, ACCESS_KEY, USERNAME, PASSWORD, DEVICE_ID

from tuya_iot import TuyaOpenAPI, TUYA_LOGGER
import logging

# Initialization of tuya openapi
openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect(USERNAME, PASSWORD, "86", 'smartlife')

# # Uncomment the following lines to see logs.

TUYA_LOGGER.setLevel(logging.DEBUG)


def turnOff():
    logging.info("Turning off modem")
    commands = {'commands': [{"code": "switch_1", "value": False}, {"code": "countdown_1", "value": 0}]}
    openapi.post('/v1.0/devices/{}/commands'.format(DEVICE_ID), commands)


def turnOn():
    logging.info("Turning on modem")
    commands = {'commands': [{"code": "switch_1", "value": True}, {"code": "countdown_1", "value": 0}]}
    openapi.post('/v1.0/devices/{}/commands'.format(DEVICE_ID), commands)


def getStatus():
    resource = openapi.get('/v1.0/devices/{}/status'.format(DEVICE_ID))
    # Parse the JSON response and get the data
    # response_data = resource.json()

    # Now 'response_data' contains the JSON data from the response
    # You can access specific data fields using dictionary notation
    # For example, if the response contains a 'status' field:
    commands = resource.get('result')
    if commands:
        for command in commands:
            if command['code'] == 'switch_1':
                return command['value']
    return False

