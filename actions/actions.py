# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
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

# actions.py
from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, EventType
import requests

class ActionGetApod(Action):

    def name(self) -> Text:
        return "action_get_apod"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        api_key = 'Ndjn0d1vUB1VYaNHcsAK4j9U8htObMUXV2AR3m5s'
        date = tracker.get_slot('date')

        if not date:
            dispatcher.utter_message(text="Please provide a date in the format YYYY-MM-DD.")
            return []

        url = f'https://api.nasa.gov/planetary/apod?api_key={api_key}&date={date}'
        response = requests.get(url)
        data = response.json()

        if data:
            title = data.get('title')
            explanation = data.get('explanation')
            image_url = data.get('url')
            dispatcher.utter_message(text=f"Title: \n{title}\n\nExplanation: \n{explanation}\n\n",image=f"\n{image_url}")
        else:
            dispatcher.utter_message(text="Sorry, I couldn't fetch the data from NASA at this time.")

        return [SlotSet("date", None)]
