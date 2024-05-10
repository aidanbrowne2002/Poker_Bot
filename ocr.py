import easyocr
import vision as feed
from players import PlayerStatus
import time

class GameTable:
    def __init__(self) -> None:
        self.img = feed.Reader()
        self.player_dict: dict[PlayerStatus] = {}
        self.pot = None

    def table_feed(self):
        dict_feeds = self.img.get_feeds()

        for n, feeds in dict_feeds.items():
            if n == "pot":
                self.pot = self.clean_bet(feeds[0])
            else:
                seat = self.create_status(n, feeds)
                if seat:
                    self.player_dict[n] = seat
                elif n in self.player_dict:
                    del self.player_dict[n]

        print(self.player_dict)

    def create_status(self, name: str, result: list) -> PlayerStatus:
        player_name: str = self.get_name(result[0])
        bet: float = self.clean_bet(result[1])
        if name not in self.player_dict: # Adds player if spot is empty
            player = PlayerStatus(player_name, bet)
            return player

        elif name in self.player_dict:
            old_player: PlayerStatus = self.player_dict[name] # Gets class

            if player_name == old_player.get_name(): # SET FOLD STATUS HERE

                old_player.set_bet(bet)
                return player

            else:
                player = PlayerStatus(player_name, bet) # MAYBE SOMETHING TODO WITH SENDING OLD PLAYER DATA TO SERVER BEFORE MAKING NEW ONE
                return player

        else: # MAYBE SOMETHING TODO WITH SENDING OLD PLAYER DATA TO SERVER BEFORE MAKING NEW ONE (If word is empty seat)
            print('Possible that the only option is that the player seat is empty')
            return None


    def get_name(self, cords: tuple) -> str:
        reader = easyocr.Reader(['en'], gpu = True)
        result = reader.readtext(cords)

        if result:
            return str(result)
        return ""

    def clean_bet(self, cords: tuple) -> PlayerStatus:
        reader = easyocr.Reader(['en'])
        result = reader.readtext(cords)

        if result:
            bet = result[1:]
            if ',' in bet:
                bet = bet.replace(',','.')
            if '.' not in bet:
                bet = bet[:-2] + '.' + bet[-2:]
            return bet
        return 0

p = GameTable()
p.table_feed()
# How this script will work:
# 1. Check if new players are on the board (DONE)
#   . If theres a new player in that area replace them with privouse person (DONE)
#   . If empty leave it empty (DONE)
# 2. Add any new players with a class and dictionary of p1: class (DONE)
# 3. Monitor if fold popped up, Options:
#    . Every frame check if the word FOLD is popped up (SLOW)
#    . Brightness level of icon with CV2, help it idenitfying if player is not playing and folded
#    .
# 4. Update pot status of player (DONE)
# 5. When main players turn, it will send all the data for process

# Identify when game has ended
# 6. Check if pot is empty, if empty everyone who had fold status goes to false - FISHY (everyone could fold when theres no bet)
