import json
import logging
import os

import requests
import xmltodict

from device import turnOff, turnOn

# Get modem IP from environment variable or use default
MODEM_IP = os.getenv('MODEM_IP', '192.168.1.1')

def isModemReachable():
    """Check if modem is reachable"""
    try:
        response = requests.get(f"http://{MODEM_IP}/", timeout=5)
        return response.status_code == 200
    except:
        return False


def getBatteryPercent():
    try:
        url = f"http://{MODEM_IP}/mark_title.w.xml"

        headers = {
            'Referer': f'http://{MODEM_IP}/index.html'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse the XML data to a Python dictionary
        xml_dict = xmltodict.parse(response.text)

        # Convert the dictionary to JSON
        json_data = json.dumps(xml_dict, indent=4)

        data_dict = json.loads(json_data)
        return int(data_dict['title']['batt_p'])
    except requests.exceptions.RequestException as e:
        logging.error(f"Network error getting battery from {MODEM_IP}: {e}")
        return None
    except (KeyError, ValueError, xmltodict.ParsingInterrupted) as e:
        logging.error(f"Data parsing error: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error getting battery: {e}")
        return None


def restartModem():
    try:
        url = f"http://{MODEM_IP}/wxml/set_reboot.xml"

        payload = "reboot=1"
        headers = {
            'Referer': f'http://{MODEM_IP}/index.html',
        }

        response = requests.post(url, headers=headers, data=payload, timeout=10)
        response.raise_for_status()
        
        logging.info(f"Modem restart response: {response.text}")
        return True
    except requests.exceptions.RequestException as e:
        logging.error(f"Network error restarting modem at {MODEM_IP}: {e}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error restarting modem: {e}")
        return False


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
