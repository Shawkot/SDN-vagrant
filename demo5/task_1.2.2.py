import requests
from requests.auth import HTTPBasicAuth

# Define the ONOS controller URL
controller_url = "http://127.0.0.1:8181"

# Define the device ID
device_id = "of:0000369ec87f964a"

# Define ONOS credentials
username = "onos"
password = "rocks"

# Function to get device details
def get_device_details(device_id):
    # Construct the URL for device details endpoint
    device_url = f"{controller_url}/onos/v1/devices/{device_id}"

    # Send GET request to retrieve device details
    response = requests.get(device_url, auth=HTTPBasicAuth(username, password))

    # Check if request was successful (HTTP status code 200)
    if response.status_code == 200:
        device_info = response.json()
        ip_address = device_info['annotations']['managementAddress']
        of_version = device_info['annotations']['protocol']
        return ip_address, of_version
    else:
        return None, None

# Get device details
ip_address, of_version = get_device_details(device_id)

# Print device details
if ip_address and of_version:
    print(f"Device ID: {device_id}")
    print(f"IP Management Address: {ip_address}")
    print(f"OpenFlow Version: {of_version}")
else:
    print(f"Failed to retrieve device details for device ID: {device_id}")

