import requests
import re
import random
# import spacy

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




# some of these are generated from GPT/copilot. may need to sort them out more. unsure if we need to separate utensils and tools
utensils_lex = {"fork", "spoon", "knife", "chopsticks", "spork", "tongs", "spatula", "ladle", 
               "peeler", "can opener", "pizza cutter", "cutter",
               "measuring cups", "measuring spoons", "rolling pin", "mortar and pestle", 
               "potato masher", "pastry brush", "garlic press", "egg beater", "nutcracker", 
               "ice cream scoop", "basting brush", "corkscrew", "cheese slicer", "kitchen shears", 
               "strainer", "slotted spoon", "melon baller", "fish spatula", "potato peeler", 
               "rice paddle", "serrated knife", "meat tenderizer", "apple corer", "jalapeno corer", 
               "onion chopper", "egg separator", "turkey baster", "funnel", "basting syringe", 
               "pastry wheel", "zester", "salad spinner", "nutmeg grater", "bamboo skewers", 
               "soup ladle", "spaghetti server", "egg timer", "tomato slicer", "avocado slicer", 
               "corn stripper", "berry huller", "meat cleaver",
               "corn holders", "bamboo steamers", "cherry pitter", 
               "oyster knife", "sushi mat", "bread lame", "slicer", 
               "dough scraper", "slicer", "nut chopper"}

tools_lex = {"pan", "grater", "whisk", "oven", "refrigerator", "stove", "sink", "pot", "bowl", "plate",
             "grill", "blender", "microwave", "toaster", "thermometer", "scale", "strainer", "colander", "grinder",
             "masher", "peeler", "rolling pin", "sifter", "ladle", "skillet", "wok", "saucepan", "crockpot", "slow cooker",
             "pressure cooker", "food processor", "cutting board", "baking sheet", "baking pan", "baking tray",
             "baking rack", "baking mold", "baking tin", "baking stone", "baking paper", "baking parchment",
             "mixing bowl", "whisking bowl", "serving platter", "tongs", "ladle", 
             "measuring cups", "measuring spoons", "timer", "pepper mill", "grill brush", "pastry brush",
             "frying pan", "pizza cutter", "ice cream scoop", "scooper", "garlic press", "bottle opener"}

methods_lex = {"sauté", "broil", "boil", "bake", "fry", "roast", "grill", "simmer", "poach", "steam", "stew", 
               "braise", "sear", "pan-fry", "deep-fry", "stir-fry", "griddle", "blanch", "smoke", "pressure cook", 
               "slow cook", "sous vide", "marinate", "pickle", "brine", "dehydrate", "ferment", "toast", "roast",
               "char-grill", "blacken", "flambé", "caramelize", "poêlé", "sweat", "confit", "reduce", "glaze", 
               "julienne", "puree", "parboil", "glaze", "blitz", "shallow-fry", "steam-fry", "flash-fry", 
               "steam-roast", "gratin", "coddle", "bain-marie", "macerate", "spherify", "infuse", "griddle", 
               "melt", "blowtorch", "baste", "gravy", "shuck", "fold", "knead", "deglaze", "whip", "beat", "cook"}

