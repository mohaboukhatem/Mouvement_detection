import pyrebase
import pytz
from datetime import datetime

from dotenv import load_dotenv
import os

load_dotenv()

credentiels = {
  "apiKey": os.getenv("API_KEY"),
  "authDomain": os.getenv("AUTH_DOMAIN"),
  "databaseURL": os.getenv("DATABASE_URL"),
  "projectId": os.getenv("PROJECT_ID"),
  "storageBucket": os.getenv("STORAGE_BUCKET"),
  "messagingSenderId": os.getenv("MESSAGING_SENDER_ID"),
  "appId": os.getenv("APP_ID"),
  "measurementId": os.getenv("MEASUREMENT_ID"),
}

def data_storage(distance,status,notifier) : 

  firebase = pyrebase.initialize_app(credentiels)
  storage = firebase.storage()
  database = firebase.database()
  
  quebec_tz = pytz.timezone('America/Toronto')

  print ("storage ... : ",distance)
  timestamp = datetime.now(pytz.utc).astimezone(quebec_tz).strftime("%Y-%m-%d %H:%M:%S")
  
  data = {
      "Distance (cm)": distance,
      "Date": timestamp,
      "Status": status,
      "Notification SMS": notifier ,
      "Numéro" : os.getenv("PHONE_NUMBER_RECEIVER") 

  }

  database.child("Capteur 1").push(data) 

