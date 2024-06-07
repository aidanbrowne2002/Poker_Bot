class Player:
    def __init__(self, name, style) -> None:
        self.name = name
        self.style = style
        self.cards = []
        self.hand = None
        self.hand_value = []
        self.additional_cards = []
        self.rank = None
        self.fold_status = False
        self.bet = 0

    def is_main(self) -> bool:
        if hasattr(self, "main"):
            return True
        return False

    def change_name(self, name, bet) -> None:
        self.name = name
        self.bet = bet

    def set_bet(self, bet) -> None:
        self.bet = bet

    def set_fold(self, fold) -> None:
        self.fold_status = fold

    def get_name(self) -> str:
        return self.name

    def get_info(self) -> str:
        return f'name: {self.name}, bet: {self.bet}, fold_status: {self.fold_status}'

class Me(Player):
    def __init__(self, name, style):
        Player.__init__(self, name, style)
        self.main = True
        self.wins = 0
        self.ranks = []
