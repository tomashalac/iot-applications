import time
from datetime import datetime

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import logging
import os
import json
import sys

dir2 = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(level=logging.DEBUG, filename=dir2 + '/logger.log')
host = "a1y3ud7plgc0yl-ats.iot.us-east-1.amazonaws.com"


# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Incoming!")
    data = json.loads(message.payload)
    command = ""
    to = "client"

    if ("command" in data):
        command = data["command"]


    print("A message was received with the command=" + str(command))

    if command == "sleep":            
        os.system("shutdown.exe /h")
        
        print("Restarting IoT", flush=True)
        global myAWSIoTMQTTClient, connection
        try:
            myAWSIoTMQTTClient.configureConnectDisconnectTimeout(2)
            myAWSIoTMQTTClient.disconnect()
        except:
            print("Disconnect from IoT")
        
        myAWSIoTMQTTClient = None
        connection = None
        
        print("Wait for 10 seconds")
        time.sleep(10)
        start()
        print("Restart complete!")


def SendMSG(msg):
    connection.publish("global", str(msg), 0)
    print("The following message was sent: " + str(msg))


def start():
    logging.info("----- START OF THE IoT LOG -----")
    try:
        dir = os.path.dirname(os.path.realpath(__file__))
        rootCAPath = dir + "/root-CA.crt"
        certificatePath = dir + "/device.cert.pem"
        privateKeyPath = dir + "/device.private.key"

        streamHandler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        streamHandler.setFormatter(formatter)

        global myAWSIoTMQTTClient, host
        myAWSIoTMQTTClient = AWSIoTMQTTShadowClient("basicPubSub")
        myAWSIoTMQTTClient.configureEndpoint(host, 8883)
        myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

        # AWSIoTMQTTClient connection configuration
        myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
        myAWSIoTMQTTClient.configureConnectDisconnectTimeout(30)
        myAWSIoTMQTTClient.configureMQTTOperationTimeout(10)

        # Connect and subscribe to AWS IoT
        myAWSIoTMQTTClient.connect(10)

        global connection
        connection = myAWSIoTMQTTClient.getMQTTConnection()
        connection.configureAutoReconnectBackoffTime(1, 32, 20)
        connection.configureDrainingFrequency(2)  # Draining: 2 Hz
        connection.configureConnectDisconnectTimeout(30)  # 10 sec
        connection.configureMQTTOperationTimeout(10)  # 5 sec

        connection.subscribe("global", 1, customCallback)

        SendMSG('{"to": "server", "client-id": "2", "info": "start-up"}')
    except Exception as e:
        logging.exception("Error IoT: " + str(e))
        print("Error IoT: " + str(e))
        import traceback
        traceback.print_exc()

# Fin de la funcion
old_f = sys.stdout


class F:
    def write(self, x):
        if (str(x) != "\n"):
            old_f.write("[" + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "]: " + str(x))
            old_f.flush()
        else:
            old_f.write(x)

    def flush(self):
        old_f.flush()


sys.stdout = F()

print("Se inicio control!")
start()

while(True):
    time.sleep(100)

print("IoT cargado!")
