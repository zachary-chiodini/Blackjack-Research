from blackjack import Hand, Player


class BasicStrategy(Player):

    def __init__(self):
        super().__init__(0)
        self.name = 'Basic Strategy'
        self.decision_tree = {}

    def call(self, hand: Hand) -> str:
        pass
