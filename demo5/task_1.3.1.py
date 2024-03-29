import requests
from requests.auth import HTTPBasicAuth

# Define the ONOS controller URL
controller_url = "http://127.0.0.1:8181"

# Define ONOS credentials
username = "onos"
password = "rocks"

# Function to get all available hosts
def get_all_hosts():
    # Construct the URL for hosts endpoint
    hosts_url = f"{controller_url}/onos/v1/hosts"

    # Send GET request to retrieve all hosts
    response = requests.get(hosts_url, auth=HTTPBasicAuth(username, password))

    # Check if request was successful (HTTP status code 200)
    if response.status_code == 200:
        hosts_info = response.json().get('hosts', [])
        return hosts_info
    else:
        return None

# Get all available hosts
hosts = get_all_hosts()

# Print host details
if hosts:
    print("Available Hosts:")
    print("ID\t\tMAC Address\t\tIP Address")
    for host in hosts:
        host_id = host['id']
        mac_address = host['mac']
        ip_addresses = host.get('ipAddresses', [])
        ip_addresses_str = ', '.join(ip_addresses) if ip_addresses else "N/A"
        print(f"{host_id}\t{mac_address}\t{ip_addresses_str}")
else:
    print("Failed to retrieve hosts.")

