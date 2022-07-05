from basic_strategy import BasicStrategy
from blackjack import Card, Hand, npmax


class CardCounter(BasicStrategy):
    """
    Uses Hi-Lo Card Counting System with Basic Strategy.
    """
    count_map = {0: 0, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 0, 8: 0, 9: 0, 10: -1, 11: -1}

    def __init__(self):
        super().__init__()
        self.name = 'Card Counter'
        self.running_count = 0
        self.true_count = 0

    def ask_for_insurance(self) -> None:
        pass

    def call(self, hand: Hand) -> str:
        true_count = self.dealer_ref.get_true_count()
        return ''

    def place_bet(self, minimum_bet: int) -> bool:
        pass
