#!/usr/bin/env python3

from Notifier import send_sms_message
from database import data_storage

import RPi.GPIO as GPIO
import time


TRIG = 11
ECHO = 12

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

def distance_calculator():

    GPIO.output(TRIG, 0)
    time.sleep(0.000002)

    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)

    while GPIO.input(ECHO) == 0:
        a = 0
    time1 = time.time()
    while GPIO.input(ECHO) == 1:
        a = 1
    time2 = time.time()

    during = time2 - time1
    return round (during * 340 / 2 * 100, 2)

def loop():

    i, j= 0, 0
    while True:
        distance = distance_calculator()
        
        if distance > 100:
            message = f" Aucun objet détecté ({distance} cm)"
            print (message)
            i = 0
            j = 0
        
        
        elif distance > 50 and distance < 100:
            message = f"Un Objet Detecté moin de 1 mètre ({distance} cm) de votre maison"
            print (message)
            i += 1
            j = 0
    
        else :
            message = f" Un Objet Detecté moin de 50 cm ({distance} cm) de votre maison"
            print (message)
            i = 0
            j += 1

        if i == 1 or j == 1 :
            notifier = send_sms_message(message)
            print("sms send")

        data_storage(distance,message,notifier = None)

        time.sleep(1)
        

def destroy():
    GPIO.cleanup()

if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
    

