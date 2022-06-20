from random import randint
from typing import Text, List, Tuple


class Card:
    rank_map = {'A': 1, 'K': 10, 'Q': 10, 'J': 10, '10': 10, '9': 9,
                '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}

    def __init__(self, rank: str, suit: Text, face_up=False):
        self.rank = rank
        self.suit = suit
        self.face_up = face_up
        self.value = self.rank_map[rank]

    def show(self) -> Tuple[str, str]:
        if self.face_up:
            return self.rank, self.suit
        return '*', '*'


class Hand:

    def __init__(self, *args: Card):
        self.cards: List[Card] = list(args)
        self.value: int = sum(card.value for card in args)

    def add(self, card: Card):
        self.cards.append(card)
        self.value += card.value
        return None

    def show(self) -> List[Tuple[str, str]]:
        return [card.show() for card in self.cards]


class Deck:
    ranks = {'A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2'}
    suits = {'\u2663', '\u2662', '\u2661', '\u2660'}

    def __init__(self):
        self.cards: List[Card] = []

    def generate(self) -> None:
        for rank in self.ranks:
            for suit in self.suits:
                self.cards.append(Card(rank, suit))
        return None

    def shuffle(self) -> None:
        for i in range(len(self.cards) - 1, -1, -1):
            j = randint(0, i)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]
        return None

    def _show(self) -> List[Tuple[str, str]]:
        return [card.show() for card in self.cards]
