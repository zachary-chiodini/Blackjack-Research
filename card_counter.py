from basic_strategy import BasicStrategy
from blackjack import Hand


class CardCounter(BasicStrategy):

    def __init__(self):
        super().__init__()
        self.name = 'Card Counter'
        self.running_count = 0
        self.true_count = 0

    def ask_for_insurance(self) -> None:
        pass

    def call(self, hand: Hand) -> str:
        pass

    def place_bet(self, minimum_bet: int) -> bool:
        pass

    def calc_true_count(self, round_to_nearest: int = 1) -> None:
        decks_remaining = len(self.dealer_ref.shoe.deck.cards) / 52
        self.true_count = round(decks_remaining / round_to_nearest) * round_to_nearest
        return None
