import json, requests
import jwt
import os
from time import sleep

is_msa_account = False
client_id = "97f01988-b110-4a78-b422-ad777b7ffae3"  # Multi-tenant DriveReader App
redirect_uri = "http://localhost:8076"
scopes = "offline_access openid profile Files.ReadWrite.All"

def refreshAuthzToken(client_id, refresh_token, redirect_uri, scopes, is_msa_account):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    params = {
        # Request parameters
    }
    url = f"https://login.microsoftonline.com/common/oauth2/v2.0/token"
    data = {
        "client_id": f"{client_id}",
        "scope": f"{scopes}",
        "refresh_token": f"{refresh_token}",
        "redirect_uri": f"{redirect_uri}",
        "grant_type": "refresh_token",
    }
    if is_msa_account == True:
        url = "https://login.live.com/oauth20_token.srf"
    req = requests.post(url, params=params, data=data, headers=headers)
    content = json.loads(req.content)
    access_token = content["access_token"]
    id_token = content["id_token"]
    refresh_token = content["refresh_token"]
    return id_token, access_token, refresh_token

if os.path.exists("refresh.txt") == False:
    print("I couldn't find a refresh token cache file. Running cache_refresh_token.py to try and get one.")
    os.system("start python cache_refresh_token.py")
    while os.path.exists("refresh.txt") == False:
        sleep(1)
    print("Found refresh.txt!")

with open("refresh.txt", "r") as cached_refresh_token:
    code = cached_refresh_token.read()

print(code)
try:
    if len(code.split(".")[2]) == 37:
        is_msa_account = True
except Exception as e:
    pass

id_token, access_token, refresh_token = refreshAuthzToken(client_id, code, redirect_uri, scopes, is_msa_account)
print(access_token)

decoded_id_token = jwt.decode(id_token, verify=False)
print(json.dumps(decoded_id_token, indent=2, sort_keys=True))
user = decoded_id_token["preferred_username"]

def readMail(token, user):
    url = f"https://graph.microsoft.com/v1.0/users/{user}/messages"
    params = {}
    headers = {"Authorization": f"{token}"}
    r = requests.get(url=url, headers=headers, params=params)
    data = r.json()
    pretty = json.dumps(json.loads(r.content), indent=2, sort_keys=True)
    # with open("mail.json", "w") as json_file:
    # json.dump(data, json_file)
    print(len(data))
    print("Recent Messages:\n")
    for message in range(len(data)):
        createdDateTime = data["value"][message]["createdDateTime"]
        subject = data["value"][message]["subject"]
        fromAddress = data["value"][message]["sender"]["emailAddress"]["address"]
        print(f"Created: {createdDateTime}\nFrom: {fromAddress}\nSubject: {subject}\n")

readMail(access_token, user)






