class PlayerStatus:
    def __init__(self, name, bet) -> None:
        self.name: str = name
        self.fold_status: bool = False
        self.bet: float = bet

    def change_name(self, name, bet) -> None:
        self.name = name
        self.bet = bet

    def set_bet(self, bet) -> None:
        self.bet = bet

    def set_fold(self, fold) -> None:
        self.fold_status = fold

    def get_name(self) -> str:
        return self.name