ingredients_lex = {"salt", "pepper", "olive oil", "vegetable oil", "butter", "eggs", "milk", "sugar", "flour", "onion", "garlic",
                   "tomato", "chicken", "beef", "pork", "rice", "pasta", "potatoes", "carrots", "bell pepper",
                   "broccoli", "spinach", "cheese", "cream", "yogurt", "honey", "mustard", "vinegar", "soy sauce",
                   "lemon", "lime", "cumin", "coriander", "basil", "thyme", "rosemary", "oregano", "cinnamon",
                   "vanilla extract", "baking powder", "baking soda", "cocoa powder", "maple syrup", "ketchup",
                   "mayonnaise", "mustard", "pickles", "chicken broth", "beef broth", "fish sauce", "salsa",
                   "hoisin sauce", "chili powder", "paprika", "bay leaves", "nutmeg", "ginger", "turmeric",
                   "cayenne pepper", "red pepper flakes", "sesame oil", "coconut milk", "quinoa", "almonds",
                   "walnuts", "pecans", "cashews", "sunflower seeds", "pumpkin seeds", "flaxseeds", "chia seeds",
                   "poppy seeds", "sun-dried tomatoes", "artichoke hearts", "capers", "green onions", "parsley",
                   "cilantro", "dill", "mint", "chives", "jalapeño", "avocado", "lentils", "black beans",
                   "kidney beans", "chickpeas", "canned tomatoes", "crushed red pepper", "nutritional yeast",
                   "parmesan cheese", "mozzarella cheese", "feta cheese", "cheddar cheese", "greek yogurt",
                   "shallots", "celery", "asparagus", "zucchini", "mushrooms", "leeks", "radishes", "sweet potatoes",
                   "butternut squash", "acorn squash", "pumpkin", "eggplant", "corn", "cauliflower", "cabbage",
                   "brussels sprouts", "green beans", "beets", "turnips", "rutabaga", "kiwi", "pineapple", "strawberries",
                   "blueberries", "raspberries", "blackberries", "watermelon", "melon", "grapes", "kiwi", "orange",
                   "grapefruit", "peach", "plum", "nectarine", "apricot", "pear", "apple", "figs", "dates", "raisins",
                   "prunes", "apricots", "cranberries", "pomegranate seeds", "dates", "figs", "hazelnuts", "pistachios",
                   "macadamia nuts", "peanuts", "almond butter", "peanut butter", "cashew butter", "sunflower butter",
                   "hummus", "tofu", "tempeh", "seitan", "edamame", "misu", "soy milk", "almond milk", "coconut water",
                   "beetroot", "cucumber", "avocado oil", "truffle oil", "sesame seeds", "wasabi", "mirin", "rice vinegar",
                   "balsamic vinegar", "red wine vinegar", "white wine vinegar", "white wine", "red wine", "rosemary",
                   "thyme", "dill", "oregano", "sage", "tarragon", "mint leaves", "coriander leaves", "bay leaves",
                   "curry leaves", "lemongrass", "star anise", "cardamom", "cloves", "fennel seeds", "mustard seeds",
                   "cumin seeds", "poppy seeds", "sesame seeds", "chia seeds", "sunflower seeds", "flaxseeds",
                   "pumpkin seeds", "vanilla bean", "cocoa nibs", "coconut flakes", "chocolate chips", "white chocolate",
                   "dark chocolate", "miso paste", "tahini", "dijon mustard", "whole grain mustard", "hot sauce",
                   "barbecue sauce", "teriyaki sauce", "worcestershire sauce", "hoisin sauce", "soy sauce",
                   "sriracha", "sambal oelek", "kaffir lime leaves", "fish sauce", "tamari", "mirin", "sake",
                   "rice wine", "cooking wine", "white pepper", "black garlic", "pickled ginger", "wasabi paste",
                   "furikake", "seaweed", "norimaki", "kimchi", "sauerkraut", "harissa", "garam masala", "curry powder",
                   "five-spice powder", "za'atar", "tahini", "pistachio oil", "walnut oil", "flaxseed oil",
                   "pomegranate molasses", "molasses", "agave nectar", "miracle fruit", "gochujang", "ajvar", "tomato paste",
                   "dashi", "ume plum vinegar", "mirin", "wasabi powder", "xanthan gum", "agar-agar", "arrowroot",
                   "cornstarch", "tapioca starch", "ghee", "clarified butter", "duck fat", "schmaltz", "lard",
                   "bacon fat", "coconut oil", "palm oil", "beef tallow", "vegetable shortening", "duck eggs", "quail eggs",
                   "goat cheese", "blue cheese", "gouda", "pecorino", "ricotta", "cottage cheese", "paneer", "queso fresco",
                   "smoked salmon", "anchovies", "sardines", "trout", "mackerel", "caviar", "crab", "lobster", "shrimp",
                   "scallops", "calamari", "octopus", "clams", "mussels", "oysters", "squid", "abalone", "eel", "frog legs",
                   "snake", "rabbit", "venison", "elk", "bison", "buffalo", "boar", "kangaroo", "quail", "pigeon", "turtle",
                   "alligator", "snail", "escargot", "cactus", "bamboo shoots", "water chestnuts", "lotus root", "okra",
                   "jicama", "chayote", "wasabi peas", "goji berries", "goldenberries", "black garlic", "kombu", "nori", 
                   "parmigiano-reggiano", "water", "red chile flakes", "seasoning", "sauce"}

meat_lex = {'beef', 'pork', 'chicken', 'lamb', 'turkey', 'fish', 'shrimp', 'bacon', 'sausage', 'ham', 'steak', 'veal', 'venison', 'mutton', 'rabbit', 'duck', 'goose',
    'anchovy', 'calamari', 'clams', 'crab', 'lobster', 'mussels', 'octopus', 'oysters', 'scallops', 'squid', 'tilapia', 'catfish', 'trout', 'salmon', 'tuna',
    'sardines', 'haddock', 'cod', 'swordfish', 'perch', 'crayfish', 'snapper', 'bass', 'carp', 'marlin', 'halibut', 'pike', 'snail', 'frog', 'turtle', 'escargot',
    'buffalo', 'bison', 'elk', 'horse', 'boar', 'quail', 'pigeon', 'pheasant', 'emu', 'kangaroo', 'alligator', 'turtle', 'squab', 'veal', 'mahi-mahi'}

