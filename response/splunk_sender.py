import requests
import json
import time

SPLUNK_HEC_URL = "https://127.0.0.1:8088/services/collector"
SPLUNK_TOKEN = "c0077094-1ee4-4ec3-b8eb-45d50dbd08b1"


def send_to_splunk(alert):
    print("DEBUG: Sending event to Splunk HEC...")


    headers = {
        "Authorization": f"Splunk {SPLUNK_TOKEN}"
    }

    payload = {
    "time": int(time.time()),   # ⭐ important
    "event": alert,
    "sourcetype": "security:incident",
    "index": "phishing_security"
}

    response = requests.post(
        SPLUNK_HEC_URL,
        headers=headers,
        data=json.dumps(payload),
        verify=False
    )

    print("HEC STATUS:", response.text)