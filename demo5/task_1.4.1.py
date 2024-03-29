import requests
from requests.auth import HTTPBasicAuth
from tabulate import tabulate

# Define the ONOS controller URL
controller_url = "http://127.0.0.1:8181"

# Define ONOS credentials
username = "onos"
password = "rocks"

# Function to get all active links
def get_active_links():
    # Construct the URL for links endpoint
    links_url = f"{controller_url}/onos/v1/links"

    # Send GET request to retrieve information about all links
    response = requests.get(links_url, auth=HTTPBasicAuth(username, password))

    # Check if request was successful (HTTP status code 200)
    if response.status_code == 200:
        links_info = response.json().get('links', [])
        active_links = []
        for link in links_info:
            if link['state'] == 'ACTIVE':
                src_device = link['src']['device']
                src_port = link['src']['port']
                dst_device = link['dst']['device']
                dst_port = link['dst']['port']
                active_links.append([src_device, src_port, dst_device, dst_port])
        return active_links
    else:
        return None

# Get all active links
active_links = get_active_links()

# Print active links in a table format
if active_links:
    print(tabulate(active_links, headers=["Device ID (Source)", "Port (Source)", "Device ID (Destination)", "Port (Destination)"]))
else:
    print("No active links found.")