vegetarian_alternatives = [
    'Plant-based mock meat', 'Lentils', 'Portobello mushrooms',
    'Plant-based impossible meat', 'Jackfruit', 'Tempeh bacon', 'Tofu', 'Seitan', 'Chickpeas', 
    'Lentils', 'Eggplant', 'Quinoa', 'Tofu', 'Tempeh', 'Eggplant', 'Zucchini', 'King oyster mushrooms',
    'Smoked tofu', 'Eggplant strips', 'Mushroom and lentil mixtures', 'Chickpea or black bean sausages',
    'Smoked tofu', 'Tempeh', 'Portobello mushrooms', 'Eggplant or cauliflower steaks',
    'Artichoke hearts', 'Textured vegetable protein (TVP)', 'Soy curls', 'Black bean burgers', 'Sweet potato falafel']




def extract_time_information(input_string):
    # Define a regular expression pattern for time intervals (e.g., "5 minutes")
    time_pattern = re.compile(r'\b(\d+\s*(?:to|-)\s*\d+\s*(?:seconds?|secs?|minutes?|mins?|hours?|days?|weeks?|months?|years?)|\d+\s*(?:seconds?|secs?|minutes?|mins?|hours?|days?|weeks?|months?|years?))\b', re.IGNORECASE)
    # Search for the pattern in the input string
    match = re.search(time_pattern, input_string)
    # Return True if a match is found, indicating the presence of time information
    return match.group(1) if match else None


def extract_temperature_information(input_string):
    # Define a regular expression pattern for temperature (e.g., "25°C", "98.6°F")
    temperature_pattern = re.compile(r'\b(\d+(?:\.\d+)?)\s*(degrees?)\s*([FC])\b', re.IGNORECASE)
    
    # Search for the pattern in the input string
    match = re.search(temperature_pattern, input_string)
    # Return the matched temperature information or None if no match is found
    if match:
        return match.group(1) 
    
    keywords = ['medium-high heat', 'medium-low heat', 'medium heat', 'low heat','high heat',  'boiling', 'warm', 'hot', 'cold', 'cool']
    for keyword in keywords:
        if keyword.lower() in input_string.lower():
            return keyword
    return None



