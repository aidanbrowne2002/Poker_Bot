import random
import time
import matplotlib.pyplot as plt

from icecream import ic

# Initial variable definition
playerNum = 6
people = []
names = ["Steve", "Alan", "Barry", "Pete", "Garry"]
pretty_suits = {'C': '\u2667', 'D': '\u2662', 'H': '\u2661', 'S': '\u2664'}
value_def = {1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: "J", 11: "Q", 12: "K", 13: "A"}
global cards
cards = []

playerName = "Aidan"


class Player:
    def __init__(self, name, style):
        self.name = name
        self.style = style
        self.cards = []
        self.hand = None
        self.hand_value = []
        self.additional_cards = []
        self.rank = None
        self.folded = False

    def is_main(self):
        if hasattr(self, "main"):
            return True
        else:
            return False


class Me(Player):
    def __init__(self, name, style):
        Player.__init__(self, name, style)
        self.main = True
        self.wins = 0
        self.ranks = []


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.cards = cards


class Table:
    def __init__(self):
        self.pot = 0
        self.cards = []


def initialise():
    for x in range(0, playerNum - 1):
        person = Player(names[x], 0)
        people.append(person)

    for key, value in pretty_suits.items():
        for x in range(1, 14):
            card = Card(key, x)
            cards.append(card)
    return people, cards


def deal_hands():
    for person in people:
        if person.is_main():
            for card in cards:
                if card.suit == "H" and card.value == 13:
                    person.cards.append(card)
                    cards.remove(card)
            for card in cards:
                if card.suit == "D" and card.value == 13:
                    person.cards.append(card)
                    cards.remove(card)
                    # print (len(car`ds))
            # print(len(person.cards))
            # print(person.cards[0].value, person.cards[0].suit)
            # print(
            # f"{person.name} received: {value_def[person.cards[0].value], pretty_suits[person.cards[0].suit]},"
            # f" {value_def[person.cards[1].value], pretty_suits[person.cards[1].suit]}")
    for person in people:
        if not person.is_main():
            for x in range(0, 2):
                chosen_card = random.choice(cards)
                person.cards.append(chosen_card)
                cards.remove(chosen_card)  # Remove the chosen card from the deck
            # print(
            # f"{person.name} received: {value_def[person.cards[0].value], pretty_suits[person.cards[0].suit]},"
            # f" {value_def[person.cards[1].value], pretty_suits[person.cards[1].suit]}")


def deal_card():
    chosen_card = random.choice(cards)
    table.cards.append(chosen_card)
    cards.remove(chosen_card)  # Remove the chosen card from the deck
    # print(f" {value_def[table.cards[-1].value], pretty_suits[table.cards[-1].suit]}")


def deal_flop():
    for x in range(0, 3):
        deal_card()


def check_hand(player):
    cards = table.cards + player.cards
    flush_cards = []
    high_card = None
    flush_suit = None

    # Check Royal Flush /Straight Flush/ Flush

    suits = []
    for card in cards:
        suits.append(card.suit)
    suit_num = {i: suits.count(i) for i in suits}
    for card, num in suit_num.items():
        if num >= 5:
            flush_suit = card
    for card in cards:
        if card.suit == flush_suit:
            flush_cards.append(card.value)
    if flush_cards:
        high_card = max(flush_cards)
        if sorted(flush_cards) == list(range(min(flush_cards), max(flush_cards) + 1)):
            if min(flush_cards) == 9:
                player.hand_value = [high_card]
                return "Royal Flush"
            player.hand_value = [high_card]
            return "Straight Flush"

        player.hand_value = [high_card]
        return "Flush"
    # Check straight
    cards_values = []
    for card in cards:
        cards_values.append(card.value)
    # print(cards_values)
    cards_values = sorted(cards_values)
    # ic(cards_values)
    if sorted(cards_values[0:5]) == list(range(min(cards_values[0:5]), max(cards_values[0:5]) + 1)):
        player.hand_value = [max(cards_values[0:5])]
        return "Straight"
    if sorted(cards_values[1:6]) == list(range(min(cards_values[1:6]), max(cards_values[1:6]) + 1)):
        player.hand_value = [max(cards_values[1:6])]
        return "Straight"
    if sorted(cards_values[2:7]) == list(range(min(cards_values[2:7]), max(cards_values[2:7]) + 1)):
        player.hand_value = [max(cards_values[2:7])]
        return "Straight"

    values = []
    for card in cards:
        values.append(card.value)
    number_num = {i: values.count(i) for i in values}
    # ic(number_num)
    combinations = []
    types = []
    # print (number_num)
    number_num = dict(sorted(number_num.items(), reverse=True))
    # print(number_num)
    for card, num in number_num.items():

        if num >= 4:
            combinations.append(["four", card])
            player.hand_value.append(card)
            types.append("four")
        elif num >= 3:
            combinations.append(["three", card])
            player.hand_value.append(card)
            types.append("three")
        elif num >= 2:
            combinations.append(["two", card])
            player.hand_value.append(card)
            types.append("two")
        else:
            player.additional_cards.append(card)
    try:
        player.hand_value = sorted(player.hand_value, reverse=True)
    except:
        print("couldn't sort")
    try:
        player.additional_cards = sorted(player.additional_cards, reverse=True)
    except:
        print("couldn't sort")
    if "four" in types:
        return "Four"
    if "three" in types and "two" in types:
        return "Full House"
    if "three" in types:
        return "Three"
    if types.count("two") >= 2:
        return "Two Pair"
    if types.count("two") == 1:
        return "Pair"
    # print(combinations)
    return None


