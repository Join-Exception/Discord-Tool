from flask import Flask, request, render_template, jsonify, redirect, url_for
import requests
import json
import time
import logging

app = Flask(__name__)

logging.basicConfig(filename="message_logs.txt", level=logging.INFO, format="%(asctime)s - %(message)s")


with open("token.txt", "r") as f:
    Token = f.read().strip()

with open("token2.txt", "r") as g:
    Token2 = g.read().strip()

def get_current_token():
    return Token

def get_headers(token):
    return {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

@app.route("/", methods=["GET", "POST"])
def send_message():
    feedback = ""

    if request.method == "POST":
        channel_id = request.form.get("channel_id")
        message = request.form.get("message")
        msg_type = request.form.get("type")
        spam_amount = request.form.get("spam_amount", 1)

    
        user_ip = request.remote_addr
        logging.info(f"Request from IP: {user_ip}, Channel ID: {channel_id}, Message: {message}, Type: {msg_type}, Spam Amount: {spam_amount}")

        server = f"https://discord.com/api/v10/channels/{channel_id}/messages"
        message_json = {"content": message}

        current_token = get_current_token()

        if msg_type == "1":
            all_feedback = [] 
            for i in range(int(spam_amount)):
                response = requests.post(server, headers=get_headers(current_token), data=json.dumps(message_json))
                
                if response.status_code == 200:
                    all_feedback.append(f"{i + 1}. Message sent successfully!")
                elif response.status_code == 429:
                    all_feedback.append(f"Rate limited. Retrying after 3 seconds.")
                    logging.info(f"Rate limited. Retrying after 3 seconds.")
                    time.sleep(3)
                    spam_amount -= 1
                    current_token = Token2 if current_token == Token else Token
                    logging.info(f"Switched to token: {current_token}")

                else:
                    all_feedback.append(f"Error {response.status_code}: {response.text}")

            logging.info(f"Spam Feedback: {' | '.join(all_feedback)}")

            feedback = " ".join(all_feedback)

    return render_template("index.html", feedback=feedback)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
