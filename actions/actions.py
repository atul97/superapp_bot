# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset, SlotSet

#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # authentic_user = tracker.get_slot("authentic_user") 
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

import requests
import psycopg2


class ActionSendOTP(Action):

    def name(self) -> Text:
        return "action_sendotp"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        authentic_user = tracker.get_slot("authentic_user") 
        if authentic_user !="True":
            try:
                
                number = tracker.get_slot("mobile")
                country_code = tracker.get_slot("country_code")
                url = "https://verificationapi-v1.sinch.com/verification/v1/verifications"
                payload=            {
                        "identity": {
                            "type": "number",
                            "endpoint": f"{country_code}{number}"},
                            "method": "sms"
                            }
                payload = str(payload)
                # payload="{\n  \"identity\": {\n  \"type\": \"number\",\n  \"endpoint\": \"+919873147995\"\n  },\n  \"method\": \"sms\"\n}"
                headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Basic MDM2YjIxM2UtMDdlOS00ZTNiLWJlOTAtMmI1NDRjMGI1OGU1Ok1jL1Z1MEFkbWtPQXUwc0dlNEo4blE9PQ=='
                }
                response = requests.request("POST", url, headers=headers, data=payload)
                dispatcher.utter_message(text=f"OTP sent to {country_code}{number}")
            except:
                print(response.json())
                dispatcher.utter_message(text="Something went wrong")
            

        return []

class ActionVerifyOTP(Action):

    def name(self) -> Text:
        return "action_verify_otp"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        authentic_user = tracker.get_slot("authentic_user") 
        if authentic_user !="True":
            try:
                otp = tracker.get_slot("otp")
                number = tracker.get_slot("mobile")
                country_code = tracker.get_slot("country_code")
                url = f"https://verificationapi-v1.sinch.com/verification/v1/verifications/number/{country_code}{number}"
                # payload="{ \"method\": \"sms\", \"sms\":{ \"code\": \"4163\" }}"
                payload={ 
                "method": "sms", 
                "sms":{ 
                    "code": f"{otp}" 
                    }
                    }
                payload = str(payload)

                headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Basic MDM2YjIxM2UtMDdlOS00ZTNiLWJlOTAtMmI1NDRjMGI1OGU1Ok1jL1Z1MEFkbWtPQXUwc0dlNEo4blE9PQ=='
                }
                response = requests.request("PUT", url, headers=headers, data=payload)

                print(response.json())
                response_json = response.json()
                dispatcher.utter_message(text=f"Verification Status:{response_json['status']}")
                if response_json['status'] == 'SUCCESSFUL':
                    return [SlotSet('authentic_user',"True")]
                else:
                    return [AllSlotsReset()]
            except:
                dispatcher.utter_message(text="Something went wrong")

        return []


class ActionCheckCustomer(Action):

    def name(self) -> Text:
        return "action_check_customer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:      
        

        authentic_user = tracker.get_slot("authentic_user") 

        if authentic_user =="True":
            conn = None
            try:
                print("-----------")
                mobile = tracker.get_slot("mobile")
                conn = psycopg2.connect(database ="sapp", user = "postgres",
                            password = "123456", host = "localhost", 
                            port = "5432")
                print("Connection Successful to PostgreSQL")

                cur = conn.cursor()
                
                query = f"""select * from customer where phone_number = '{mobile}';"""
                cur.execute(query)
                rows = cur.fetchall()


                
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                
                print(error)
            finally:
                if conn is not None:
                    conn.close()
                    print('Database connection closed.')
            if len(rows)==0:
                dispatcher.utter_message(text=f"No details found for user with contact: {mobile} ")

                buttons = []
                buttons.append({"title": "Add new customer" , "payload": "add_customer"})
                buttons.append({"title": "Explore More" , "payload": "explore_more"})
                dispatcher.utter_message(text="Want to add customer",buttons=buttons)
            else:
                dispatcher.utter_message(text="User existed")
                dispatcher.utter_message(template=f"utter_main_menu")
        else:
            dispatcher.utter_message(text=f"Please authenticate")

        return []

class ActionExistingOrder(Action):

    def name(self) -> Text:
        return "action_existing_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        authentic_user = tracker.get_slot("authentic_user") 

        if authentic_user =="True":
            conn = None
            try:
                print("-----------")
                mobile = tracker.get_slot("mobile")
                order_type = tracker.get_slot("order_type")
                order_type = order_type.lower()
                conn = psycopg2.connect(database ="sapp", user = "postgres",
                            password = "123456", host = "localhost", 
                            port = "5432")
                print("Connection Successful to PostgreSQL")

                cur = conn.cursor()
                
                query = f"""select * from orders where phone_number = '{mobile}' and order_type = '{order_type}';"""
                cur.execute(query)
                rows = cur.fetchall()
                for i in rows :
                    dispatcher.utter_message(text=f"Data: {i[2]} , Status: {i[3]}, Amount: {i[4]}")

                
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                
                print(error)
            finally:
                if conn is not None:
                    conn.close()
                    print('Database connection closed.')
            if len(rows)==0:
                dispatcher.utter_message(text=f"No details found for user with contact: {mobile}  for {order_type} order")
        else:
            dispatcher.utter_message(text=f"Please authenticate")
        return [SlotSet('order_type',None)]


class ActionAddCustomer(Action):

    def name(self) -> Text:
        return "action_add_customer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        authentic_user = tracker.get_slot("authentic_user") 

        if authentic_user =="True":        
            conn = None
            try:
                print("-----------")
                mobile = tracker.get_slot("mobile")
                customer_name = tracker.get_slot("customer_name")
                country_code = tracker.get_slot("country_code")
                conn = psycopg2.connect(database ="sapp", user = "postgres",
                            password = "123456", host = "localhost", 
                            port = "5432")
                print("Connection Successful to PostgreSQL")

                cur = conn.cursor()
                
                query = f"""insert into customer values('{customer_name}',{mobile},'{country_code}');"""
                cur.execute(query)

                conn.commit()


                
                cur.close()
                dispatcher.utter_message(template=f"utter_main_menu")
            except (Exception, psycopg2.DatabaseError) as error:
                
                print(error)
            finally:
                if conn is not None:
                    conn.close()
                    print('Database connection closed.')
        else:
            dispatcher.utter_message(text=f"Please authenticate")

        
        return [SlotSet('order_type',None)]