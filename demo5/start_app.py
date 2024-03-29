import requests
from requests.auth import HTTPBasicAuth
import json

url = "http://127.0.0.1:8181/onos/v1/applications/"

apps = ["org.onosproject.hostprovider", "org.onosproject.mobility", "org.onosproject.lldprovider", "org.onosproject.ofagent", "org.onosproject.openflow-base", "org.onosproject.openflow", "org.onosproject.roadm", "org.onosproject.proxyarp", "org.onosproject.fwd"]

for app in apps:
	myResponse = requests.post(url + app + "/active",auth=HTTPBasicAuth('onos','rocks'))
	if myResponse.status_code == 200:
		print('Activated: %s '%app)
		
