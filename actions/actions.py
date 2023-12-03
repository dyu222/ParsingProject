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
import json
import random
import traceback # for debugging

# Linked List Node Class
# If the class is too long, extract to a different python file

# To make the fetched recipe accessible to all actions in your Rasa chatbot
# Store the recipe information in the conversation's tracker.

dish_head = None
current_step = None
specific_step = dish_head

################################################################################
# Some helpers:


def get_entity(tracker):
    if "entities" in tracker.latest_message:
        return tracker.latest_message["entities"][0]["entity"]
    else:
        return None


def get_entity_value(tracker):
    if "entities" in tracker.latest_message:
        if tracker.latest_message["entities"]:
            return tracker.latest_message["entities"][0]["value"]
    else:
        return None


def get_intent(tracker):
    if "intent" in tracker.latest_message:
        if "name" in tracker.latest_message["intent"]:
            return tracker.latest_message["intent"]["name"]
    else:
        return None

############################################################################
# some more lexes that i think works better here than in recipe.py
meat_lex = {'beef', 'pork', 'chicken', 'lamb', 'turkey', 'fish', 'shrimp', 'bacon', 'sausage', 'ham', 'steak', 'veal', 'venison', 'mutton', 'rabbit', 'duck', 'goose',
    'anchovy', 'calamari', 'clams', 'crab', 'lobster', 'mussels', 'octopus', 'oysters', 'scallops', 'squid', 'tilapia', 'catfish', 'trout', 'salmon', 'tuna',
    'sardines', 'haddock', 'cod', 'swordfish', 'perch', 'crayfish', 'snapper', 'bass', 'carp', 'marlin', 'halibut', 'pike', 'snail', 'frog', 'turtle', 'escargot',
    'buffalo', 'bison', 'elk', 'horse', 'boar', 'quail', 'pigeon', 'pheasant', 'emu', 'kangaroo', 'alligator', 'turtle', 'squab', 'veal', 'mahi-mahi'}

vegetarian_alternatives = [
    'plant-based mock meat', 'lentils', 'portobello mushrooms',
    'plant-based impossible meat', 'jackfruit', 'tempeh bacon', 'tofu', 'seitan', 'chickpeas', 
    'lentils', 'eggplant', 'quinoa', 'tofu', 'eggplant', 'zucchini', 'king oyster mushrooms',
    'smoked tofu', 'eggplant strips', 'mushroom and lentil mixtures', 'chickpea or black bean sausages',
    'tempeh', 'portobello mushrooms', 'eggplant or cauliflower steaks',
    'artichoke hearts', 'textured vegetable protein (TVP)', 'soy curls', 'black bean burgers', 'sweet potato'
]



################################################################################


