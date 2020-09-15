import json, requests
import jwt
import os
from time import sleep

is_msa_account = False

config_file = "config.json"
if config_file:
    with open(config_file, "r") as f:
        config_data = f.read()
    config = json.loads(config_data)
else:
    raise ValueError("Please provide config.json file with account information.")

client_id = config["client_id"]  # Multi-tenant DriveReader App
redirect_uri = config["redirect_uri"]
scopes = config["scopes"]
ipfile = config["ipfile"]


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


def callGraphApi(url, user_token, method="get", payload=""):
    params = {}
    headers = {"Authorization": f"{user_token}", "Content-Type": "text/plain"}
    if method == "put":
        r = requests.put(url=url, headers=headers, params=params, data=payload)
    else:
        r = requests.get(url=url, headers=headers, params=params)
    return json.loads(r.content)


def getAuthDetails(is_msa_account=is_msa_account):
    if os.path.exists("refresh.txt") == False:
        print(
            "I couldn't find a refresh token cache file. Running cache_refresh_token.py to try and get one."
        )
        os.system("start python cache_refresh_token.py")
        while os.path.exists("refresh.txt") == False:
            sleep(1)
        print("Found refresh.txt!")

    with open("refresh.txt", "r") as cached_refresh_token:
        code = cached_refresh_token.read()

    # print(code)
    try:
        if len(code.split(".")[2]) == 37:
            is_msa_account = True
    except Exception as e:
        pass

    id_token, access_token, refresh_token = refreshAuthzToken(
        client_id, code, redirect_uri, scopes, is_msa_account
    )
    # print(access_token)

    decoded_id_token = jwt.decode(id_token, verify=False)
    # print(json.dumps(decoded_id_token, indent=2, sort_keys=True))
    user = decoded_id_token["preferred_username"]
    return user, access_token
