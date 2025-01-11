import requests
import json
import time

with open("token.txt", 'r') as f:
        Token = f.read().strip()

headers = {
    "Authorization": Token,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36)",
}

Channel_ID = input("Channel ID: ")
Message = input("Message: ")
Type = input("1 (Spam) or 2 (Send Message): ")

Server = f"https://discord.com/api/v10/channels/{Channel_ID}/messages"

if Type =="1":
    spam_amount = int(input("Amount of messages: "))
    for i in range(spam_amount):
        time.sleep(0.25)
        Messagejson = {"content": Message}
        response = requests.post(Server, headers=headers, data=json.dumps(Messagejson))
        if response.status_code == 200:
            print(f"Message sent successfully! Code: {response.status_code}")
        elif response.status_code == 429:
            for i in range(5):
                print(f"Ratelimited retrying in {5 - i} seconds")
                time.sleep(1)
        else:
            print(f"Error {response.status_code} - {response.text}")    
if Type =="2":
        Messagejson = {"content": Message}
        response = requests.post(Server, headers=headers, data=json.dumps(Messagejson))
        if response.status_code == 200:
            print(f"Message sent successfully! Code: {response.status_code}")
        elif response.status_code == 429:
            for i in range(5):
                print(f"Ratelimited retrying in {5 - i} seconds")
                time.sleep(1)
        else:
            print(f"Error {response.status_code} - {response.text}")