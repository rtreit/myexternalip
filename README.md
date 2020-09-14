# myexternalip
Store current home computer external IP in cloud storage and retrieve via OAuth from anywhere. 

Say you're out and about in the world and you want to connect to your home PC. Maybe you want to be able to RDP or SSH into it. The computer is on your home WiFi which is wired into your ISP's cable modem. 

Setting up port forwarding rules to get the incoming connection from the Internet to your PC is straightforward. 

There's one small catch: how do you know what your current external IP address is if you're not at home to check? You could be fancy and have a static IP address but that seems like a bunch of trouble that's not needed. 

How about the home PC just periodically checks for you, stores the IP address in the cloud in a secure location, and you can retrieve it on demand while you're out and about? 

Let's do this. 
