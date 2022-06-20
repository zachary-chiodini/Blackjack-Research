from random import randint, uniform
from typing import Text, List, Tuple, Union


class Card:
    # Aces have a default value of 11.
    rank_map = {'A': 11, 'K': 10, 'Q': 10, 'J': 10, '10': 10, '9': 9,
                '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}

    def __init__(self, rank: str, suit: Text, face_up=False):
        self.rank = rank
        self.suit = suit
        self.face_up = face_up
        self.value: int = self.rank_map[rank]

    def show(self) -> Tuple[str, str]:
        if self.face_up:
            return self.rank, self.suit
        return '*', '*'


class Hand:

    def __init__(self, *args: Card):
        self.cards: List[Card] = list(args)
        self.value: int = self._sum_values(*args)

    def add(self, *args: Card) -> None:
        self.cards.extend(args)
        self.value += self._sum_values(*args)
        return None

    def show(self) -> List[Tuple[str, str]]:
        return [card.show() for card in self.cards]

    @staticmethod
    def _sum_values(*args: Card) -> Union[List[int], int]:
        return sum(card.value for card in args)


class Deck:
    ranks = {'A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2'}
    suits = {'\u2663', '\u2662', '\u2661', '\u2660'}

    def __init__(self):
        self.cards: List[Card] = []
        self.cards_dealt = 0

    def cut(self, ratio: float = 0.0) -> None:
        if self.cards:
            if not 0.0 < ratio < 1.0:
                ratio = uniform(0.0, 1.0)
            n = int((len(self.cards) - 1) * ratio)
            self.cards = self.cards[n:] + self.cards[:n]
        return None

    def generate(self) -> None:
        for rank in self.ranks:
            for suit in self.suits:
                self.cards.append(Card(rank, suit))
        return None

    def get_card(self) -> Card:
        card = self.cards[self.cards_dealt]
        self.cards_dealt += 1
        return card

    def shuffle(self) -> None:
        """This is a modern Fisher–Yates shuffle algorithm."""
        for i in range(len(self.cards) - 1, -1, -1):
            j = randint(0, i)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]
        self.cards_dealt = 0
        return None
