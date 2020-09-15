import requests
import re
import sharedFunctions as sf
import requests
import json

config_file = "config.json"
with open(config_file, "r") as f:
    config_data = f.read()
config = json.loads(config_data)
ipfile = config["ipfile"]

url = "http://checkip.dyndns.org"
r = requests.get(url)
myIP = re.findall(
    "(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)",
    r.text,
)

text = f"your external IP Address is:\n{myIP[0]}"
print(text)


user, access_token = sf.getAuthDetails()

print(f"Trying to save external IP address to {ipfile} in {user}'s Drive...'")


url = f"https://graph.microsoft.com/v1.0/users/{user}/drives"
user_drive = sf.callGraphApi(url, access_token)
drive_id = user_drive["value"][0]["id"]


url = f"https://graph.microsoft.com/v1.0/users/{user}/drives/{drive_id}/root:/myexternalip/{ipfile}:/content"
result = sf.callGraphApi(url, access_token, method="put", payload=text)
if "name" in result.keys():
    print(f"{result['name']} saved - view at: {result['webUrl']}")
else:
    print(result)
