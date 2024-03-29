import requests
from requests.auth import HTTPBasicAuth

# Define the ONOS controller URL
controller_url = "http://127.0.0.1:8181"

# Define ONOS credentials
username = "onos"
password = "rocks"

# Function to list all intents
def list_intents():
    # Construct the URL for intents endpoint
    intents_url = f"{controller_url}/onos/v1/intents"

    # Send GET request to retrieve information about all intents
    response = requests.get(intents_url, auth=HTTPBasicAuth(username, password))

    # Check if request was successful (HTTP status code 200)
    if response.status_code == 200:
        intents_info = response.json().get('intents', [])
        if intents_info:
            return intents_info
        else:
            return None  # No intents found
    else:
        return None  # Error retrieving intents information

# Get all intents
intents = list_intents()

# Print intents information
if intents:
    print("List of Intents:")
    for intent in intents:
        intent_id = intent.get('id', 'N/A')
        app_id = intent.get('appId', 'N/A')
        state = intent.get('state', 'N/A')
        print(f"Intent ID: {intent_id}, Application ID: {app_id}, State: {state}")
else:
    print("No intents found.")

