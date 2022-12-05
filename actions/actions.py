# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

import requests


class ActionSendOTP(Action):

    def name(self) -> Text:
        return "action_sendotp"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        number = '9953635285'
        url = "https://verificationapi-v1.sinch.com/verification/v1/verifications"
        payload=            {
                "identity": {
                    "type": "number",
                    "endpoint": f"+91{number}"},
                    "method": "sms"
                    }
        payload = str(payload)
        # payload="{\n  \"identity\": {\n  \"type\": \"number\",\n  \"endpoint\": \"+919873147995\"\n  },\n  \"method\": \"sms\"\n}"
        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic MDM2YjIxM2UtMDdlOS00ZTNiLWJlOTAtMmI1NDRjMGI1OGU1Ok1jL1Z1MEFkbWtPQXUwc0dlNEo4blE9PQ=='
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.json())
        dispatcher.utter_message(text="Hello World!")

        return []

class ActionVerifyOTP(Action):

    def name(self) -> Text:
        return "action_verify_otp"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        code = '1100'
        url = "https://verificationapi-v1.sinch.com/verification/v1/verifications/number/+919873147995"
        # payload="{ \"method\": \"sms\", \"sms\":{ \"code\": \"4163\" }}"
        payload={ 
        "method": "sms", 
        "sms":{ 
            "code": f"{code}" 
            }
            }
        payload = str(payload)
        
        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic MDM2YjIxM2UtMDdlOS00ZTNiLWJlOTAtMmI1NDRjMGI1OGU1Ok1jL1Z1MEFkbWtPQXUwc0dlNEo4blE9PQ=='
        }
        response = requests.request("PUT", url, headers=headers, data=payload)

        print(response.json())
        dispatcher.utter_message(text="Hello World!")

        return []