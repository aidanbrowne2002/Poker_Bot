import os
from numpy import ndarray
import cv2
from icecream import ic

import helper_scripts.card_info as cInfo
import helper_scripts.card_bounderies as card_bounderies
import text_read.ocr as player_feeds
from main import main as simulate

path = os.path.dirname(os.path.abspath(__file__))
train_ranks = cInfo.load_ranks( path + '/train_ranks/')
train_suits = cInfo.load_suits( path + '/train_suits/')

CARDS = card_bounderies.VideoFeeds()
PLAYERS = player_feeds.GameTable()
RANKS = {"two": 1, "three": 2, "four": 5, "five": 6, "six": 7,
             "seven": 6, "eight": 7, "nine": 8, "ten": 9,
             "jack": 10, "queen": 11, "king": 12, "ace": 13}

def convert_card(cards) -> list[list[str,int]]:
    ic(cards)
    return [[card[0][0].upper(), RANKS[card[1]]] for card in cards]

def gather_info() -> list[list[str,int]]:
    # Get cards from hand and community hand
    dict_feeds: dict[ndarray] = CARDS.get_feeds()
    k: int = 0
    cards_found: list[str, str, int, int] = []
    for _, card_cords in dict_feeds.items():
        cards_found.append(cInfo.process(card_cords))
        cards_found[k].best_rank_match, cards_found[k].best_suit_match = cInfo.match_card(cards_found[k],train_ranks,train_suits)

#         ic(f"""{cards_found[k].best_rank_match} | {cards_found[k].rank_diff}
# {cards_found[k].best_suit_match} | {cards_found[k].suit_diff}
# ------------------------------------------------""")
        k += 1

    # Get opponents status
    PLAYERS.table_feed()

    str_list_cards = [(cards_found[i].best_suit_match, cards_found[i].best_rank_match)
                      for i, _ in enumerate(cards_found)]

    # Change if you want to get all community cards also (FIX UNKNOWN ERROR)
    return convert_card(str_list_cards[-2:])


def check_turn() -> None:
    # Getting the check button
    img = cv2.VideoCapture(0)
    cords = (420, 425, 113, 62)
    x1,y1,w1,h1 = cords

    gather_on = False
    while True:
        _, frame = img.read()
        frame = frame[y1: y1+h1, x1:x1+w1]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        _, binary = cv2.threshold(gray, 39, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea,reverse=True)

        # Can comment this out - debug visual
        cv2.imshow('Video', cv2.drawContours(frame, contours, -1, (0,255,0), 2))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Incase theres nothing on screen
        try:
            size = cv2.contourArea(contours[0])
        except IndexError:
            size = 0

        if size > 4000 and size < 5000 and not gather_on: # Need something to make it run onces
            str_list_cards = gather_info()
            # RUN THE SIMULATION
            simulate(str_list_cards)
            gather_on = True
        elif size > 4000 and size < 5000 and gather_on:
            # Debug statement - could debug out
            pass
        elif size < 4000:
            gather_on = False
        else:
            ic('ERROR: Is the virtual camera on? Is OBS on?')

if __name__ == '__main__':
    check_turn()
