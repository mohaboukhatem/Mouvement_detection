import os
import smtplib

import yagmail
from twilio.rest import Client

from dotenv import load_dotenv
import os

load_dotenv()

def send_sms_message(message):


    account_sid = os.environ["TWILIO_ACCOUNT_SID"]

    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
        
    client = Client(account_sid, auth_token)

    try :
        client.messages.create(

            body=message, from_=os.getenv("PHONE_NUMBER_SENDER") , to = os.getenv("PHONE_NUMBER_RECEIVER") 

        )
        return "Envoyé"

    except :
        return "Non Envoyé" 
# send_sms_message()
