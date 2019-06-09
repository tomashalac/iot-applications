import time
from time import sleep
import RPi.GPIO as GPIO
import IoT
import os
import json
from wakeonlan import send_magic_packet

#The light always starts off, to avoid inconveniences due to power outages at night
estado = False

last = 0
off_key = False

def get_time():
    return int(time.time() * 1000)

def callBack(command = "switch"):
    global estado, last, off_key
    estadoInicial = estado
    
    if last >= get_time():
        return
    last = get_time() + 300

    if command == "switch":
        estado = not estado
    elif command == "off":
        estado = False
    elif command == "on":
        estado = True
    elif command == "off_key":
        off_key = not off_key
    elif command == "wake up":
        send_magic_packet('B0-6E-BF-CD-A6-C9')
    else:
        print "Error with the command: " + str(command)
    print "Final state: " + str(command)
    update_status()

def OnKey():
    if off_key == False:
        callBack()
    
def update_status():
    global estado
    if not estado:
        GPIO.output(18, GPIO.HIGH)
        if(os.path.isfile("on")):
            os.remove("on")
    else:
        GPIO.output(18, GPIO.LOW)
        file = open("on","w+")
        file.close()

def customShadowCallback_Update(payload, responseStatus, token):
    if responseStatus == "timeout":
        print("Update request " + token + " time out!")
    if responseStatus == "accepted":
        payloadDict = json.loads(payload)
        print("The shadow was updated to the state: " + str(payloadDict["state"]))
    if responseStatus == "rejected":
        print("Update request " + token + " rejected!")