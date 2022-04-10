import json

import requests

url = "http://192.168.0.197:8000/pm100d/start"

payload = json.dumps({"deviceID": -1733073, "wavelength": 18898246.292536095})
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": "Bearer REPLACE_WITH_BEARER_TOKEN",
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response)
