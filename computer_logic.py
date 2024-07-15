from board import board
from cards import draw_card, handle_card, chance_cards, community_chest_cards

def movePlayer(player, roll, players):
    player.move(roll, players)

def computerDecisionToBuy(player):
    property = board[player.position]
    if property not in player.properties and property not in player.mortgaged_properties:
        if player.money >= property['price']:
            player.buyProperty(property)

def computerDecisionToMortgage(player):
    if player.money <= 500:
        if player.properties:
            player.mortgageProperty()

def computerTurn(player, players):
    dice1, dice2 = player.rollDice()
    movePlayer(player, dice1 + dice2, players)

    current_square = board[player.position]
    if current_square['name'] == "Income Tax":
        player.payTax(200)
    elif current_square['name'] == "Luxury Tax":
        player.payTax(100)
    elif current_square['name'] == "Chance":
        chance_card = draw_card(chance_cards)
        handle_card(player, chance_card, players)
    elif current_square['name'] == "Community Chest":
        community_chest_card = draw_card(community_chest_cards)
        handle_card(player, community_chest_card, players)
    else:
        if 'price' in current_square:
            if current_square not in player.properties and current_square not in player.mortgaged_properties:
                if player.money >= current_square['price']:
                    computerDecisionToBuy(player)
            elif current_square in player.properties:
                player.buildHouse()
            else:
                rent = player.calculateRent(current_square)
                player.payRent(rent, players)
        computerDecisionToMortgage(player)
