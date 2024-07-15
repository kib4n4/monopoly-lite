import random


# Function to roll two six-sided dice and return their sum.
def roll_dice():
  die1 = random.randint(1, 6)
  die2 = random.randint(1, 6)
  return die1 + die2


# Call the function to roll the dice and store the result.
result = roll_dice()

