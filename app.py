from flask import Flask, request, render_template, jsonify
import requests
import json
import time

app = Flask(__name__)

with open("token.txt", "r") as f:
    Token = f.read().strip()

headers = {
    "Authorization": Token,
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

        server = f"https://discord.com/api/v10/channels/{channel_id}/messages"
        message_json = {"content": message}

        if msg_type == "1":  # Spam messages
            all_feedback = []  # List to hold feedback for all spam messages
            for i in range(int(spam_amount)):
                response = requests.post(server, headers=headers, data=json.dumps(message_json))
                if response.status_code == 200:
                    all_feedback.append(f"{i + 1}. Message sent successfully!")
                elif response.status_code == 429:
                    retry_after = response.json().get("retry_after", 1)
                    all_feedback.append(f"Rate limited. Retrying after {retry_after} seconds.")
                    time.sleep(retry_after)
                else:
                    all_feedback.append(f"Error {response.status_code}: {response.text}")

            # Join all feedback into one string to display all messages
            feedback = "<br>".join(all_feedback)
                
        elif msg_type == "2":  # Single message
            response = requests.post(server, headers=headers, data=json.dumps(message_json))
            if response.status_code == 200:
                feedback = "Message sent successfully!"
            elif response.status_code == 429:
                retry_after = response.json().get("retry_after", 1)
                feedback = f"Rate limited. Retrying after {retry_after} seconds."
                time.sleep(retry_after)
            else:
                feedback = f"Error {response.status_code}: {response.text}"

    # Render the form and pass feedback to template
    return render_template("index.html", feedback=feedback)


if __name__ == "__main__":
    app.run(debug=True)
