import random
from board import board
from cards import draw_card, handle_card, chance_cards, community_chest_cards

class Player:
    def __init__(self, name, token=None, properties=None, is_computer=False):
        self.name = name
        self.token = token if token is not None else self.tokenSelection()
        self.money = 1500
        self.properties = properties if properties is not None else []
        self.mortgaged_properties = []
        self.position = 0
        self.is_computer = is_computer
        self.in_jail = False
        self.jail_turns = 0
        self.get_out_of_jail_free = False
        self.houses = {}
        self.hotels = {}

    def tokenSelection(self):
        tokens = ["Thor", "Strange", "IronMan", "Hawkeye"]
        choice = random.choice(tokens) if self.is_computer else int(input("Enter the number of your choice: ")) - 1
        return tokens[choice]

    def rollDice(self):
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        return die1, die2

    def move(self, roll, players):
        if self.in_jail:
            self.handleJail(roll)
            return

        self.position = (self.position + roll) % len(board)
        current_square = board[self.position]
        if current_square['name'] == "Go" and self.position != 0:
            self.money += 200

        if current_square['name'] == "Chance":
            chance_card = draw_card(chance_cards)
            handle_card(self, chance_card, players)
        elif current_square['name'] == "Community Chest":
            community_chest_card = draw_card(community_chest_cards)
            handle_card(self, community_chest_card, players)
        else:
            if 'price' in current_square:
                self.handleProperty(current_square)

    def handleJail(self, roll):
        if self.get_out_of_jail_free:
            self.get_out_of_jail_free = False
            self.in_jail = False
            self.position = (self.position + roll) % len(board)
            return

        if self.money >= 50:
            self.money -= 50
            self.in_jail = False
            self.position = (self.position + roll) % len(board)
            return

        die1, die2 = self.rollDice()
        if die1 == die2:
            self.in_jail = False
            self.position = (self.position + roll) % len(board)
        else:
            self.jail_turns += 1
            if self.jail_turns >= 3:
                self.money -= 50
                self.in_jail = False
                self.position = (self.position + roll) % len(board)

    def handleProperty(self, current_square):
        if current_square not in self.properties and current_square not in self.mortgaged_properties:
            if self.money >= current_square['price']:
                self.buyProperty(current_square)
            else:
                print(f"Not enough money to buy {current_square['name']}.")

    def buyProperty(self, property):
        self.properties.append(property)
        self.money -= property['price']
        self.checkBankruptcy()

    def mortgageProperty(self):
        if not self.properties:
            return

        property_to_mortgage = self.properties[0] if self.is_computer else self.selectPropertyToMortgage()
        mortgage_value = property_to_mortgage['price'] // 2

        self.money += mortgage_value
        self.mortgaged_properties.append(property_to_mortgage)
        self.properties.remove(property_to_mortgage)
        property_to_mortgage['is_mortgaged'] = True
        self.checkBankruptcy()

    def selectPropertyToMortgage(self):
        for i, property in enumerate(self.properties, 1):
            print(f"{i}. {property['name']}")
        choice = int(input("Enter the number of the property you want to mortgage: "))
        return self.properties[choice - 1]

    def payTax(self, amount):
        self.money -= amount
        self.checkBankruptcy()

    def calculateRent(self, property):
        if property['name'] in ["Go", "Chance", "Community Chest"]:
            return 0
        elif property in self.properties:
            return 0
        base_rent = property['rent'][0]
        houses = self.houses.get(property['name'], 0)
        hotels = self.hotels.get(property['name'], 0)
        return property['rent'][5] if hotels else base_rent + houses * (property['rent'][houses] - base_rent)

    def payRent(self, amount, players):
        self.money -= amount
        for player in players:
            if player != self and board[self.position] in player.properties:
                player.money += amount
                break
        self.checkBankruptcy()

    def buildHouse(self):
        property = board[self.position]
        if property in self.properties and self.money >= 50:
            self.money -= 50
            self.houses[property['name']] = self.houses.get(property['name'], 0) + 1
            self.checkBankruptcy()

    def buildHotel(self):
        property = board[self.position]
        if property in self.properties and self.money >= 200:
            self.money -= 200
            self.hotels[property['name']] = 1
            self.checkBankruptcy()

    def checkBankruptcy(self):
        if self.money < 0:
            return True
        return False

    def handleBankruptcy(self, players):
        if self.checkBankruptcy():
            players.remove(self)
            if len(players) == 1:
                return True
        return False