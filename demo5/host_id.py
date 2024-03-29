import requests
from requests.auth import HTTPBasicAuth

# Define the ONOS controller URL
controller_url = "http://127.0.0.1:8181"

# Define the target IP address
target_ip = "10.0.0.130"

# Define ONOS credentials
username = "onos"
password = "rocks"

# Function to get host ID and port used by the host with the target IP address
def get_host_and_port_for_ip(target_ip):
    # Construct the URL for hosts endpoint
    hosts_url = f"{controller_url}/onos/v1/hosts"

    # Send GET request to retrieve information about all hosts
    response = requests.get(hosts_url, auth=HTTPBasicAuth(username, password))

    # Check if request was successful (HTTP status code 200)
    if response.status_code == 200:
        hosts_info = response.json().get('hosts', [])
        for host in hosts_info:
            ip_addresses = host.get('ipAddresses', [])
            if target_ip in ip_addresses:
                host_id = host.get('mac', None)  # Get host ID (MAC address)
                port = host.get('locations', [{}])[0].get('port', None)  # Get port
                return host_id, port
        return None, None  # Host with target IP not found
    else:
        return None, None  # Error retrieving hosts information

# Get host ID and port used by the host with the target IP address
host_id, port = get_host_and_port_for_ip(target_ip)

# Print host ID and port
if host_id and port:
    print(f"Host with IP address {target_ip} is connected to:")
    print(f"Host ID (MAC address): {host_id}")
    print(f"Port: {port}")
else:
    print(f"No host found with IP address {target_ip}")

