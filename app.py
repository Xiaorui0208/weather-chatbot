  
#Python libraries that we need to import for our bot
import random
import intentWit
from flask import Flask, request 
from pymessenger.bot import Bot
app = Flask(__name__)
ACCESS_TOKEN = 'EAACpQHABF0UBALuobvuAqzFWEyEL3jV7eGoF3ZB9iy6P77cMGw4BqDYwgnGeWzqzWZAjNoRTZB9tEpXBv21ZB0RPC9zxxlnDIRXwaksNGXbxFnAokzKHoFebE7jzcNeslh5FJP5eZAFHdbyhPvsSIcK0MYmRUCsY9pACVGMPB2QZDZD'
VERIFY_TOKEN = 'VERIFY_TOKEN'
bot = Bot(ACCESS_TOKEN)
messages_dico = {}
user_must_complete={}

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       print("ce qu'envoie messenger \n")
       print(output)
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                #we only consider text messages from the user
                if message['message'].get('text'):
                    text_to_treat = message['message'].get('text')
                    #if it's a new user: welcome message + create history
                    if recipient_id not in messages_dico:
                        messages_dico[recipient_id] = [text_to_treat]
                        infos = bot.get_user_info(recipient_id)
                        send_message(recipient_id, "Bienvenue " + infos["first_name"] + "! \nJe suis un chatbot spécialiste dans les données météos, tu peux me donner un type de données ou une activité que tu souhaites pratiquer ainsi qu'une date et je saurai te guider ;) ")
                    if "détails" in text_to_treat:
                        messages_dico[recipient_id].append(text_to_treat)
                        print("voici le messages dico :\n ")
                        print(messages_dico[recipient_id])
                        reponse=intentWit.get_Keywords(str(messages_dico[recipient_id].pop(0)) + " détails")
                        send_message(recipient_id, str(reponse["message"]))
                        if len(messages_dico[recipient_id]) >= 2:
                            messages_dico[recipient_id].pop(0)
                    elif recipient_id in user_must_complete and user_must_complete[recipient_id]:
                        messages_dico[recipient_id].append(text_to_treat)
                        print("Je lui demande de compléter :\n ")
                        print(messages_dico[recipient_id])
                        reponse=intentWit.get_Keywords(str(messages_dico[recipient_id].pop(0)) +" "+ text_to_treat)
                        send_message(recipient_id, str(reponse["message"]))
                        user_must_complete[recipient_id]=False
                        if len(messages_dico[recipient_id]) >= 2:
                            messages_dico[recipient_id].pop(0)          
                    else:
                        reponse=intentWit.get_Keywords(text_to_treat)
                        messages_dico[recipient_id].append(text_to_treat)
                        print("voici le messages dico :\n ")
                        print(messages_dico[recipient_id])
                        if "details" in reponse:
                            send_message(recipient_id, str(reponse["message"]))
                            send_bubbles(recipient_id,"Click sur détails pour un bulletin plus précis", ["détails"])
                            if len(messages_dico[recipient_id]) >= 2:
                                messages_dico[recipient_id].pop(0)
                        elif "complement" in reponse:
                            #send_message(recipient_id, str(reponse["message"])) #pour quand?
                            user_must_complete[recipient_id]=True
                            complements=[" ce soir"," demain matin"," demain soir"]
                            send_bubbles(recipient_id,reponse["message"], complements)
                            if len(messages_dico[recipient_id]) >= 2:
                                messages_dico[recipient_id].pop(0)
                        else:
                            send_message(recipient_id, reponse["message"])
                            if len(messages_dico[recipient_id]) >= 2:
                                messages_dico[recipient_id].pop(0)
            return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

#ask the user to send his current location
def send_location(recipient_id):
    bot.send_quick_replies(recipient_id, 'give us your location', [{"content_type":"location"}])
    return "success"


#Send a proposition of multiple replies for the user, multiple_replies must be a list of String with 11 strings maximum.
def send_bubbles(recipient_id, response, multiple_replies):
    quick_replies = []
    for i in range(len(multiple_replies)):
    	quick_replies.append({"content_type":"text", "title":multiple_replies[i], "payload":"<POSTBACK_PAYLOAD>"})
    bot.send_quick_replies(recipient_id, response, quick_replies)
    return "success"



if __name__ == "__main__":
    app.run()
