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

    def calc_true_count(self, round_to_nearest: float = 1.0) -> None:
        decks_remaining = len(self.dealer_ref.shoe.deck.cards) / 52
        decks_remaining = round(decks_remaining / round_to_nearest) * round_to_nearest
        self.true_count = int(round(self.running_count / decks_remaining))
        return None
