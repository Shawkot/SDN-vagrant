import requests
from requests.auth import HTTPBasicAuth

# Define the ONOS controller URL
controller_url = "http://127.0.0.1:8181"

# Define the device ID
device_id = "of:0000369ec87f964a"

# Define ONOS credentials
username = "onos"
password = "rocks"

# Function to get active MAC addresses and port names
def get_active_macs_and_ports(device_id):
    # Construct the URL for device ports endpoint
    device_ports_url = f"{controller_url}/onos/v1/devices/{device_id}/ports"

    # Send GET request to retrieve device ports
    response = requests.get(device_ports_url, auth=HTTPBasicAuth(username, password))

    # Check if request was successful (HTTP status code 200)
    if response.status_code == 200:
        ports_info = response.json()['ports']
        active_macs = {}
        for port in ports_info:
            if 'mac' in port and port['enabled']:
                active_macs[port['name']] = port['mac']
        return active_macs
    else:
        return None

# Get active MAC addresses and port names
active_macs = get_active_macs_and_ports(device_id)

# Print active MAC addresses and port names
if active_macs:
    print(f"Active MAC addresses and Port names for device ID: {device_id}")
    for port_name, mac_address in active_macs.items():
        print(f"Port: {port_name}, MAC: {mac_address}")
else:
    print(f"Failed to retrieve active MAC addresses and port names for device ID: {device_id}")

