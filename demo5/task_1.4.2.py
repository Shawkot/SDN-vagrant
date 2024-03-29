import requests
from requests.auth import HTTPBasicAuth

# Define the ONOS controller URL
controller_url = "http://127.0.0.1:8181"

# Define the device ID
device_id = "of:0000f2a53f2a7e46"

# Define ONOS credentials
username = "onos"
password = "rocks"

# Function to list all flows applied to a device
def list_flows_for_device(device_id):
    # Construct the URL for flows endpoint
    flows_url = f"{controller_url}/onos/v1/flows/{device_id}"

    # Send GET request to retrieve information about flows applied to the device
    response = requests.get(flows_url, auth=HTTPBasicAuth(username, password))

    # Check if request was successful (HTTP status code 200)
    if response.status_code == 200:
        flows_info = response.json().get('flows', [])
        if flows_info:
            return flows_info
        else:
            return None  # No flows found for the device
    else:
        return None  # Error retrieving flows information

# Get all flows applied to the device
flows = list_flows_for_device(device_id)

# Print flows information
if flows:
    print("Flows applied to device", device_id)
    for flow in flows:
        flow_id = flow.get('id', 'N/A')
        app_id = flow.get('appId', 'N/A')
        instructions = flow.get('treatment', {}).get('instructions', 'N/A')
        print(f"Flow ID: {flow_id}, Application ID: {app_id}, Device ID: {device_id}, Instructions: {instructions}")
else:
    print(f"No flows found for device {device_id}")

