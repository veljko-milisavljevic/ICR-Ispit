from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests


class ActionLatestToys(Action):

    def name(self) -> Text:
        return "action_latest_toys"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        url = "https://toy.pequla.com/api/toy"
        rsp = requests.get(url)
        data = rsp.json()

        if len(data) >= 3:
            dispatcher.utter_message(text='Here are some recommendations', attachment=data[-3:])
        else:
            dispatcher.utter_message(text='Not enought toys found') 
        return []
