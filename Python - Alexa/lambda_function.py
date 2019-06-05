from __future__ import print_function
import events
import boto3

client = boto3.client('iot-data')
# --------------- Main handler ------------------

def lambda_handler(event, context):
    print (str(event) + " context: " + str(context));

    if event['session']['new']:
        events.on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return events.on_launch(event['request'], event['session'])

    elif event['request']['type'] == "IntentRequest":
        return events.on_intent(event['request'], event['session'])

    elif event['request']['type'] == "SessionEndedRequest":
        return events.on_session_ended(event['request'], event['session'])