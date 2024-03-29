import requests
from requests.auth import HTTPBasicAuth

# Define the URL for the devices endpoint
url = "http://127.0.0.1:8181/onos/v1/devices/"

# Define the ONOS credentials
username = 'onos'
password = 'rocks'

# Send GET request to retrieve the list of devices
response = requests.get(url, auth=HTTPBasicAuth(username, password))

# Check if the request was successful (HTTP status code 200)
if response.status_code == 200:
    devices = response.json()['devices']
    # Extract device IDs from the response
    device_ids = [device['id'] for device in devices]
    print("Available devices IDs:")
    for device_id in device_ids:
        print(device_id)
else:
    print(f"Failed to retrieve devices: {response.status_code}")

