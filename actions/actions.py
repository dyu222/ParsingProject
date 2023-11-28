# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


# Linked List Node Class
# If the class is too long, extract to a different python file

# To make the fetched recipe accessible to all actions in your Rasa chatbot
# Store the recipe information in the conversation's tracker.


class ActionSearchRecipe(Action):
    def name(self) -> Text:
        return "action_search_recipe"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Implement logic to search for a recipe
        # and return the recipe details.

        # This is how you access extracted entities
        # dish_name = tracker.get_slot("dish_name")

        recipe_details = "this will be the linkedlist recipe"

        # This is how bot responds to the User
        dispatcher.utter_message("User is asking for the recipe")

        # This is how you track history
        # return [SlotSet("recipe_details", recipe_details)]
        return []


class ActionProvideIngredientsList(Action):
    def name(self) -> Text:
        return "action_provide_ingredients_list"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Implement logic to search for the ingredients list
        # and return the ingredient list details.

        dispatcher.utter_message("User is asking for the ingredients list")

        return []


class ActionProvideIngredientDetails(Action):
    def name(self) -> Text:
        return "action_provide_ingredient_details"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Implement logic to give the details on a particular ingredient
        # and return the ingredient's details.

        dispatcher.utter_message(
            "User is asking for the an ingredient's detail")

        return []


class ActionProvideExplanation(Action):
    def name(self) -> Text:
        return "action_provide_explanation"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Implement logic to give external instructions on a question
        # and return the explanation or link or instructions

        dispatcher.utter_message("User is asking for help")

        return []


# Need to implement logic to inform the last step
class ActionProvideNextStep(Action):
    def name(self) -> Text:
        return "action_provide_next_step"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Implement logic to give the next step in the linked list
        # and return the next step details

        # Access the recipe details from the tracker's slot
        # recipe_details = tracker.get_slot("recipe_details")

        dispatcher.utter_message("User is asking for the next step")

        return []


# Need to implement logic to inform the first step (cannot go back past the first step)
class ActionProvidePreviousStep(Action):
    def name(self) -> Text:
        return "action_provide_previous_step"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Implement logic to give the previous step in the linked list
        # and return the previous step details

        # Access the recipe details from the tracker's slot
        # recipe_details = tracker.get_slot("recipe_details")

        dispatcher.utter_message("User is asking for the previous step")

        return []


class ActionRepeat(Action):
    def name(self) -> Text:
        return "action_repeat"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Implement logic to iterate the current step
        # and return the current step details

        # Access the recipe details from the tracker's slot
        # recipe_details = tracker.get_slot("recipe_details")

        dispatcher.utter_message("User is asking to repeat the current step")

        return []
