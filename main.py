import random
import time
import matplotlib.pyplot as plt
from icecream import ic

from text_read.players import Player, Me

# Initial variable definition
PLAYER_NUM = 6
PEOPLE = []
NAMES = ["Steve", "Alan", "Barry", "Pete", "Garry"]
PRETTY_SUIT = {'C': '\u2667', 'D': '\u2662', 'H': '\u2661', 'S': '\u2664'}
VALUE_DEF = {1: 2, 2: 3, 3: 4, 4: 5, 5: 6,
             6: 7, 7: 8, 8: 9, 9: 10, 10: "J", 11: "Q", 12: "K", 13: "A"}
CARDS = []

PLAYERS_NAME = "Aidan"
PEOPLE.append(Me(PLAYERS_NAME, 0))


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.cards = CARDS


class Table:
    def __init__(self):
        self.pot = 0
        self.cards = []


def initialise() -> None:
    for x in range(0, PLAYER_NUM - 1):
        person = Player(NAMES[x], 0)
        PEOPLE.append(person)

    for key, _ in PRETTY_SUIT.items():
        for x in range(1, 14):
            card = Card(key, x)
            CARDS.append(card)
    # return PEOPLE, CARDS


def deal_hands(cards, me_cards) -> None:
    card_remove = [card for card in cards
                   if (card.suit == me_cards[0][0] or card.suit == me_cards[1][0])
                   and (card.value == me_cards[0][1] or card.value == me_cards[1][1])]
    for person in PEOPLE:
        # if person.is_main():
        #     for card in cards:
        #         if (card.suit == "H" or card.suit == "D") and card.value == 13:
        #             person.cards.append(card)
        #             cards.remove(card)
        #             print (len(cards))
        #     print(len(person.cards))
        #     print(person.cards[0].value, person.cards[0].suit)
        #     ic(
        #     f"{person.name} received:fire {VALUE_DEF[person.cards[0].value], PRETTY_SUIT[person.cards[0].suit]},"
        #     f" {VALUE_DEF[person.cards[1].value], PRETTY_SUIT[person.cards[1].suit]}")
        if person.is_main():
            for card in card_remove:
                person.cards.append(card)
                cards.remove(card)


    for person in PEOPLE:
        if not person.is_main():
            for _ in range(0, 2):
                # ic("cards" if cards else "Null")
                chosen_card = random.choice(cards)
                person.cards.append(chosen_card)
                cards.remove(chosen_card)  # Remove the chosen card from the deck
            # print(
            # f"{person.name} received: {VALUE_DEF[person.cards[0].value], PRETTY_SI[person.cards[0].suit]},"
            # f" {VALUE_DEF[person.cards[1].value], PRETTY_SI[person.cards[1].suit]}")


def deal_card(game_table, cards) -> None:
    chosen_card = random.choice(cards)
    game_table.cards.append(chosen_card)
    cards.remove(chosen_card)  # Remove the chosen card from the deck
    # print(f" {VALUE_DEF[game_table.cards[-1].value], PRETTY_SI[game_table.cards[-1].suit]}")


def deal_flop(game_table, cards) -> None:
    for _ in range(0, 3):
        deal_card(game_table, cards)


def check_hand(player, game_table) -> str:
    cards = game_table.cards + player.cards
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
    except TypeError as e:
        print(f"{e}: couldn't sort")
    try:
        player.additional_cards = sorted(player.additional_cards, reverse=True)
    except TypeError as e:
        print(f"{e}: couldn't sort")

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


def hand_ranking(player):
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
    ranked_players = []
    for rank in range(1, 11):
        compare = []
        for player in PEOPLE:
            if player.rank == rank:
                compare.append(player)
        for player in compare:
            # compare = sorted(compare, key=lambda x: x.hand_value, reverse = True)
            compare = sorted(compare, key=lambda x: (x.hand_value, x.additional_cards), reverse=True)
        for player in compare:
            ranked_players.append(player)
    return ranked_players

def main():
    initialise()

    START_TIME = time.time()
    for _ in range(0, 10000):
        # print("reset")
        for player in PEOPLE:
            player.rank = None
            player.hand_value = []
            player.hand = None
            player.cards = []
        cards = []
        for key, _ in PRETTY_SUIT.items():
            for r in range(1, 14):
                card = Card(key, r)
                cards.append(card)

        game_table = Table()
        deal_hands(cards, [["H",13],["D",13]])
        # print("Table:")
        deal_flop(game_table, cards)
        deal_card(game_table, cards)
        deal_card(game_table, cards)

        for player in PEOPLE:
            player.hand = check_hand(player, game_table)

            hand_ranking(player)

        PEOPLE_RANK = player_ranking()
        PREVIOUS_PLY = None
        INDEX = 1

        for player in PEOPLE_RANK:
            if PREVIOUS_PLY:
                if [player.hand, player.hand_value, player.additional_cards] != [PREVIOUS_PLY.hand,
                                                                                    PREVIOUS_PLY.hand_value,
                                                                                    PREVIOUS_PLY.additional_cards]:
                    INDEX += 1
                    player.rank = INDEX
                else:
                    player.rank = INDEX
            else:
                player.rank = INDEX
            PREVIOUS_PLY = player
        # for player in PEOPLE_RANK:
        #     pass
        #     ic(f"{player.name} Got a: {player.hand}, ranking: {player.rank}")
        for player in PEOPLE_RANK:
            if player.name == "Aidan":
                player.ranks.append(player.rank)
                if player.rank == 1:
                    player.wins += 1
        # print (len(cards))

    END_TIME = time.time()
    TOTAL_TIME = END_TIME - START_TIME

    for player in PEOPLE_RANK:
        if player.name == "Aidan":
            rank_values = {i: player.ranks.count(i) for i in player.ranks}
            rank_values = dict(sorted(rank_values.items(), reverse=True))
            plt.bar(range(len(rank_values)), list(rank_values.values()), align='center')
            plt.xticks(range(len(rank_values)), list(rank_values.keys()))
            ic(rank_values)
            ic(f"{player.wins / 100}%")
            ic("time taken to run 10000 games =", TOTAL_TIME)
            plt.show()
main()
