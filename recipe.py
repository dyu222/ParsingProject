import requests
import re
import spacy

# Specify the URL of the API you want to call
api_url = "https://themealdb.com/api/json/v1/1/search.php?s=Arrabiata"

# Make a GET request to the API
response = requests.get(api_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Print the content of the response
    recipe = response.json()['meals'][0]
    # print(recipe.keys())
else:
    # Print an error message if the request was not successful
    print(f"Error: {response.status_code}")


class Step:
    def __init__(self, text = None, ingredients = None, p = None, n = None):
        self.prev = p
        self.next = n
        self.text = text.lower() if text is not None else None
        self.cooking_actions = []
        self.ingredients = []
        self.tools = []
        self.utensils = []
        self.time = []
        self.temperature = []
        if text:
            self.parse(text.lower(), ingredients)

    def has_next_step(self):
        if self.next == None:
            return False
        return True

    def print_text(self):
        print(self.text)
    def print_cooking_actions(self):
        print(self.cooking_actions)
    def print_ingredients(self):
        print(self.ingredients)

    def parse(self, text, ingredients):
        #TODO: inplement this function, find following information
        # self.cooking_actions = [] # verbs #done
        # self.ingredients = [] #direct object #done
        # self.tools = []
        # self.utensils = []
        # self.time = [] #optional
        # self.temperature = [] #optional

        #self.cooking_actions
        spacy_model = spacy.load("en_core_web_sm")
        spacy_output = spacy_model(text)
        for token in spacy_output:
            if token.pos_ == "VERB":
                self.cooking_actions.append(token.text)

        
        # self.ingredients
        for ingredient in ingredients:
            if ingredient in text:
                self.ingredients.append(ingredient)

        # more advanced classification on ingredients?
        # noun_chunks_without_det = [" ".join(token.text for token in chunk if token.dep_ != "det") for chunk in spacy_output.noun_chunks]
        # for chunk in noun_chunks_without_det:
        #     self.ingredients.append(chunk)
        

        
utensils_lex = {"fork","spoon","knife","chopsticks"}
tools_lex = {"oven","refrigerator","stove","sink"}

instructions = re.split(r'\.\r\n|\.',recipe['strInstructions'])
ingredients = []
for i in range(1,20):
    ingredient = recipe['strIngredient'+str(i)]
    if ingredient == '' or ingredient == None:
        continue
    ingredients.append(ingredient.lower())




def remove_leading_space(input_str):
    if input_str and input_str[0] == ' ':
        return input_str.lstrip()
    else:
        return input_str



head = Step()
prev_step = head
for instruction in instructions:
    # print(instruction)
    instruction = remove_leading_space(instruction)
    curr_step = Step(instruction, ingredients, prev_step)
    prev_step.next = curr_step
    prev_step = curr_step




###################################
#printing text of steps, cooking actions of steps, etc.
curr_step = head.next
while curr_step.has_next_step():
    curr_step.print_text() # can change to other methods like print_cooking_actions()
    curr_step.print_ingredients()
    curr_step = curr_step.next