import pyrebase
from datetime import datetime

credentiels = {
  "apiKey": "AIzaSyBJh1FatYuGHq581ueRMA-kvkl1t6_xgNA",
  "authDomain": "mti840-779c4.firebaseapp.com",
  "databaseURL": "https://mti840-779c4-default-rtdb.firebaseio.com",
  "projectId": "mti840-779c4",
  "storageBucket": "mti840-779c4.firebasestorage.app",
  "messagingSenderId": "520901661043",
  "appId": "1:520901661043:web:0d18f3853eda5cae20b506",
  "measurementId": "G-VZ4XWJK07T"
}

def data_storage(distance,status,notifier) : 

  firebase = pyrebase.initialize_app(credentiels)
  storage = firebase.storage()
  database = firebase.database()
  
  print ("storage ... : ",distance)
  timestamp = datetime.now().isoformat()  

  data = {
      "Distance": distance,
      "Time": timestamp,
      "Status": status,
      "SMS Sending": notifier ,
      "To" : "+14389293674"

  }

  database.child("Capteur 1").push(data) 

