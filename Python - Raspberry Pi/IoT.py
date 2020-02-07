from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import logging
import os
import json
import sys
import control
import config

thisDir = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(level=logging.DEBUG, filename=thisDir+'/logger.log')


# Custom MQTT message callback
def customCallback(client, userdata, message):
    data = json.loads(message.payload.decode("utf8"))
    command = ""
    to = "client"
    
    if "command" in data:
        command = data["command"]
        
    if "to" in data:
        to = data["to"]
    
    if to == "server":
        return

    print("A message was received with the command=" + str(command))
    sys.stdout.flush()

    if command == "ping":
        pong()
    else:
        control.callBack(command)


def pong():
    SendMSG('{"command": "pong", "estado": "' + str(control.estado) + '", "to": "server", "off_key": "' + str(control.off_key) + '"}')


def SendMSG(msg):
    Connection.publish("global",  str(msg), 0)
    print("The following message was sent:", msg)


def start():
    print("Connecting IoT, endpoint:" + str(config.iot_endpoint))
    logging.info("----- START OF THE IoT LOG -----")
    try:
        dir = os.path.dirname(os.path.realpath(__file__))

        rootCAPath = dir + "/root-CA.crt"
        certificatePath = dir + "/" + config.name +".cert.pem"
        privateKeyPath = dir + "/" + config.name + ".private.key"

        streamHandler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        streamHandler.setFormatter(formatter)

        global myAWSIoTMQTTClient
        myAWSIoTMQTTClient = AWSIoTMQTTShadowClient(config.name)
        myAWSIoTMQTTClient.configureEndpoint(config.iot_endpoint, 8883)
        myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
        
        # AWSIoTMQTTClient connection configuration
        myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
        myAWSIoTMQTTClient.configureConnectDisconnectTimeout(30)  # 30 sec
        myAWSIoTMQTTClient.configureMQTTOperationTimeout(10)  # 5 sec
        

        # Connect and subscribe to AWS IoT
        myAWSIoTMQTTClient.connect(10)
        
        print("Creating shadows")
        global deviceShadowHandler

        deviceShadowHandler = myAWSIoTMQTTClient.createShadowHandlerWithName(config.name, True)
        
        global Connection
        Connection = myAWSIoTMQTTClient.getMQTTConnection()
        Connection.configureAutoReconnectBackoffTime(1, 32, 20)
        Connection.configureDrainingFrequency(2)  # Draining: 2 Hz
        Connection.configureConnectDisconnectTimeout(30)  # 30 sec
        Connection.configureMQTTOperationTimeout(10)  # 10 sec
          
        Connection.subscribe("global", 1, customCallback)
        
        
        SendMSG('{"to": "server", "client-id": "1", "info": "start-up"}')
        
        control.update_status()
        
    except Exception as e:
        logging.exception("Error IoT: " + str(e))
        print("Error IoT: ", e)
        import traceback
        traceback.print_exc()
