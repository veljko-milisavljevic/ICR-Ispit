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

        print("Preporuka!")

        if len(data) >= 3:
            bot_response = {
                "type": "toy_list",
                "data": data[-3:]
            }
            dispatcher.utter_message(text='Evo nekih preporuka', attachment=bot_response)
        else:
            dispatcher.utter_message(text='Izvini, nisam uspeo ništa da pronađem') 
        return []

class ActionSearchToys(Action):

    def name(self) -> Text:
        return "action_search_toys"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        criteria=tracker.get_slot("search_criteria")

        url = "https://toy.pequla.com/api/toy"
        rsp = requests.get(url)
        all_toys = rsp.json()

        print("Pretraga!")

        if not criteria:
            criteria = tracker.latest_message.get('text')

        print("Kriterijum: " + criteria)
        print(all_toys[0])

        filtered_toys = [
            toy for toy in all_toys 
            if criteria.lower() in toy.get('name', '').lower() 
            or criteria.lower() in toy.get('description', '').lower()
            or criteria.lower() in toy.get('type', {}).get('name', '').lower()
        ]

        if filtered_toys:
            dispatcher.utter_message(
                    text='Evo šta sam pronašao',
                    attachment={
                    "type": "toy_list",
                    "data": filtered_toys
                }
                )
        else:
            dispatcher.utter_message(text='Izvinite, nisam uspeo da pronađem ništa za vašu pretragu')

        return []