from random import randint, uniform
from typing import Text, List, Tuple, Union

from numpy import array
from nptyping import Int8, NDArray, Shape


IntArray = NDArray[Shape['*'], Int8]


class Card:
    rank_map = {'A': array([11, 1], dtype=Int8), 'K': Int8(10), 'Q': Int8(10),
                'J': Int8(10), '10': Int8(10), '9': Int8(9), '8': Int8(8), '7': Int8(7),
                '6': Int8(6), '5': Int8(5), '4': Int8(4), '3': Int8(3), '2': Int8(2)}

    def __init__(self, rank: str, suit: Text, face_up=False):
        self.rank = rank
        self.suit = suit
        self.face_up = face_up
        self.value: Union[IntArray, Int8] = self.rank_map[rank]
        self.ace = rank == 'A'

    def show(self) -> Tuple[str, str]:
        if self.face_up:
            return self.rank, self.suit
        return '*', '*'


class Hand:

    def __init__(self, bet: int, *args: Card):
        self.cards: List[Card] = list(args)
        self.value: Union[IntArray, Int8] = Int8(0)
        self._add_values(*args)
        self.bet = bet

    def add(self, *args: Card) -> None:
        self.cards.extend(args)
        self._add_values(*args)
        return None

    def show(self) -> List[Tuple[str, str]]:
        return [card.show() for card in self.cards]

    def _add_values(self, *args: Card) -> None:
        for card in args:
            if card.ace and isinstance(self.value, IntArray):
                self.value += Int8(1)
            else:
                self.value += card.value
        return None


class Deck:
    ranks = {'A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2'}
    suits = {'\u2663', '\u2662', '\u2661', '\u2660'}

    def __init__(self):
        self.cards: List[Card] = []
        self.cards_dealt = 0

    def add(self, *args: Card) -> None:
        self.cards = self.cards[self.cards_dealt:] + args
        self.cards_dealt = 0
        return None

    def card_count(self) -> int:
        return len(self.cards) - self.cards_dealt

    def cut(self, ratio: float = 0.0) -> None:
        if self.cards:
            if not 0.0 < ratio < 1.0:
                ratio = uniform(0.0, 1.0)
            cut_index = int((len(self.cards) - 1) * ratio)
            self.cards = self.cards[cut_index:] + self.cards[:cut_index]
        return None

    def generate(self) -> None:
        for rank in self.ranks:
            for suit in self.suits:
                self.cards.append(Card(rank, suit))
        return None

    def get_card(self) -> Union[Card, None]:
        if self.cards_dealt == len(self.cards):
            return None
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


class Tray:

    def __init__(self):
        self.deck = Deck()

    def add(self, args: Card) -> None:
        self.deck.add(*args)
        return None

    def empty(self) -> None:
        self.deck = Deck()
        return None

    def card_count(self) -> int:
        return self.deck.card_count()


class Shoe:

    def __init__(self, deck: Deck, penetration: float = 0.75):
        self.deck = deck
        if not 0.0 < penetration < 1.0:
            penetration = 0.75
        self.cut_off = int(deck.card_count() * penetration)

    def add(self, *args: Card) -> None:
        self.deck.add(*args)
        return None

    def get_card(self) -> Card:
        return self.deck.get_card()
