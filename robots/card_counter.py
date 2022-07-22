from typing import Callable

from robots.basic_strategy import BasicStrategy
from blackjack import Hand, Player, sleep, Table


class CardCounter(BasicStrategy):

    def __init__(self):
        super().__init__()
        self.name = 'Card Counter'
        self._apply_deviations()

    def ask_for_insurance(self) -> None:
        if self.dealer_ref and self.dealer_ref.get_true_count() >= 3:
            price = self.total_bet // 2
            if self.chips >= price:
                self.chips -= price
                self.total_bet += price
                self.insurance = price
                return None
        self.insurance = 0
        return None

    def call(self, hand: Hand) -> str:
        up_card = self.dealer_ref.hand.cards[1]
        choice = self.decision(hand, up_card)
        if isinstance(choice, Callable):
            choice = choice()
        if choice == 'ds':
            if len(hand.cards) == 2:
                choice = 'd'
            else:
                choice = 's'
        return self.choices[choice](hand)

    def place_bet(self, minimum_bet: int) -> bool:
        if self.dealer_ref:
            true_count = self.dealer_ref.get_true_count()
        else:
            true_count = 0.0
        if true_count <= 0.0:
            bet = minimum_bet
        else:
            bet = int(minimum_bet + minimum_bet * true_count)
        if bet <= self.chips:
            print(f'{self.name}; Chips: {self.chips}; Place bet: {bet}')
            sleep(self.sleep_int)
            self.total_bet = 0
            self.hands.append(Hand(bet))
            self.total_bet += bet
            self.chips -= bet
            self.rounds += 1
            self._your_turn = True
            return True
        return False

    def show_hand(self, *args: Hand) -> None:
        if self.dealer_ref:
            true_count = f'; Count: {self.dealer_ref.get_true_count()}'
        else:
            true_count = ''
        for hand in args:
            print(f"{self.name}: {hand.show(f'{self.name}: ')}; Value: {hand.value}{true_count}")
            sleep(self.sleep_int)
        return None

    def _apply_deviations(self) -> None:
        self.decision_tree['pair'][False]['ace'][False]['total'][16]['upcard'][9] = \
            lambda: 's' if self.dealer_ref.get_true_count() >= 5 else 'h'
        self.decision_tree['pair'][False]['ace'][False]['total'][16]['upcard'][10] = \
            lambda: 's' if self.dealer_ref.get_true_count() >= 0 else 'h'
        self.decision_tree['pair'][False]['ace'][False]['total'][15]['upcard'][10] = \
            lambda: 's' if self.dealer_ref.get_true_count() >= 4 else 'h'
        self.decision_tree['pair'][False]['ace'][False]['total'][13]['upcard'][2] = \
            lambda: 'h' if self.dealer_ref.get_true_count() < -1 else 's'
        self.decision_tree['pair'][False]['ace'][False]['total'][13]['upcard'][3] = \
            lambda: 'h' if self.dealer_ref.get_true_count() < -2 else 's'
        self.decision_tree['pair'][False]['ace'][False]['total'][12]['upcard'][2] = \
            lambda: 's' if self.dealer_ref.get_true_count() >= 4 else 'h'
        self.decision_tree['pair'][False]['ace'][False]['total'][12]['upcard'][3] = \
            lambda: 's' if self.dealer_ref.get_true_count() >= 2 else 'h'
        self.decision_tree['pair'][False]['ace'][False]['total'][12]['upcard'][4] = \
            lambda: 's' if self.dealer_ref.get_true_count() >= 0 else 's'
        self.decision_tree['pair'][False]['ace'][False]['total'][12]['upcard'][5] = \
            lambda: 'h' if self.dealer_ref.get_true_count() < -1 else 's'
        self.decision_tree['pair'][False]['ace'][False]['total'][12]['upcard'][6] = \
            lambda: 'h' if self.dealer_ref.get_true_count() < -1 else 's'
        self.decision_tree['pair'][False]['ace'][False]['total'][11]['upcard'][11] = \
            lambda: 'd' if self.dealer_ref.get_true_count() >= -1 else 'd'
        self.decision_tree['pair'][False]['ace'][False]['total'][10]['upcard'][10] = \
            lambda: 'd' if self.dealer_ref.get_true_count() >= 4 else 'h'
        self.decision_tree['pair'][False]['ace'][False]['total'][10]['upcard'][11] = \
            lambda: 'd' if self.dealer_ref.get_true_count() >= 4 else 'h'
        self.decision_tree['pair'][False]['ace'][False]['total'][9]['upcard'][2] = \
            lambda: 'd' if self.dealer_ref.get_true_count() >= 1 else 'h'
        self.decision_tree['pair'][False]['ace'][False]['total'][9]['upcard'][7] = \
            lambda: 'd' if self.dealer_ref.get_true_count() >= 4 else 'h'
        self.decision_tree['pair'][True]['ace'][False]['total'][20]['upcard'][5] = \
            lambda: 'y' if self.dealer_ref.get_true_count() >= 5 else 's'
        self.decision_tree['pair'][True]['ace'][False]['total'][20]['upcard'][6] = \
            lambda: 'y' if self.dealer_ref.get_true_count() >= 5 else 's'
        return None


if __name__ == '__main__':
    table = Table(players=2, decks=6, minimum_bet=50, penetration=0.75)
    table.players = [Player(1), CardCounter()]
    table.play()
