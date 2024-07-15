import random

# List of Chance cards for the Monopoly game
chance_cards = [
    "Advance to GO",  # Move to the "GO" space
    "Go to Jail",  # Move directly to Jail
    "Pay Poor Tax of $15",  # Pay a tax of $15
    "Your building and loan matures. Collect $150",  # Collect $150 from a matured loan
    "You have won a crossword competition. Collect $100",  # Collect $100 for winning a competition
    "Bank pays you dividend of $50",  # Receive a dividend payment of $50 from the bank
    "Get out of Jail Free",  # Get out of Jail without paying
    "Advance to Illinois Ave",  # Move to the Illinois Avenue space
    "Advance to St. Charles Place",  # Move to the St. Charles Place space
    "Take a ride on the Reading Railroad",  # Move to the Reading Railroad space
    "Advance to Boardwalk",  # Move to the Boardwalk space
    "Advance to the nearest Utility",  # Move to the nearest Utility space
    "Advance to the nearest Railroad",  # Move to the nearest Railroad space
    "You are assessed for street repairs: $40 per house, $115 per hotel",  # Pay for street repairs based on houses and hotels owned
    "Pay each player $50",  # Pay $50 to each player
    "Collect $150"  # Collect $150
]

# List of Community Chest cards for the Monopoly game
community_chest_cards = [
    "Advance to GO",  # Move to the "GO" space
    "Bank error in your favor. Collect $200",  # Receive $200 due to a bank error
    "Doctor's fees. Pay $50",  # Pay doctor's fees of $50
    "From sale of stock you get $50",  # Collect $50 from a stock sale
    "Get out of Jail Free",  # Get out of Jail without paying
    "Go to Jail",  # Move directly to Jail
    "Grand Opera Night. Collect $50 from every player",  # Collect $50 from each player for opera tickets
    "Holiday Fund matures. Receive $100",  # Collect $100 from a matured holiday fund
    "Income tax refund. Collect $20",  # Collect $20 from an income tax refund
    "It is your birthday. Collect $10 from each player",  # Collect $10 from each player for your birthday
    "Life insurance matures. Collect $100",  # Collect $100 from a matured life insurance policy
    "Pay hospital fees of $100",  # Pay hospital fees of $100
    "Pay school fees of $150",  # Pay school fees of $150
    "Receive $25 consultancy fee",  # Collect a consultancy fee of $25
    "You have won second prize in a beauty contest. Collect $10",  # Collect $10 for winning second prize in a beauty contest
    "You inherit $100"  # Collect $100 as an inheritance
]

def draw_card(cards):
    selected_card = random.choice(chance_cards)
    print(f"You drew a '{selected_card}' card.")
    return selected_card

community_chest_card=draw_card(community_chest_cards)
chance_card= draw_card(chance_cards)


# def draw_card(cards):
#     return random.choice(chance_cards)
# print("Chance_cards")
# for card in chance_cards:
#     print(card)

# def draw_card():

#    print("\nCommunity Chest Cards:")
# # Loop through Community Chest cards and print each one
# for card in community_chest_cards:
#    print(card)

def handle_card(player, card, players):
   if card == "Advance to GO":
       player.position = 0
       player.money += 200
       print(f"{player.name} advanced to GO and collected $200.")
   elif card == "Go to Jail":
       player.position = 10
       player.in_jail = True
       player.jail_turns = 0
       print(f"{player.name} is sent to jail.")
   elif card == "Pay Poor Tax of $15":
       player.money -= 15
       print(f"{player.name} paid $15 Poor Tax.")
   elif card == "Your building and loan matures. Collect $150":
       player.money += 150
       print(f"{player.name} collected $150 from building and loan maturing.")
   elif card == "You have won a crossword competition. Collect $100":
       player.money += 100
       print(f"{player.name} collected $100 for winning a crossword competition.")
   elif card == "Bank pays you dividend of $50":
       player.money += 50
       print(f"{player.name} collected $50 bank dividend.")
   elif card == "Get out of Jail Free":
       player.get_out_of_jail_free = True
       print(f"{player.name} received a 'Get out of Jail Free' card.")
   elif card == "Advance to Illinois Ave":
       player.position = 24
       print(f"{player.name} advanced to Illinois Ave.")
   elif card == "Advance to St. Charles Place":
       player.position = 11
       print(f"{player.name} advanced to St. Charles Place.")
   elif card == "Take a ride on the Reading Railroad":
       player.position = 5
       print(f"{player.name} advanced to Reading Railroad.")
   elif card == "Advance to Boardwalk":
       player.position = 38
       print(f"{player.name} advanced to Boardwalk.")
   elif card == "Advance to the nearest Utility":
       if player.position < 12 or player.position > 28:
           player.position = 12
       else:
           player.position = 28
       print(f"{player.name} advanced to the nearest Utility.")
   elif card == "Advance to the nearest Railroad":
       if player.position < 5 or player.position > 35:
           player.position = 5
       elif player.position < 15:
           player.position = 15
       elif player.position < 25:
           player.position = 25
       else:
           player.position = 35
       print(f"{player.name} advanced to the nearest Railroad.")
   elif card == "You are assessed for street repairs: $40 per house, $115 per hotel":
       total_cost = sum(player.houses.values()) * 40 + sum(player.hotels.values()) * 115
       player.money -= total_cost
       print(f"{player.name} paid ${total_cost} for street repairs.")
   elif card == "Pay each player $50":
       for p in players:
           if p != player:
               player.money -= 50
               p.money += 50
       print(f"{player.name} paid each player $50.")
   elif card == "Collect $150":
       player.money += 150
       print(f"{player.name} collected $150.")