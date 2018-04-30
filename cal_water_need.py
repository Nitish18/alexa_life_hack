import json
import random

def lambda_handler(event, context):
    if (event["session"]["application"]["applicationId"] !=
            "amzn1.ask.skill.5eaacfac-6380-4f60-ba57-48b0469622e6"):
        raise ValueError("Invalid Application ID")
    
    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])

def on_session_started(session_started_request, session):
    print "Starting new session."

def on_launch(launch_request, session):
    return get_welcome_response()

def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    # custom intents
    if intent_name == "intro":
        return get_intro()

    elif intent_name == "myWaterNeeds":
        return cal_water_need(intent)

    elif intent_name == "myWaterTips":
        return give_water_tips()
        
    # predefined intents
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    print "Ending session."
    # Cleanup goes here...

def handle_session_end_request():
    card_title = "WATERREMINDO - Thanks"
    speech_output = "Thank you for using Water Remindo. See you next time!"
    should_end_session = True
    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))

def get_welcome_response():
    session_attributes = {}
    card_title = "WATER REMINDO"
    speech_output = "Welcome to the Alexa Water Remindo skill. " \
                    "I will tell you about, how much water you should drink daily" 
                    
    reprompt_text = "Please tell me your weight in pounds" \
                    "for example 100 pounds"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_intro():
    session_attributes = {}
    card_title = "Water Remindo Status"
    reprompt_text = ""
    should_end_session = False
    speech_output = "Hello, water remindo will tell you about your daily water intake requirement. You have to tell alexa your weight and age, it will calculate how much water you need to drink daily."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def give_water_tips():
    session_attributes = {}
    card_title = "Water Remindo tips"
    reprompt_text = ""
    should_end_session = False
    water_tips = get_random_tips()
    speech_output = "some tips are : " + str(water_tips) 
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))   


def get_random_tips():
    random_tip_list = [
            "ADD FLAVOR TO YOUR PITCHER",
            "DRINK A GLASS AFTER EVERY BATHROOM BREAK",
            "USE AN APP TO TRACK YOUR CUPS",
            "GET A HIGH-TECH WATER BOTTLE",
            "DILUTE SUGARY DRINKS WITH WATER AND ICE",
            "CHOOSE SPARKLING OR MINERAL WATER OVER SODA",
            "STICK TO A ONE-TO-ONE RULE WHEN DRINKING ALCOHOL",
            "USE A MARKED WATER BOTTLE",
            "Whenever you feel a hunger pang, drink a glass of water first",
            "Keep an open water bottle or glass next to you while you work",
            "Keep Your Water Close",
            "Drink Water Right When You Wake Up"
        ]
    return random.choice(random_tip_list)
        
def cal_water_need(intent):
    session_attributes = {}
    card_title = "Calculating daily water requirement"
    speech_output = "sorry, please enter a valid weight value. Try again"
    reprompt_text = "sorry, please enter a valid weight value. Try again"
    should_end_session = True

    if "slots" in intent and "weight" in intent["slots"] and "unit" in intent["slots"]:
        my_weight = intent["slots"]["weight"].get('value')
        weight_unit = intent["slots"]["unit"].get('value')
        if my_weight and weight_unit:
            my_weight = int(my_weight)
            if my_weight < 0:
                return build_response(session_attributes, build_speechlet_response(
                    card_title, speech_output, reprompt_text, should_end_session))
            
            my_water_intake = cal_water_intake(my_weight, weight_unit)

            if not my_water_intake:
                return build_response(session_attributes, build_speechlet_response(
                    card_title, speech_output, reprompt_text, should_end_session))

            speech_output = "You should daily drink " + str(my_water_intake[0]) + " ounces of water or " + str(my_water_intake[1]) + " litres of water on a daily basis."
            should_end_session = False
            reprompt_text = "want to try again"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def cal_water_intake(weight,unit):
   
    if str(unit) in ["pounds","pound"]:    
        a = weight / 2
        ounce_vol = round(a * 1.5,1)
        lit_vol = round(ounce_vol * 0.029573,1)
        return [ounce_vol,lit_vol]
    elif str(unit) in ["kilos","kgs","kilograms"]:
        a = weight * 0.3
        deci_litre = a * 1.5
        
        lit_vol = round(deci_litre * 0.1,1)
        ounce_vol = round(lit_vol * 33.8,1)
        return [ounce_vol,lit_vol]
    return None         


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }