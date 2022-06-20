from typing import List, Optional, Tuple

from cards import Card, Deck, Hand


class Player:

    def __init__(self, n: int, chips: int = 100):
        self.hands = [Hand()]
        self.n = n
        self.chips = chips
        self.bet = 0
        self.choice = ''

    def show_hand(self) -> List[List[Tuple[str, str]]]:
        return [hand.show() for hand in self.hands]


class Dealer:

    def __init__(self, deck: Deck):
        self.hand = Hand()
        self.deck = deck

    def deal_card(self, hand: Hand, face_up=True) -> None:
        card = self.deck.get_card()
        card.face_up = face_up
        hand.add(card)
        return None

    def deal_all(self, *args: Player) -> None:
        for player in args:
            self.deal_card(player.hands[0])
        self.deal_card(self.hand)
        for player in args:
            self.deal_card(player.hands[0])
        self.deal_card(self.hand, face_up=False)
        return None

    def show_hand(self) -> List[Tuple[str, str]]:
        return self.hand.show()

    @staticmethod
    def split(player: Player, hand: Hand) -> None:
        card1, card2 = hand.cards
        player.hands.remove(hand)
        player.hands.extend(Hand(card1), Hand(card2))
        return None


class Table:
    pass
