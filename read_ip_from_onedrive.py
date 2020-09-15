import sharedFunctions as sf
import requests
import json

config_file = "config.json"
with open(config_file, "r") as f:
    config_data = f.read()
config = json.loads(config_data)
ipfile = config["ipfile"]

user, access_token = sf.getAuthDetails()

print(f"Trying to retrieve external IP address from {ipfile} in {user}'s Drive...'")


url = f"https://graph.microsoft.com/v1.0/users/{user}/drives"
user_drive = sf.callGraphApi(url, access_token)
drive_id = user_drive["value"][0]["id"]


url = f"https://graph.microsoft.com/v1.0/users/{user}/drives/{drive_id}/root/search(q='{ipfile}')"
myipfile = sf.callGraphApi(url, access_token)
if len(myipfile["value"]) > 0:
    data = myipfile["value"][0]
    downloadurl = data["@microsoft.graph.downloadUrl"]
    r = requests.get(downloadurl)
    print(r.content.decode("utf-8"))
else:
    print(f"Did not find file {ipfile} in {user}'s drive root!'")
