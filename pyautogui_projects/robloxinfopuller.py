#!/usr/bin/env python3
import requests

username = input("Enter username: ")

# get user id from username
res = requests.post("https://users.roblox.com/v1/usernames/users", 
    json={"usernames": [username], "excludeBannedUsers": False})

data = res.json()

if not data["data"]:
    print("User not found")
else:
    user = data["data"][0]
    user_id = user["id"]
    display_name = user["displayName"]
    print(f"Display Name: {display_name}")
    print(f"User ID: {user_id}")

    # get full profile
    profile = requests.get(f"https://users.roblox.com/v1/users/{user_id}").json()
    print(f"Description: {profile.get('description', 'None')}")
    print(f"Created: {profile.get('created')}")
    print(f"Banned: {profile.get('isBanned')}")
    # get current game
    presence = requests.post("https://presence.roblox.com/v1/presence/users",
        json={"userIds": [user_id]}).json()
    
    p = presence["userPresences"][0]
    if p["userPresenceType"] == 2:
        print(f"Currently in game: {p['lastLocation']}")
    elif p["userPresenceType"] == 1:
        print("Currently on website")
    else:
        print("Currently offline")
