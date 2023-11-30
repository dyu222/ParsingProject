# ParsingProject
CS 337: Parsing Project Partners: Qinyan Li, Derek Yu, Emily Zhang

# Starting the RecipeBot
    1. Activate the virtual environment with Python@3.8
    2. pip install -r requirements.txt
    3. rasa train
    4. rasa run actions (on one terminal)
    5. rasa shell (on another terminal)

# Implementation General Idea
Store each step as a node in a Doubly Linked List (this allows us to easily find next and previous step)

Have each node contain important parsed values: cooking action, ingredient, tools, utensils, etc.

Use our 'model' to answer questions

# Parsing idea
Currently assuming that each sentence is likely to be a step.
Within this step parse each of the values that we are looking for using various methods and add them to the node's attributes


# Deploying bot to slack
1. Run `rasa run actions` in terminal 1
2. Run `rasa run --connector slack --credentials credentials.yml --endpoints endpoints.yml --enable-api` in terminal 2
3. Run `ngrok http 5005` - i might need to change this port tbd
4. Go into slack subscriptions and add the request URL: https://api.slack.com/apps/A067Z3NR4H2/event-subscriptions?
(It might be beneficial to change the ngrok command to try and use a deterministic web url, will look into that)
6. Go to slack bot and chat with it by messaging `@Rasa recipe chatbot` in any channel: https://join.slack.com/t/cs337nlp/shared_invite/zt-27yf7lck5-RS9zvZ2cJFQxI5F66N_TFA
Notice: credentials are out of date and get deactivated when put on public github, not sure what the current plan for this is right now