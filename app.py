from flask import Flask, request
import random
from pymessenger.bot import Bot
# using flask, we can create an endpoint - a fancy way of referring to to a website URL - such as "/r/science"
# to begin, we'll create a basic Flask app called app.py (see Flask intro post for learning abt the framework

# app = Flask(__name__)
# @app.route('/', methods=['GET', 'POST'])
# def receive_message():
#     return "Hello World!"
#
# if __name__ == '__main__':
#     app.run()

# the above is the basis of a Flask app - to see more, go to http://flask.pocoo.org/docs/0.12/quickstart/
# to handle the sending of messages back to a user who communicates with our bot, we'll be using the PyMessenger
# library

# to make the bot, we first need to handle two types of requests: GET and POST. GET requests are used when FB
# checks the bot's verify token

app = Flask(__name__)
ACCESS_TOKEN = 'EAAYj3FZACfhYBAF2kJzYcvmqaIcmxfCpdJZAZBnQ0bdMoZAAlLHoFOhmyPBLl8vMNkBEoXf5TjkxxdMhTPhZCoddcbDQIxKlQzl0MwFbdzq2UcFAcHGfk1CANWRgycEyoLO6LWXWywH0135YCM2EZBlhyenvAx6iu4rn4z17CH4ICrJdnNVHKR'
VERIFY_TOKEN = 'bibliography1994'
bot = Bot(ACCESS_TOKEN)


@app.route('/', methods=['GET', 'POST'])
def receive_message():
    """Before allowing people to message your bot, Facebook has implemented a verify token
    that confirms all requests that your bot receives came from Facebook."""
    if request.method == 'GET':
        # before allowing people to message bot, need to check FB verify token that confirms all requests that
        # bot receives comes from FB
        token_sent = request.args.get("hub.verify_token") # last part = a token we make up and give to FB for verific.
        return verify_fb_token(token_sent)

    # if the bot is not receiving a GET, likely receiving a POST req. where FB is sending bot a message sent by user
    else:
        # get whatever message a user sent to the bot
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    # FB Messanger ID for user so we know where to send responses back to
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):
                        response_sent_text = get_message()
                        send_message(recipient_id, response_sent_text)
                    if message['message'].get('attachments'): # if user sends a non-text item like a GIF or video
                        response_sent_nontext = get_message()
                        send_message(recipient_id, response_sent_nontext)
    return "Message Processed"

# moving on, need to handle verifying a message from FB as well as generating and sending a response back to the user
# FB requires bot to have a verify token that you also provide them in order to be secure

def verify_fb_token(token_sent):
    # take token sent by FB and verify it matches the verify token you sent
    # if they match, allow request, else return error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def get_message():
    # chooses a random message to send to the user
    positive_reminders = ["Remember you are loved, that your friends care for you even if you don't see it",
                          "Your friends want to be with you as much as you long to be with them",
                          "You are a one-of-a-kind person, and people love you for who you are :)"]
    return random.choice(positive_reminders)

def send_message(recipient_id, response):
    # sends user a text-based message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == '__main__':
    app.run()

