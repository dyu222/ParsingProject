# ParsingProject
CS 337: Parsing Project Partners: Qinyan Li, Derek Yu, Emily Zhang

# Implementation General Idea
Store each step as a node in a Doubly Linked List (this allows us to easily find next and previous step)

Have each node contain important parsed values: cooking action, ingredient, tools, utensils, etc.

Use our 'model' to answer questions

# Parsing idea
Currently assuming that each sentence is likely to be a step.
Within this step parse each of the values that we are looking for using various methods and add them to the node's attributes