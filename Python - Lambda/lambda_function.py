import boto3
import json
import time
import sys

print('Loading function')


def respond(text, code = 200):
    return {
        'statusCode': code,
        'body': text,
        'headers': {
            'Content-Type': 'text/html',
        },
    }


def lambda_handler(event, context):
    if str(event["queryStringParameters"]["token"]) == "Fl401z1mzl074xj1lzdm4slslL2iO":
    
        command = str(event["queryStringParameters"]["command"])
        
        if(command == "on" or command == "off" or command == "switch"):
            client = boto3.client('iot-data')
            response = client.publish(
                topic='global',
                qos=1,
                payload='{"command": "'+command+'", "time": "'+str(int(round(time.time() * 1000)))+'"}'
            )
            return respond('good')
            
        if(command == "ping"):
            client = boto3.client('iot-data')
            response = client.publish(
                topic='global',
                qos=1,
                payload='{"command": "ping", "time": "'+str(int(round(time.time() * 1000)))+'"}'
            )
            shadowText = client.get_thing_shadow(thingName="Cuarto")["payload"].read()
            shadow = json.loads(shadowText)
            return respond(shadow["state"]["reported"]["estado"])
            
        return respond("invalid action")
    
    return respond("invalid login")        