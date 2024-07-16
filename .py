from player import Player
from computer_logic import computerTurn
from board import board
import random

def movePlayer(player, roll, players):
    player.move(roll, players)

def check_for_bankruptcy(players):
    for player in players:
        if player.checkBankruptcy():
            print(f"{player.name} is bankrupt and has been removed from the game.")
            players.remove(player)
    if len(players) == 1:
        print(f"{players[0].name} is the winner!")
        return True
    return False

def play_game():
    print("Player 1, please select your token.")
    player1 = Player("Player 1")
    remaining_tokens = ["Thor", "Strange", "IronMan", "Hawkeye"]
    remaining_tokens.remove(player1.token)
    player2 = Player("Computer", token=random.choice(remaining_tokens), is_computer=True)
    players = [player1, player2]

    current_player = player1

    while len(players) > 1:
        current_square = board[current_player.position]

        if current_player.is_computer:
            computerTurn(current_player, players, board, current_square)
        else:
            print(f"\n{current_player.token}'s turn.")
            input("Press Enter to roll the dice.\n")
            dice1, dice2 = current_player.rollDice()
            movePlayer(current_player, dice1 + dice2, players)

            current_square = board[current_player.position]

            # Handle special squares of the game
            if current_square['name'] == "Income Tax":
                current_player.payTax(200)
            elif current_square['name'] == "Luxury Tax":
                current_player.payTax(100)
            elif 'price' in current_square:
                if current_square not in current_player.properties and current_square not in current_player.mortgaged_properties:
                    print(f"\n{current_player.token}, do you want to buy {current_square['name']} for ${current_square['price']}?")
                    buy_option = input("Press 'y' to buy or 'n' to skip: ").lower()
                    if buy_option == 'y':
                        current_player.buyProperty()
                elif current_square in current_player.properties:
                    print(f"{current_player.token}, you landed on your own property: {current_square['name']}.")
                    print(f"Do you want to build a house or hotel on {current_square['name']}?")
                    build_option = input("Press 'h' to build a house, 'o' to build a hotel, or 'n' to skip: ").lower()
                    if build_option == 'h':
                        current_player.buildHouse()
                    elif build_option == 'o':
                        current_player.buildHotel()
                else:
                    rent = current_player.calculateRent(current_square)
                    print(f"{current_player.token} needs to pay ${rent} in rent.")
                    current_player.payRent(rent, players)

            # Mortgage option
            print(f"\n{current_player.token}, do you want to mortgage a property?")
            mortgage_option = input("Press 'y' to mortgage or 'n' to continue: ").lower()
            if mortgage_option == 'y':
                current_player.mortgageProperty()

        # Check for bankruptcy at the end of each turn
        if check_for_bankruptcy(players):
            break

        current_player = player1 if current_player == player2 else player2

play_game()