



#Code à ajouter dans le script "bot.py" dans la librairie pymessenger



def send_quick_replies(self, recipient_id, message, quick_replies):
        '''Send text messages to the specified recipient.
        https://developers.facebook.com/docs/messenger-platform/send-messages/quick-replies
        Input:
            recipient_id: recipient id to send to
            message: message to send
        Output:
            Response from API as <dict>
        '''
        payload = {
            'recipient': {
                'id': recipient_id
            },
            'message': {
                'text': message,
                'quick_replies': quick_replies
            }
        }
        return self.send_raw(payload)