class ActionSearchRecipe(Action):
    def name(self) -> Text:
        return "action_search_recipe"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Implement logic to search for a recipe
        # and return the recipe details.
        global dish_head
        message = f"""
        Sorry, this recipe was not found.
        """

        # This is how you access extracted entities
        # dish_name = tracker.get_slot("dish_name")
        dish_name = get_entity_value(tracker)
        print("dish name: ", dish_name)
        if not dish_name:
            dispatcher.utter_message(text=message)
            return []

        processed_dish_name = '+'.join([word.capitalize()
                                       for word in dish_name.split()])

        message = f"""
        Sorry, this recipe was not found online.
        """

        # make api call
        api_url = "https://themealdb.com/api/json/v1/1/search.php?s=" + processed_dish_name
        response = requests.get(api_url)
        if response.status_code == 200:
            # throws an ERROR WHEN NOTHING IN 'meals
            if response.json()['meals'] == None:
                dispatcher.utter_message(text=message)
                return []

            recipe = response.json()['meals'][0]
            dispatcher.utter_message(
                "Searching for " + dish_name + " recipe\n")
        else:
            # print(f"Error: {response.status_code}")
            # print("Sorry, we are not able to find the recipe for ", dish_name)
            dispatcher.utter_message(text=message)
            # return [SlotSet("recipe_details", None)]
            return []

        # get info from recipe (json)
        instructions = re.split(r'\.\r\n|\.', recipe['strInstructions'])
        recipe_ingredients = {}  # []
        for i in range(1, 20):
            ingredient = recipe['strIngredient'+str(i)]
            if ingredient == '' or ingredient == None:
                continue
            recipe_ingredients[ingredient.lower(
            )] = recipe['strMeasure'+str(i)].lower()

        # initializing the recipe (linked list of step objects)
        dish_head = Step()
        prev_step = dish_head
        instructions_text = ""
        print("recipe_ingredients: ", recipe_ingredients)
        for instruction in instructions:

            # print(instruction)
            instruction = remove_leading_space(instruction)
            instruction = instruction.lstrip('\t')
            if len(instruction) < 2:
                continue
            instructions_text += ("\t" + instruction + "\n")
            curr_step = Step(instruction, recipe_ingredients, prev_step)
            print("ingredients: ", curr_step.ingredients)
            prev_step.next = curr_step
            prev_step = curr_step

        # recipe_details = dish_head.to_dict()

        message = f"""This is the recipe for {dish_name}.\nHere are all the steps:\n\n{instructions_text}\n"""

        # This is how bot responds to the User
        dispatcher.utter_message(text=message)
        global current_step
        current_step = dish_head.next

        global specific_step
        specific_step = dish_head

        # This is how you track history
        return []
        # return [SlotSet("recipe_details", json.dumps(recipe_details))]
        # return []


# ask for the ingredient list of the whole recipe
class ActionProvideIngredientsList(Action):
    def name(self) -> Text:
        return "action_provide_ingredients_list"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Implement logic to search for the ingredients list
        # and return the ingredient list details.
        global dish_head
        message = "You haven't told me what dish you want to cook today."
        # print("dish head: ", dish_head)
        if dish_head != None:
            # print("dish head.next: ", dish_head.next)
            # print(list(dish_head.next.recipe_ingredients))
            ingredients = list(dish_head.next.recipe_ingredients)
            if not ingredients:
                message = "Sorry, I don't know what ingredients you need"
            else:
                message = "The ingredients are " + ", ".join(ingredients)
        dispatcher.utter_message(message)

        # return [SlotSet("ingredients_list", message)]
        return []


# ask for the list of ingredients in a particular step
class ActionProvideIngredientInStep(Action):
    def name(self) -> Text:
        return "action_provide_ingredients_in_step"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:

        message = "Please select a recipe first!"
        global dish_head
        if dish_head != None:
            message = "There are no ingredients in this step."
            global current_step
            ingredients = list(current_step.ingredients)
            if not ingredients:
                message = "Sorry, I don't know what ingredients you need"
            else:
                message = "Here are the ingredients in this step:\n" + ingredients
        dispatcher.utter_message(message)
        return []


# ask for the quantity of a particular ingredient at a particular step
class ActionProvideIngredientDetails(Action):
    def name(self) -> Text:
        return "action_provide_ingredient_details"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Implement logic to give the details on a particular ingredient
        # and return the ingredient's details.
        # ingredient_name = tracker.get_slot("ingredient_name")
        ingredient_name = get_entity_value(tracker)
        message = "Sorry I don't know how much of this ingredient you should put."
        if ingredient_name != None:
            global current_step
            if current_step == None:
                dispatcher.utter_message(text="Please select a recipe first!")
                return []
            if ingredient_name in current_step.recipe_ingredients:
                measurement_string = current_step.recipe_ingredients[ingredient_name]
                # parts = measurement_string.split('of', 1)
                # m = parts[0].strip() if len(parts) > 0 else measurement_string.strip()
                message = "You should put " + measurement_string + " of " + ingredient_name

        dispatcher.utter_message(message)

        return []


