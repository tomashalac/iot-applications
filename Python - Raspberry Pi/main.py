import config
import control
import IoT
from gpiozero import Button
import time
import RPi.GPIO as GPIO
import urllib
from threading import Thread
import helper


print("\n" * 5 + "Starting......." + "\n" * 2)
estadoGlobal = control.estado;
off_keyGlobal = control.off_key
Working = True
    
def ThreadedShadowUpdater():
    global estadoGlobal, Working, off_keyGlobal;
    print("[New Thread]: The thread that updates the shadow started")
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


helper.print_to_file()
helper.block_until_internet()



#GPIO
button = Button(17)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

#To set the initial state of the light
control.update_status()

print("Loading IoT")
IoT.start()

button.when_pressed = control.OnKey
button.when_released = control.OnKey

print("Starting the threads")

shadowUpdateThread = Thread(target=ThreadedShadowUpdater)
shadowUpdateThread.start()

InternetCheckerThread = Thread(target=helper.internet_checker_thread)
InternetCheckerThread.start()

helper.block_start_command_line(["on", "off", "switch", "off_key", "wakeup", "sleep"])

    
#On Quit
InternetCheckerThread.join(1)

Working = False
shadowUpdateThread.join()
print("The program was closed.")