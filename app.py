from flask import Flask, request
import random
from pymessenger.bot import Bot
import os
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
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
# ACCESS_TOKEN = ""
# VERIFY_TOKEN = ""
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
    compliments = ["You look super cute today! I mean, y-you look super cute every day, but that's embarrassing...",
                   "I love it when you have your hair like that. Just makes me want to fluff it!",
                   "You're so kind and generous to your friends. You're my role model!"]
    positive_reminders = ["Remember you are loved, that your friends care for you even if you don't see it",
                          "Your friends want to be with you as much as you long to be with them",
                          "You are a one-of-a-kind person, and people love you for who you are :)"]
    # chibird = ["https://78.media.tumblr.com/df8ac8e3607139e76f10d01bf35b7103/tumblr_p8v14fdkMo1qc4uvwo1_500.png",
    #            "https://78.media.tumblr.com/4aeab456ea9ea1e90062080320c892f9/tumblr_p8aljuoBJU1qc4uvwo1_500.png",
    #            "https://78.media.tumblr.com/4aeab456ea9ea1e90062080320c892f9/tumblr_p8aljuoBJU1qc4uvwo1_500.png",
    #            "https://78.media.tumblr.com/310eaa8079557c7441bd0ad27f2df98f/tumblr_p7oe6bF5Sw1qc4uvwo1_500.gif",
    #            "https://78.media.tumblr.com/6576e0fd2392d8d805eee5ecb5ab0fae/tumblr_p7iy1aNd9o1qc4uvwo2_500.png",
    #            "https://78.media.tumblr.com/fdc0b83117d6d721c6000ce04d53e0eb/tumblr_p7bdad9ub11qc4uvwo2_500.png",
    #            "https://78.media.tumblr.com/5dad2503c5a6b344f2176adde12e923a/tumblr_p7bdad9ub11qc4uvwo1_500.png",
    #            "https://78.media.tumblr.com/bd6db304c5618ac4a6b3ce9bf463de0e/tumblr_p78jz3hO6K1qc4uvwo1_500.png",
    #            "https://78.media.tumblr.com/7e03ffe95b67876b6fea9b938f970a47/tumblr_p740rjPlGz1qc4uvwo1_500.png"]
    mental_health = ["Taking care of your body is important - and your brain is part of that! Please don't feel bad for taking a break when you need it. <3",
                     "You are not just your mental health; you are a multi-faceted, like a crystal growing out of the earth. <3",
                     "Self care is not selfish! You are more special and important than all the little pains in life."]

    grace_thoughts = ["Grace is waiting for a message from you! :) Go! It's not pestering if they love hearing from you.",
                      "Grace misses you very much. :( <3",
                      "You are a wonderful person, and Grace thinks you deserve every bit of love she can give you. <3"]

    available_options = [positive_reminders, compliments, mental_health, grace_thoughts]
    result = random.choice(available_options)
    return random.choice(result)

def send_message(recipient_id, response):
    # sends user a text-based message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == '__main__':
    app.run()