# Derek will take this one
class ActionProvideExplanation(Action):
    def name(self) -> Text:
        return "action_provide_explanation"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Implement logic to give external instructions on a question
        # and return the explanation or link or instructions
        global current_step
        # logic:
        # take the latest message and check to see if it contains this or that, and if the string is short enough (less than 5 words or smth)
        message = "sorry, I do not know what you are asking about, please ask again"
        search_url = ""
        try:
            text = tracker.latest_message['text']
            print("provide explanation text: ", text)
            question = ""
            print("current step text: ", current_step.text)
            print("current step text: ", current_step.methods)
            if len(text) <= 20:  # short text
                if "this" in text or "that" in text:  # assume its: how do i do this??? maybe make this better later?
                    question = "how to " + current_step.text
                else:
                    question = text
            else:  # just return question url
                question = text
            print("question: ", question)
            question = question.split(' ')
            print("question: ", question)
            if "how" in question:
                search_url = "https://www.youtube.com/results?search_query=" + \
                    "+".join(question)
            else:
                search_url = "https://www.google.com/search?q=" + \
                    "+".join(question)
            print("search url: ", search_url)
        except:
            pass

        if search_url:
            message = "Here is a link to a search for your question that may give you more information: " + search_url
        dispatcher.utter_message(message)
        # if this matches, then take the current step recipe details and return the google query url for it
        # if this doesnt match, then take the detailed question and return the query for the specific question
        # dispatcher.utter_message("User is asking for help")

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
        global current_step
        if current_step == None:
            dispatcher.utter_message(text="Please select a recipe first!")
            return []
        if current_step.next == None:
            dispatcher.utter_message(text="This is already the final step!")
            return []
        current_step = current_step.next  # we are actually moving to the next step!
        if current_step.text:
            step_text = "The next step is: " + current_step.text
        else:
            step_text = "This is the entire recipe!"
            current_step = current_step.prev

        dispatcher.utter_message(text=step_text)

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
        if current_step == None:
            dispatcher.utter_message(text="Please select a recipe first!")
            return []
        if current_step.prev.text == None:
            step_text = "There was no last step!"
        else:
            step_text = "The last step was: " + current_step.prev.text

        dispatcher.utter_message(text=step_text)

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
        if current_step == None:
            dispatcher.utter_message(text="Please select a recipe first!")
            return []

        step_text = "This step is: " + current_step.text

        dispatcher.utter_message(text=step_text)

        return []


class ActionSpecificStep(Action):
    def name(self) -> Text:
        return "action_specific_step"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Implement logic to get a specific step
        # and return the specific step details
        global specific_step
        step_number = get_entity_value(tracker)

        # dispatcher.utter_message(
        #     text=f"i am in action specific step{step_number}")

        if not step_number:
            dispatcher.utter_message(
                text="Which step of the recipe are you asking for?")
            return []

        if specific_step == None:
            dispatcher.utter_message(text="Please select a recipe first!")
            return []
        try:
            step_number = int(step_number)
            current_step = specific_step

            for i in range(2, step_number + 2):
                current_step = current_step.next

                if current_step.text:
                    pass
                else:
                    dispatcher.utter_message(
                        text=f"The recipe only has {i} steps.")
                    return []
        except:
            dispatcher.utter_message(
                text=f"The recipe does not have that many steps.")
            return []

        text = f"Step {step_number} is: " + current_step.text

        dispatcher.utter_message(
            text=text)

        return []


# what temperature? -Katrina wants to do this
class ActionTemperature(Action):
    def name(self) -> Text:
        return "action_temperature"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        message = "Please select a recipe first!"
        if current_step != None:
            temperature = current_step.temperature
            if temperature == None:
                message = "Sorry I don't know the temperature of this step."
            else:
                message = "The temperature should be " + temperature + ". "

        dispatcher.utter_message(text=message)
        return []


