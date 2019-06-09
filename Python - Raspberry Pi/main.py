import control
import IoT
from gpiozero import Button
import time
import RPi.GPIO as GPIO
import os
import sys
import urllib2
from datetime import datetime
from threading import Thread


print "\n\n\n\n\n\n\n\n\n\n\n\n\nStarting.......\n\n"
estadoGlobal = control.estado;
off_keyGlobal = control.off_key
Working = True
    
def ThreadedShadowUpdater():
    global estadoGlobal, Working, off_keyGlobal;
    print "[New Thread]: The thread that updates the shadow started"
    while Working:
        if(control.estado != estadoGlobal or control.off_key != off_keyGlobal):
            estadoText = "error"
            if(control.estado):
                estadoText = "on"
            else:
                estadoText = "off"
            
            IoT.deviceShadowHandler.shadowUpdate(
            '{"state":{"reported":{"estado":"'+ str(control.estado) +
            '", "estadoText":"' + estadoText + 
            '", "off_key": "' + str(control.off_key) + 
            '"}}}', control.customShadowCallback_Update, 5)
            
            estadoGlobal = control.estado
            off_keyGlobal = control.off_key
        
        #espero 
        time.sleep(0.5)
        
def InternetChecker():
    print "[New Thread]: The thread that verifies the internet connection was started"
    while True:
        try:
            response = urllib2.urlopen("http://www.google.com",timeout=10)
            #if I have a connection I can wait about 5 mins
            time.sleep(60*5)
        except urllib2.URLError:
            print("It was detected that there is no internet connection.")
        
        time.sleep(60)
        
#Fin de la funcion
old_f = sys.stdout
class F:
    def write(self, x):
        if(str(x) != "\n"):
            old_f.write("[" + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "]: " + str(x))
            old_f.flush()
        else:
            old_f.write(x)
    def flush(self):
        old_f.flush()

sys.stdout = F()

print "The control system was started!"


while True:
	print("Waiting until there is an internet connection to continue")
        try:
            response = urllib2.urlopen('http://www.google.com.ar',timeout=10)
            print("It was connected to internet!")
            break
        except urllib2.URLError:
            print("The device does not have internet")
            time.sleep(1)
            pass

#GPIO
button = Button(17)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

#To set the initial state of the light
control.update_status()

print "Loading IoT"
IoT.start()

button.when_pressed = control.OnKey
button.when_released = control.OnKey

print "Starting the threads"

shadowUpdateThread = Thread(target = ThreadedShadowUpdater)
shadowUpdateThread.start()

InternetCheckerThread = Thread(target = InternetChecker)
InternetCheckerThread.start();

comando = ""
print('Enter a command("quit", "on", "off", "switch", "off_key"): \n\n')
while(comando != "quit"):
    if(comando == "on" or comando == "off" or comando == "switch" or comando == "off_key"):
        control.callBack(comando)
    elif(comando != ""):
        print("Command not found: " + comando)
    try:
        comando = raw_input()
    except EOFError:
        print ("We are in an interface, which does not allow to have text entries")
        while True:
            time.sleep(10000)
        


    
#On Quit
InternetCheckerThread.join(1)

Working = False
shadowUpdateThread.join()
print("The program was closed.")