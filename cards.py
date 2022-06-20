from random import randint
from typing import Text, List, Tuple


class Card:
    # Aces have a default value of 11.
    rank_map = {'A': 11, 'K': 10, 'Q': 10, 'J': 10, '10': 10, '9': 9,
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
        self.value = self._sum_values(*args)

    def add(self, *args: Card) -> None:
        self.cards.extend(args)
        self.value += self._sum_values(*args)
        return None

    def show(self) -> List[Tuple[str, str]]:
        return [card.show() for card in self.cards]

    def _sum_values(*args: Card) -> int:
        return sum(card.value for card in args)


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
        """This is a modern Fisher–Yates shuffle algorithm."""
        for i in range(len(self.cards) - 1, -1, -1):
            j = randint(0, i)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]
        return None
