from flask import Flask, request
from pymessenger.bot import Bot

from config import FACEBOOK_TOKEN, FACEBOOK_ID

app = Flask(__name__)

bot = Bot(FACEBOOK_TOKEN)

@app.route("/facebook", methods=['GET'])
def autenticate():
    token_sent = request.args.get("hub.verify_token")    
    if token_sent == FACEBOOK_ID:
        return request.args.get("hub.challenge")
    return "FACEBOOK_ID incorrecto."

@app.route("/facebook", methods=['POST'])
def receive_message():
    output = request.get_json()
    for event in output['entry']:
        messaging = event['messaging']
        for message in messaging:
            if message.get('message'):
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    response = message['message'].get('text')
                    bot.send_text_message(recipient_id, response)
        return "Mensaje recibido y procesado!"

if __name__ == "__main__":
    app.run(port=80, debug=True)


