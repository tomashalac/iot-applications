import helper
import datetime
import lambda_function

# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Indicates action."
    reprompt_text = "Indicates action."
    return helper.build_response(session_attributes, helper.build_speechlet_response(
        card_title, speech_output, reprompt_text, False))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = ""
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return helper.build_response({}, helper.build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def basic_light(intent, session):
    slot = intent["slots"]
    my_state = ""
    if "State" in slot and "value" in slot["State"]:
        my_state = slot['State']
    if "pcState" in slot and "value" in slot["pcState"]:
        my_state = slot['pcState']
    
    my_state = my_state["value"]
    print(my_state)
        
    if my_state == "on" or my_state == "off":
        speech_output = "Light is now " + my_state
        reprompt_text = "Light is now " + my_state
        publish(my_state)
    elif my_state == "sleep" or my_state == "wake up":
        speech_output = "The pc is now " + my_state
        reprompt_text = "The pc is now " + my_state
        publish(my_state)
    else:
        speech_output = "Please try again."
        reprompt_text = "Please try again."
    return helper.build_response({}, helper.build_speechlet_response(
        intent['name'], speech_output, reprompt_text, True))

def publish(command):
    lambda_function.client.publish(
        topic='global',
        qos=1,
        payload='{"command": "'+command+'", "time": "'+datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')+'"}')

def switch_light(intent, session):
    import lambda_function
    speech_output = "Light is switched"
    reprompt_text = "Light is switched"
    publish("switch")
    return helper.build_response({}, helper.build_speechlet_response(
        intent['name'], speech_output, reprompt_text, True))