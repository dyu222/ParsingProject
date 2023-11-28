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
    def __init__(self, text=None, ingredients=None, p=None, n=None):
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
        # TODO: inplement this function, find following information
        # self.cooking_actions = [] # verbs #done
        # self.ingredients = [] #direct object #done
        # self.tools = []
        # self.utensils = []
        # self.time = [] #optional
        # self.temperature = [] #optional

        # self.cooking_actions
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

            # if chunk in utensils_lex:
            #     self.utensils.append(chunk)
            # if chunk in tools_lex:
            #     self.tool.append(chunk)


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
               "melt", "blowtorch", "baste", "gravy", "shuck", "fold", "knead", "deglaze", "whip", "beat"}

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
                   "jicama", "chayote", "wasabi peas", "goji berries", "goldenberries", "black garlic", "kombu", "nori"}

instructions = re.split(r'\.\r\n|\.', recipe['strInstructions'])
ingredients = []
for i in range(1, 20):
    ingredient = recipe['strIngredient'+str(i)]
    if ingredient == '' or ingredient == None:
        continue
    ingredients.append(ingredient.lower())


# https://www.google.com/search?q=how+to+preheat+oven
# https://www.youtube.com/results?search_query=how+to+preheat+oven
def external_knowledge(question):
    question = question.split(' ').strip()
    if "what" in question:
        search_url = "https://www.google.com/search?q=" + "+".join(question)
    if "how" in question:
        search_url = "https://www.youtube.com/results?search_query=" + \
            "+".join(question)
    return (search_url)


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
# printing text of steps, cooking actions of steps, etc.
curr_step = head.next
while curr_step.has_next_step():
    curr_step.print_text()  # can change to other methods like print_cooking_actions()
    curr_step.print_ingredients()
    curr_step = curr_step.next

if __name__ == "__main__":
    
