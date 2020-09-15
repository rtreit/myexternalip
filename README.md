# myexternalip
Store current home computer external IP in cloud storage and retrieve via OAuth from anywhere. 

Say you're out and about in the world and you want to connect to your home PC. Maybe you want to be able to RDP or SSH into it. The computer is on your home WiFi which is wired into your ISP's cable modem. 

Setting up port forwarding rules to get the incoming connection from the Internet to your PC is straightforward. 

There's one small catch: how do you know what your current external IP address is if you're not at home to check? You could be fancy and have a static IP address but that seems like a bunch of trouble that's not needed. 

How about the home PC just periodically checks for you, stores the IP address in the cloud in a secure location, and you can retrieve it on demand while you're out and about? 

Let's do this. 

## Goals
* Free - use some cloud storage like OneDrive or Google Drive that doesn't require paying anything
* No secrets - don't require any secrets to be known ahead of time
* Only authenticate once per machine - every time you need to read or write data from the cloud, you shouldn't have to re-authenticate - make it easy

## Getting the external IP address
A simple Python script can run periodically check the Internet for its current public facing IP address. 

## Reading and writing the data to the cloud
We'll need a place to store the data in the cloud. In this project we'll use OneDrive but you could easily adapt it to use another cloud provide like Google Drive or DropBox. 

## A note on the OAuth app used
To read and write data to OneDrive (or any other cloud storage provider) you'll need to specify an OAuth app. This is the application that will be granted permissions to your cloud files. During the OAuth flow, the token provider will send the code to the redirect URI specified, which will then be exchanged for the actual auth tokens. 

For this project I've registered a multi-tenant app in Azure Active Directory for use with OneDrive. This app will work with both commerical AAD accounts as well as consumer MSA accounts. Since the redirect URI specified in the code only redirects to localhost, no tokens will be provided to any external service. So you're perfectly fine using the default AppId specified in the config. However, you might want to register your own AppId and use that instead. 

## Pre-requisites
* Python 3.6+ on your path

## Home Machine Setup
From an admin PowerShell prompt:
```sh
git clone https://github.com/rtreit/myexternalip.git
cd .\myexternalip\
python3 -m venv ./env
.\env\Scripts\activate
pip install -r .\requirements.txt
.\register_scheduled_task.ps1
```
Now you just need to provide a one-time authentication to cache your OAuth refresh token:
```sh
python .\save_ip_to_onedrive.py
```
You'll be prompted to give the OAuth app access to your OneDrive files. The refresh token is cached locally and will be re-used for future interactions with OneDrive. 

After consenting, your current IP address will be saved to your OneDrive root folder under a new \myexternalip folder. 

The IP address will be updated periodically in the background via the scheduled task. Now your home PC's external IP address will always be available to you in OneDrive, no matter where you are!

## Remote Machine Setup
You can  just browse manually the "myexternalip.txt" file in your OneDrive of course. Or to automate reading it:
```sh
git clone https://github.com/rtreit/myexternalip.git
cd .\myexternalip\
python3 -m venv ./env
.\env\Scripts\activate
pip install -r .\requirements.txt
python .\read_ip_from_onedrive.py
```
The first time you run, you'll be redirected to get the initial refresh token. 

Now any time you want to output your home PC's IP address, just run that last script:
```sh
python .\read_ip_from_onedrive.py
```

Now you can remotely access your home machine no matter where you are. 