# How long do I <specific technique>? -Katrina wants to do this
class ActionTime(Action):
    def name(self) -> Text:
        return "action_time"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        message = "Please select a recipe first!"
        if current_step != None:
            time = current_step.time
            if time == None:
                message = "Sorry I don't know the time of this step."
            else:
                message = "The time should be " + time + ". "

        dispatcher.utter_message(text=message)
        return []


class ActionVegetarian(Action):
    def name(self) -> Text:
        return "action_vegetarian"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        global dish_head
        if not dish_head:
            dispatcher.utter_message(text="Please select a recipe first!")
            return []
        
        if dish_head != None:
            vegetarian = dish_head.next.is_vegetarian()
            if vegetarian == True:
                message = "Recipe is already vegetarian. Enjoy!"
            else:
                try:
                    # iterate through each step and change the ingredients??
                    # first update the recipe ingredients for whole thing and track what replaces what
                    subst_dict = {}
                    new_ingredients = {}
                    for ingredient in dish_head.next.recipe_ingredients:
                        measure = dish_head.next.recipe_ingredients[ingredient]
                        ingredient_split = ingredient.split(' ')
                        for i in range(len(ingredient_split)):
                            word = ingredient_split[i]
                            if word in meat_lex:
                                if word in subst_dict:
                                    substitute = subst_dict[word]
                                else:
                                    substitute = random.choice(vegetarian_alternatives)
                                    subst_dict[word] = substitute
                                ingredient_split[i] = substitute
                                
                        recombined = ' '.join(ingredient_split)
                        new_ingredients[recombined] = measure
                    
                    dish_head.next.recipe_ingredients = new_ingredients
                        
                    temp_curr = dish_head.next
                    while temp_curr != None:
                        # remove all ingredients that are not vegetarian, and replace with vegetarian substitutes
                        # temp_curr.make_vegetarian()
                        print("before temp_curr.text: ", temp_curr.text)
                        #update the text
                        for word in subst_dict:
                            if word in temp_curr.text:
                                temp_curr.text = temp_curr.text.replace(word, subst_dict[word])
                        print("after temp_curr.text: ", temp_curr.text)
                        temp_curr.recipe_ingredients = new_ingredients
                        # go in and change this steps ingredients
                        for i in range(len(temp_curr.ingredients)): #each val in list
                            ingred = temp_curr.ingredients[i]
                            i_split = ingred.split(' ')
                            for j in range(len(i_split)): # each word in value (beef fillet)
                                word = i_split[j]
                                if word in subst_dict:
                                    i_split[j] = subst_dict[word]
                            recombined = ' '.join(i_split)
                            temp_curr.ingredients[i] = recombined

                        temp_curr = temp_curr.next
                    message = "Recipe is now vegetarian. Enjoy!"
                except Exception as e:
                    print(e)
                    traceback.print_exc()
                    message = "Sorry, I can't make this recipe vegetarian."

        dispatcher.utter_message(text=message)
        return []


class ActionScaleRecipe(Action):
    def name(self) -> Text:
        return "action_scale_recipe"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        global dish_head

        if not dish_head:
            dispatcher.utter_message(text="Please select a recipe first!")
            return []

        scale = get_entity_value(tracker)

        if not scale:
            dispatcher.utter_message(
                text="Please ask again and include the number of people you want to make the recipe for!")
            return []

        # Change the recipe globally: new quantity = old quantity / serving size * scale
        ingredients_text = ""

        # Change the ingredients for each step
        # step.ingredients are the ingredients in each step
        # step.recipe_ingredients are the ingredients for the entire recipe

        # for name, amount in dish_head.next.recipe_ingredients.items():
        #     new_amount = "1 cup"
        #     # Example amount = '1.5kg', '2 tbs'
        #     dish_head.next.recipe_ingredients[name] = new_amount
        #     # Add new values to ingredients_text
        
        # Note that both have to be changed

        dispatcher.utter_message(
            text=f"Here are the updated ingredients for {scale} people:\n\n{ingredients_text}\n")

        return []
