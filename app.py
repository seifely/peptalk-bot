from flask import Flask, request
import random
from pymessenger.bot import Bot
import os
# using flask, we can create an endpoint - a fancy way of referring to to a website URL - such as "/r/science"

app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']  # replacing the actual access token if we use Heroku to host
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']  # see above
bot = Bot(ACCESS_TOKEN)


@app.route('/', methods=['GET', 'POST'])  # main app location, including app methods
def receive_message():
    """Before allowing people to message your bot, Facebook has implemented a verify token
    that confirms all requests that your bot receives came from Facebook."""
    if request.method == 'GET':
        # before allowing people to message bot, need to check FB verify token that confirms all requests that
        # bot receives comes from FB
        token_sent = request.args.get("hub.verify_token")  # last part = a token we make up and give to FB for verific.
        return verify_fb_token(token_sent)

    # if the bot is not receiving a GET, likely receiving a POST req. where FB is sending bot a message sent by user
    else:
        # get whatever message a user sent to the bot
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    # FB Messenger ID for user so we know where to send responses back to
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):  # is this based on extracting input type as a string?
                        response_sent_text = get_message()  # get the (for now) randomised message choice
                        send_message(recipient_id, response_sent_text)
                    if message['message'].get('attachments'): # if user sends a non-text item like a GIF or video
                        response_sent_nontext = get_message()
                        send_message(recipient_id, response_sent_nontext)
    return "Message Processed"

# moving on, need to handle verifying a message from FB as well as generating and sending a response back to the user
# FB requires bot to have a verify token that you also provide them in order to be secure


def verify_fb_token(token_sent):
    # take token sent by FB and verify it matches the verify token you sent
    if token_sent == VERIFY_TOKEN:  # if the token sent by facebook is the one specified 'here'
        return request.args.get("hub.challenge")  # get the request arguments
    return 'Invalid verification token'  # else, throw up an error


def get_message():
    # chooses a random message to send to the user
    compliments = ["You look super cute today! I mean, y-you look super cute every day, but that's embarrassing...",
                   "I love it when you have your hair like that. Just makes me want to fluff it!",
                   "You're so kind and generous to your friends. You're my role model!"]

    positive_reminders = ["Remember you are loved, that your friends care for you even if you don't see it",
                          "Your friends want to be with you as much as you long to be with them",
                          "You are a one-of-a-kind person, and people love you for who you are :)"]

    mental_health = ["Taking care of your body is important - and your brain is part of that! Please don't feel bad for taking a break when you need it. <3",
                     "You are not just your mental health; you are a multi-faceted, like a crystal growing out of the earth. <3",
                     "Self care is not selfish! You are more special and important than all the little pains in life."]

    grace_thoughts = ["Grace is waiting for a message from you! :) Go! It's not pestering if they love hearing from you.",
                      "Grace misses you very much. :( <3",
                      "You are a wonderful person, and Grace thinks you deserve every bit of love she can give you. <3"]

    available_options = [positive_reminders, compliments, mental_health, grace_thoughts]  # random category choice
    result = random.choice(available_options)  # random choice from that category
    return random.choice(result)


def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)  # sends user a txt-based message given via input response parameter
    return "success"

if __name__ == '__main__':
    app.run()  # run the app

