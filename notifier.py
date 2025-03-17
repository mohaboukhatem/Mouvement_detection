import os
import smtplib

import yagmail
from twilio.rest import Client

def send_sms_message(message):


    #account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    account_sid = "ACdf1e75c9c669c2064e92b979246cfc97"

    #auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    auth_token = "4f816ef8e7c7f726b284831a6ebc146e"
    receiver = "+14389293674"
    client = Client(account_sid, auth_token)

    try :
        client.messages.create(

            body=message, from_="+17404802451", to=receiver

        )
        return "Envoyé"

    except :
        return "Non Envoyé" 
# send_sms_message()
