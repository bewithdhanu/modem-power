import json
import logging
import subprocess
import time

import requests
import xmltodict

from device import getStatus, turnOff, turnOn


def getBatteryPercent():
    try:
        url = "http://192.168.1.1/mark_title.w.xml"

        payload = {}
        headers = {
            'Referer': 'http://192.168.1.1/index.html'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        # Parse the XML data to a Python dictionary
        xml_dict = xmltodict.parse(response.text)

        # Convert the dictionary to JSON
        json_data = json.dumps(xml_dict, indent=4)

        data_dict = json.loads(json_data)
        return int(data_dict['title']['batt_p'])
    except:
        return None


def restartModem():
    try:
        url = "http://192.168.1.1/wxml/set_reboot.xml"

        payload = "reboot=1"
        headers = {
            'Referer': 'http://192.168.1.1/index.html',
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
    except:
        print("Failed to restart")



def automateModem():
    battery = getBatteryPercent()
    logging.info('battery: ' + str(battery))
    
    if battery is not None:
        if battery > 80:
            turnOff()
            logging.info("Modem turned off - battery above 80%")
            return {
                "status": "off",
                "battery": battery,
                "message": "Modem turned off - battery above 80%"
            }
        elif battery < 20:
            turnOn()
            logging.info("Modem turned on - battery below 20%")
            return {
                "status": "on",
                "battery": battery,
                "message": "Modem turned on - battery below 20%"
            }
        else:
            # Battery is between 20-80%, no action needed
            logging.info(f"Battery at {battery}% - no action needed")
            return {
                "status": "ok",
                "battery": battery,
                "message": f"Battery at {battery}% - no action needed"
            }
    else:
        logging.error("Failed to get battery percentage")
        return {
            "status": "error",
            "battery": None,
            "message": "Failed to get battery percentage"
        }

def turnOnCharger():

    try:
        turnOn()
        return {
            "status": "success",
            "message": "Device turned on successfully",
            "internet_connected": True
        }
    except Exception as e:
        logging.error(f"Error turning on device: {str(e)}")
        return {
            "status": "error",
            "message": f"Error turning on device: {str(e)}",
            "internet_connected": False
        }


def turnOffCharger():

    try:
        turnOff()
        return {
            "status": "success",
            "message": "Device turned off successfully",
            "internet_connected": True
        }
    except Exception as e:
        logging.error(f"Error turning off device: {str(e)}")
        return {
            "status": "error",
            "message": f"Error turning off device: {str(e)}",
            "internet_connected": False
        }