def hand_ranking():
    if player.hand == "Royal Flush":
        player.rank = 1
    elif player.hand == "Straight Flush":
        player.rank = 2
    elif player.hand == "Four":
        player.rank = 3
    elif player.hand == "Full House":
        player.rank = 4
        del player.additional_cards[-2:]
    elif player.hand == "Flush":
        player.rank = 5
    elif player.hand == "Straight":
        player.rank = 6
    elif player.hand == "Three":
        player.rank = 7
        del player.additional_cards[-2:]
    elif player.hand == "Two Pair":
        player.rank = 8
        del player.additional_cards[-2:]
    elif player.hand == "Pair":
        player.rank = 9
        del player.additional_cards[-2:]
    else:
        player.rank = 10
        player.hand = "High Card"
        del player.additional_cards[-2:]


def player_ranking():
    rankedPlayers = []
    for rank in range(1, 11):
        compare = []
        for player in people:
            if player.rank == rank:
                compare.append(player)
        for player in compare:
            # compare = sorted(compare, key=lambda x: x.hand_value, reverse = True)
            compare = sorted(compare, key=lambda x: (x.hand_value, x.additional_cards), reverse=True)
        for player in compare:
            rankedPlayers.append(player)
    return rankedPlayers


if __name__ == '__main__':
    people.append(Me(playerName, 0))
    initialise()
    start_time = time.time()
    for x in range(0, 10000):
        # print("reset")
        for player in people:
            player.rank = None
            player.hand_value = []
            player.hand = None
            player.cards = []
        cards = []
        for key, value in pretty_suits.items():
            for x in range(1, 14):
                card = Card(key, x)
                # print("here")
                cards.append(card)
        table = Table()
        deal_hands()
        # print("Table:")
        deal_flop()
        deal_card()
        deal_card()
        for player in people:
            player.hand = check_hand(player)

            hand_ranking()
        people = player_ranking()
        previousplayer = None
        index = 1
        for player in people:
            if previousplayer:
                if [player.hand, player.hand_value, player.additional_cards] != [previousplayer.hand,
                                                                                 previousplayer.hand_value,
                                                                                 previousplayer.additional_cards]:
                    index += 1
                    player.rank = index
                else:
                    player.rank = index
            else:
                player.rank = index
            previousplayer = player
        for player in people:
            pass
            # print(f"{player.name} Got a: {player.hand}, ranking: {player.rank}")
        for player in people:
            if player.name == "Aidan":
                player.ranks.append(player.rank)
                if player.rank == 1:
                    player.wins += 1
        # print (len(cards))
    end_time = time.time()
    total_time = end_time - start_time
    for player in people:
        if player.name == "Aidan":
            rank_values = {i: player.ranks.count(i) for i in player.ranks}
            rank_values = dict(sorted(rank_values.items(), reverse=True))
            plt.bar(range(len(rank_values)), list(rank_values.values()), align='center')
            plt.xticks(range(len(rank_values)), list(rank_values.keys()))
            print(rank_values)
            print(f"{player.wins / 100}%")
            print("time taken to run 10000 games =", total_time)
            plt.show()
