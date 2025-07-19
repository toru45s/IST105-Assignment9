import os
import datetime
import requests
import urllib3
from pymongo import MongoClient
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from django.shortcuts import render
from .dnac_config import DNAC

# Load .env file
load_dotenv()

# Disable SSL warnings
urllib3.disable_warnings()

# MongoDB setup
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["dnac_logs"]
collection = db["actions"]

def log_action(action, ip=None, success=True):
    collection.insert_one({
        "timestamp": datetime.datetime.now(),
        "action": action,
        "ip": ip,
        "success": success
    })

def unified_dashboard(request):
    token = None
    devices = []
    interfaces = []
    ip = request.GET.get("ip")
    error = None

    # 1. Authenticate
    try:
        url = f"https://{DNAC['host']}:{DNAC['port']}/dna/system/api/v1/auth/token"
        res = requests.post(
            url,
            auth=HTTPBasicAuth(DNAC['username'], DNAC['password']),
            verify=False,
            timeout=10
        )
        res.raise_for_status()
        token = res.json().get("Token")
        log_action("auth", success=True)
    except Exception as e:
        error = "Authentication failed"
        log_action("auth", success=False)

    # 2. Get devices
    if token:
        try:
            device_url = f"https://{DNAC['host']}:{DNAC['port']}/api/v1/network-device"
            headers = {"X-Auth-Token": token}
            dev_res = requests.get(device_url, headers=headers, verify=False, timeout=10)
            dev_res.raise_for_status()
            devices = dev_res.json().get("response", [])
            log_action("list_devices", success=True)
        except Exception as e:
            error = "Failed to fetch network devices"
            log_action("list_devices", success=False)

    # 3. Get interfaces if IP is provided
    if token and ip:
        try:
            device = next((d for d in devices if d.get("managementIpAddress") == ip), None)
            if not device:
                raise ValueError("Device not found")

            intf_url = f"https://{DNAC['host']}:{DNAC['port']}/api/v1/interface"
            intf_res = requests.get(
                intf_url,
                headers=headers,
                params={"deviceId": device["id"]},
                verify=False,
                timeout=10
            )
            interfaces = intf_res.json().get("response", [])
            log_action("get_interfaces", ip=ip, success=True)
        except Exception as e:
            error = f"Failed to get interfaces for {ip}"
            log_action("get_interfaces", ip=ip, success=False)

    return render(request, "dna_center_cisco/dashboard.html", {
        "token": token,
        "devices": devices,
        "interfaces": interfaces,
        "ip": ip,
        "error": error,
    })