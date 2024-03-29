import requests
from requests.auth import HTTPBasicAuth

# Define the ONOS controller URL
controller_url = "http://127.0.0.1:8181"

# Define the host ID to remove
host_id = "1E:A3:9F:E8:13:AF/None"

# Define ONOS credentials
username = "onos"
password = "rocks"

# Function to remove a host by its ID
def remove_host_by_id(host_id):
    # Construct the URL for the specific host endpoint
    host_url = f"{controller_url}/onos/v1/hosts/{host_id}"

    # Send DELETE request to remove the host
    response = requests.delete(host_url, auth=HTTPBasicAuth(username, password))

    # Check if request was successful (HTTP status code 204)
    if response.status_code == 204:
        print(f"Host with ID {host_id} has been successfully removed.")
    else:
        print(f"Failed to remove host with ID {host_id}.")
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.text}")

# Remove the host by its ID
remove_host_by_id(host_id)