class Step:
    def __init__(self, text = None, recipe_ingredients = None, p = None, n = None):
        self.prev = p
        self.next = n
        self.text = text.lower() if text is not None else None
        # self.cooking_actions = []
        self.recipe_ingredients = recipe_ingredients
        self.ingredients = []
        self.tools = []
        self.utensils = []
        self.methods = []
        self.time = None
        self.temperature = None
        if text:
            self.parse(text.lower(), recipe_ingredients)

    def has_next_step(self):
        if self.next == None:
            return False
        return True

    def print_text(self):
        print(self.text)
    def print_cooking_actions(self):
        print(self.cooking_actions)
    def print_ingredients(self):
        print("ingredients: " , self.ingredients)
    def print_tools(self):
        if len(self.tools) != 0:
            print("tools: " , self.tools)
    def print_utensils(self):
        if len(self.utensils) != 0:
            print("utensils: " , self.utensils)
    def print_methods(self):
        if len(self.methods) != 0:
            print("methods: " , self.methods)
    def print_time(self):
        if self.time:
            print("time: ", self.time)
    def print_temperature(self):
        if self.temperature:
            print("temperature: ", self.temperature)

    # def to_dict(self):
    #     return {
    #         'text': self.text,
    #         'recipe_ingredients': self.recipe_ingredients,
    #         'ingredients': self.ingredients,
    #         'tools': self.tools,
    #         'utensils': self.utensils,
    #         'methods': self.methods,
    #         'time': self.time,
    #         'temperature': self.temperature,
    #         'prev': None if self.prev is None else self.prev.to_dict(),
    #         'next': None if self.next is None else self.next.to_dict()
    #     }

    def is_vegetarian(self):
        for ingredients in self.recipe_ingredients:
            ingredient_list = ingredients.split(' ')
            for ingredient in ingredient_list:
                if ingredient in meat_lex:
                    return False
        return True
    
    '''
    def make_vegetarian(self):
        recipe_ingredient_removal_list = [] # list of strings to remove from recipe_ingredients after loop (might cause issues to do it midway)
        ingredient_removal_list = []
        for ingredients in self.ingredients:
            ingredient_list = ingredient.split(' ')
            for i in range(len(ingredient_list)):
                ingredient = ingredient_list[i]
                print(ingredient)
                if ingredient in meat_lex: # if meat found replace meat in ingredients and recipe_ingredients
                    # remove meat from ingredients
                    measure = None
                    # self.ingredients.remove(ingredients)
                    ingredient_removal_list.append(ingredients)
                    if ingredients in self.recipe_ingredients:
                        measure = self.recipe_ingredients[ingredients]
                        # del self.recipe_ingredients[ingredients]
                        recipe_ingredient_removal_list.append(ingredients)
                    # replace with vegetarian alternative
                    substitute = random.choice(vegetarian_alternatives)
                    # update the list
                    ingredient_list[i] = substitute
                    new_ingredient = " ".join(ingredient_list)
                    self.ingredients.append(new_ingredient)
                    if new_ingredient not in self.recipe_ingredients:
                        if measure:
                            self.recipe_ingredients[new_ingredient] = measure
                        else:
                            self.recipe_ingredients[new_ingredient] = 'to taste'
    '''
            

    def parse(self, text, ingredients):
        #TODO: inplement this function, find following information
        # self.cooking_actions = [] # verbs #done
        # self.ingredients = [] #direct object #done
        # self.tools = [] #done
        # self.utensils = [] #done
        # self.time = [] #optional #done
        # self.temperature = [] #optional #done

        #self.cooking_actions
        # spacy_model = spacy.load("en_core_web_sm")
        # spacy_output = spacy_model(text)
        # for token in spacy_output:
        #     if token.pos_ == "VERB":
        #         self.cooking_actions.append(token.text)



        # more advanced classification on ingredients?
        # noun_chunks_without_det = [" ".join(token.text for token in chunk if token.dep_ != "det") for chunk in spacy_output.noun_chunks]
        # for chunk in noun_chunks_without_det:
        #     self.ingredients.append(chunk)
        # self.ingredients
        # for ingredient in ingredients_lex:
        #     if ingredient in text:
        #         self.ingredients.append(ingredient)
        # print("in")
        for ingredient in ingredients_lex:
            if ingredient in text:
                if ingredient in self.recipe_ingredients:
                    quantified_ingredient = self.recipe_ingredients[ingredient] + ' of ' + ingredient
                    self.ingredients.append(quantified_ingredient)
                else:
                    self.ingredients.append(ingredient)




        for tool in tools_lex:
            if tool in text:
                self.tools.append(tool)

        for utensil in utensils_lex:
            if utensil in text:
                self.utensils.append(utensil)

        for method in methods_lex:
            if method in text:
                self.methods.append(method)

        self.time = extract_time_information(text)
        self.temperature = extract_temperature_information(text)

        


instructions = re.split(r'\.\r\n|\.',recipe['strInstructions'])
recipe_ingredients = {} #[]
for i in range(1,20):
    ingredient = recipe['strIngredient'+str(i)]
    if ingredient == '' or ingredient == None:
        continue
    recipe_ingredients[ingredient.lower()] = recipe['strMeasure'+str(i)].lower()


# https://www.google.com/search?q=how+to+preheat+oven 
# https://www.youtube.com/results?search_query=how+to+preheat+oven 
def external_knowledge(question):
    question = question.split(' ').strip()
    if "what" in question:
        search_url = "https://www.google.com/search?q=" + "+".join(question)
    if "how" in question:
        search_url = "https://www.youtube.com/results?search_query=" + "+".join(question)
    return(search_url)

    


def remove_leading_space(input_str):
    if input_str and input_str[0] == ' ':
        return input_str.lstrip()
    else:
        return input_str


# head = Step()
# prev_step = head
# for instruction in instructions:
#     # print(instruction)
#     instruction = remove_leading_space(instruction)
#     curr_step = Step(instruction, recipe_ingredients, prev_step)
#     prev_step.next = curr_step
#     prev_step = curr_step




###################################
#printing text of steps, cooking actions of steps, etc.
# curr_step = head.next
# while curr_step.has_next_step():
#     curr_step.print_text() # can change to other methods like print_cooking_actions()
#     curr_step.print_ingredients()
#     curr_step.print_tools()
#     curr_step.print_utensils()
#     curr_step.print_methods()
#     curr_step.print_time()
#     curr_step.print_temperature()
#     curr_step = curr_step.next