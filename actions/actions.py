# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from recipe import Step, remove_leading_space

import re
import requests

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
        dish_name = tracker.get_slot("dish_name")
        processed_dish_name = '+'.join([word.capitalize() for word in dish_name.split()])

        #make api call
        api_url = "https://themealdb.com/api/json/v1/1/search.php?s=" + processed_dish_name
        response = requests.get(api_url)
        if response.status_code == 200:
            recipe = response.json()['meals'][0]
        else:
            print(f"Error: {response.status_code}")
            print("Sorry, we are not abie to find the recipe for ", dish_name)
            return []

        # get info from recipe (json)
        instructions = re.split(r'\.\r\n|\.',recipe['strInstructions'])
        recipe_ingredients = {} #[]
        for i in range(1,20):
            ingredient = recipe['strIngredient'+str(i)]
            if ingredient == '' or ingredient == None:
                continue
            recipe_ingredients[ingredient.lower()] = recipe['strMeasure'+str(i)].lower()

        #initializing the recipe (linked list of step objects)
        dish_head = Step()
        prev_step = dish_head
        for instruction in instructions:
            # print(instruction)
            instruction = remove_leading_space(instruction)
            curr_step = Step(instruction, recipe_ingredients, prev_step)
            prev_step.next = curr_step
            prev_step = curr_step

       

        recipe_details = dish_head
        message = "Okay, I find the recipe for " + dish_name + ".\n"
        message += "Here are all the steps: \n"
        message += instructions

        # This is how bot responds to the User
        dispatcher.utter_message(message)


        # This is how you track history
        return [SlotSet("recipe_details", recipe_details)]
        # return []


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
