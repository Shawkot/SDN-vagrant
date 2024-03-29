import requests
from requests.auth import HTTPBasicAuth

# Define the ONOS controller URL
controller_url = "http://127.0.0.1:8181"

# Define the device ID
device_id = "of:0000369ec87f964a"

# Define ONOS credentials
username = "onos"
password = "rocks"

# Function to get active ports
def get_active_ports(device_id):
    # Construct the URL for device ports endpoint
    device_ports_url = f"{controller_url}/onos/v1/devices/{device_id}/ports"

    # Send GET request to retrieve device ports
    response = requests.get(device_ports_url, auth=HTTPBasicAuth(username, password))

    # Check if request was successful (HTTP status code 200)
    if response.status_code == 200:
        ports_info = response.json().get('ports', [])
        active_ports = []
        for port in ports_info:
            if port.get('enabled', False):
                active_ports.append(port['name'])
        return active_ports
    else:
        return None

# Get active ports
active_ports = get_active_ports(device_id)

# Print active ports
if active_ports:
    print(f"Active ports for device ID: {device_id}")
    for port_name in active_ports:
        print(f"Port: {port_name}")
else:
    print(f"Failed to retrieve active ports for device ID: {device_id}")

