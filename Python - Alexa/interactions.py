import helper
import datetime

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
    import lambda_function
    my_state = intent['slots']['State']['value']
    if my_state == "on" or my_state == "off":
        speech_output = "Light is now " + my_state
        reprompt_text = "Light is now " + my_state
        lambda_function.client.publish(
    topic='global',
    qos=1,
    payload='{"command": "'+my_state+'", "time": "'+datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')+'"}')
    else:
        speech_output = "Please try again."
        reprompt_text = "Please try again."
    return helper.build_response({}, helper.build_speechlet_response(
        intent['name'], speech_output, reprompt_text, True))


def switch_light(intent, session):
    import lambda_function
    speech_output = "Light is switched"
    reprompt_text = "Light is switched"
    lambda_function.client.publish(
    topic='global',
    qos=1,
    payload='{"command": "switch", "time": "'+datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')+'"}')
    return helper.build_response({}, helper.build_speechlet_response(
        intent['name'], speech_output, reprompt_text, True))