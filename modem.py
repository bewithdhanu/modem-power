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


def is_wifi_connected():
    """
    Check if we have internet access by testing connectivity.
    This is more reliable than trying to detect specific WiFi networks.
    """
    try:
        # Method 1: Try to ping Google DNS (most reliable)
        result = subprocess.run(['ping', '-c', '1', '-W', '3000', '8.8.8.8'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return True
        
        # Method 2: Try to ping Cloudflare DNS
        result = subprocess.run(['ping', '-c', '1', '-W', '3000', '1.1.1.1'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return True
        
        # Method 3: Try to make an HTTP request to a reliable endpoint
        try:
            response = requests.get('http://httpbin.org/status/200', timeout=5)
            if response.status_code == 200:
                return True
        except:
            pass
        
        # Method 4: Check if we can resolve DNS
        result = subprocess.run(['nslookup', 'google.com'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and 'Address:' in result.stdout:
            return True
            
        return False
        
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError, Exception):
        return False


def wait_for_wifi_connection(timeout=300):
    start_time = time.time()
    while not is_wifi_connected():
        if time.time() - start_time >= timeout:
            logging.info("Timeout reached. Wi-Fi not connected.")
            break
        time.sleep(1)


def automateModem():
    wait_for_wifi_connection()
    logging.info("Wi-Fi is connected!")
    battery = getBatteryPercent()
    logging.info('battery: ' + str(battery))
    if battery is not None:
        if battery > 80 :
            turnOff()
            logging.info("Modem turned off")
            return {
                "status": "off",
                "battery": battery
            }
        if battery < 20:
            turnOn()
            logging.info("Modem turned on")
            return {
                "status": "on",
                "battery": battery
            }
    return {
        "status": "error",
        "battery": battery
    }


def turnOffDeviceByInternetCheck():
    """
    Turn off the device by checking internet connectivity.
    Only turns off if internet is available (meaning we're connected to modem).
    """
    try:
        # Check if we have internet connectivity
        if is_wifi_connected():
            logging.info("Internet connectivity confirmed, turning off device")
            turnOff()
            return {
                "status": "success",
                "message": "Device turned off successfully",
                "internet_connected": True
            }
        else:
            logging.info("No internet connectivity, device not turned off")
            return {
                "status": "error",
                "message": "No internet connectivity detected. Cannot turn off device.",
                "internet_connected": False
            }
    except Exception as e:
        logging.error(f"Error turning off device: {str(e)}")
        return {
            "status": "error",
            "message": f"Error turning off device: {str(e)}",
            "internet_connected": False
        }
