import cv2
import easyocr
from numpy import ndarray

import text_read.player_bounderies as feed
from text_read.players import Player as PlayerStatus

class GameTable:
    """
    Class of the game
    """
    def __init__(self) -> None:
        # Classes
        self.img = feed.Reader()
        self.player_dict: dict[PlayerStatus] = {}

        # Veriables
        self.pot = 0
        self.cards = []
        self.bounderies = feed.BOUNDERIES

    def table_feed(self) -> None:
        """
        Set up of getting the cv2.frames
        """
        image_dict = self.img.get_feeds()

        for n, feeds in image_dict.items():
            if n == 'pot':
                self.pot = self.get_pot(feeds)
            else:
                seat = self.create_status(n, feeds)
                if seat:
                    # Adds class to dictionary
                    self.player_dict[n] = seat
                else:
                    # Deletes any none players (i.e. 'Empty')
                    try:
                        del self.player_dict[n]
                    except KeyError as e:
                        print(f"{e}: Doesn't exist")

    def create_status(self, seat_name: str, box_bounderies: ndarray) -> PlayerStatus:
        """
        Creates Player classes for new players or changes the status of existing players
        """
        player_name, bet, fold = self.get_seat_info(seat_name, box_bounderies)
        # print(f'name: {player_name}, bet: {bet}, has_folded: {fold}')

        if player_name:
            print(self.player_dict)
            # Adds player if spot is empty
            # If players name on the table isn't in the dictionary of player names
            if seat_name not in self.player_dict:
                player = PlayerStatus(player_name, bet)
                player.set_fold(fold)
                return player

            # If Name is in player dictionary
            # Changes status of the amount they have bet and also the fold status
            elif seat_name in self.player_dict:
                old_player: PlayerStatus = self.player_dict[seat_name] # Gets class

                if player_name == old_player.get_name(): # SET FOLD STATUS HERE
                    old_player.set_bet(bet)
                    old_player.set_fold(fold)
                    return old_player

                else:
                    # MAYBE SOMETHING TODO WITH SENDING OLD PLAYER DATA TO SERVER BEFORE MAKING NEW ONE
                    player = PlayerStatus(player_name, bet)
                    player.set_fold(fold)
                    return old_player

        else:
            # SEND OLD PLAYER DATA TO DATABASE (If word is 'Empty')
            print('this could be the empty seat')
            return None

    def get_seat_info(self, name: str, area_bounderies: ndarray) -> tuple[str, int, bool]:
        """
        Retrieval of seats info, i.e. gets name of player on the seat and their bet
        """
        reader = easyocr.Reader(['en'])
        result = reader.readtext(area_bounderies)

        find_name = self.bounderies[name][0]
        find_bet = self.bounderies[name][1]
        find_fold = self.bounderies[name][2]
        player_name, bet = '', 0

        for found in result:
            if found[1] == 'Empty':
                return player_name, bet, False

            elif find_name[0][0] <= found[0][0][0] and find_name[0][1] <= found[0][0][1]: # Point top left
                if find_name[1][0] >= found[0][2][0] and find_name[1][1] >= found[0][2][1]: # Point bottom right
                    player_name = found[1]

            elif find_bet[0][0] <= found[0][0][0] and find_bet[0][0] <= found[0][0][1]: # Point top left
                if find_bet[1][0] >= found[0][2][0] and find_bet[1][1] >= found[0][2][1]: # Point bottom right
                    bet = self.clean_bet(found[1])

        return player_name, bet, self.is_folded(find_fold, area_bounderies)

    def is_folded(self, is_cards: tuple[int,int], area_bounderies: ndarray) -> bool:
        """
        Checks if player has folded
        """
        x, y = is_cards

        gray = cv2.cvtColor(area_bounderies, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 185, 255, cv2.THRESH_BINARY_INV)

        if binary[y,x] == 0:
            return False
        return True

    def get_pot(self, box_bounderies: ndarray) -> int:
        """
        Gets the pot (int) of game
        """
        reader = easyocr.Reader(['en'])
        result = reader.readtext(box_bounderies)

        return self.clean_bet(result[0][1])

    def clean_bet(self, bet: str) -> int:
        """
        Cleans the OCR visuals (str) of the bet into a int
        """
        # Issue might arrise if it doesn't pick up the dollar sign
        bet = bet[1:]
        bet = ''.join(filter(str.isdigit, bet))

        return int(bet)/100

    def player_count(self) -> int:
        """
        Returns numb of player in the game
        """
        return len(self.player_dict)
