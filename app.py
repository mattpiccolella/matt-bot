import os, sys, json

import requests, time
from flask import Flask, request
from chatterbot import ChatBot

from multiprocessing import Pool

app = Flask(__name__)

RANDOM_STRING = 'BrMtyyEe5Rqvh1kF0fMo'
INPUT_DATA_FILE = 'data/result.csv'

def generate_bot_response(sender_id, message_text):
    chatbot = ChatBot("Matt Bot",
        storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
        database='heroku_vzt7md78',
        database_uri='mongodb://matt:buddymatt123@ds119151.mlab.com:19151/heroku_vzt7md78')
    response = chatbot.get_response(message_text)
    log("Sending message " + response.text + " to " + str(sender_id))
    send_message(sender_id, response.text)

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            print os.environ["VERIFY_TOKEN"]
            print request.args.get("hub.verify_token")
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello World", 200


@app.route('/', methods=['POST'])
def webhook():
    # Endpoint for processing incoming messaging events from Messenger users.
    data = request.get_json()

    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):
                    sender_id = messaging_event["sender"]["id"]        # The Facebook ID of the person sending you the message.
                    recipient_id = messaging_event["recipient"]["id"]  # The Facebook ID of our page.
                    message_text = messaging_event["message"]["text"]  # The message's text.
                    pool = Pool(processes=1) # Start a worker progress to get our chatbot output.
                    log("Received message " + message_text + " from " + str(sender_id))
                    result = pool.apply_async(generate_bot_response, args=(sender_id,message_text)) # Asynchronous function to find response from chatbot.

                if messaging_event.get("delivery"):  # Delivery Confirmation.
                    pass
                if messaging_event.get("optin"):  # Opt-in Confirmation.
                    pass
                if messaging_event.get("postback"):  # User clicked/tapped "postback" button in earlier message.
                    pass

    return "OK", 200


def send_message(recipient_id, message_text):
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    result = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if result.status_code != 200:
        log(result.status_code)
        log(result.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
