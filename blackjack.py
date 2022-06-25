from random import randint, uniform
from time import sleep
from typing import Text, List, Tuple, Union

from nptyping import Int8, NDArray, Shape
from numpy import any as npany, array, all as npall, vectorize


SLEEP_INT = 1

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

    def show(self, indent: int = 10) -> str:
        top, bottom = '', ''
        for card in self.cards:
            rank, suit = card.show()
            top += f'|{rank} {suit}|'
            bottom += f'|{suit} {rank}|'
        top += '\n'
        bottom = (' ' * indent) + bottom
        return top + bottom

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
        self.cards = self.cards[self.cards_dealt:] + list(args)
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

    def add(self, *args: Card) -> None:
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


class Player:

    def __init__(self, n: int, chips: int = 1000):
        self.n = n
        self.hands: List[Hand] = []
        self.chips = chips
        self.total_bet = 0
        self.your_turn = False
        self.insurance = 0
        self.choices = {'h': self.hit, 's': self.stand, 'd': self.double,
                        'y': self.split, 'sur': self.surrender}

    def ask_for_insurance(self) -> int:
        input_ = str(input(f'Player {self.n}; Chips: {self.chips}; Insurance? (y/n) '))
        if input_.lower().replace('es', '').strip() == 'y' or input_.strip() == '1':
            price = self.total_bet // 2
            if self.chips >= price:
                self.chips -= price
                self.total_bet += price
                self.insurance = price
                return price
        self.insurance = 0
        return 0

    def call(self, hand: Hand) -> str:
        input_ = str(input(f'Chips: {self.chips}; Bet: {self.total_bet}; Your turn: '))
        if input_ not in self.choices:
            print(f'You must choose {self.choices.keys()}.')
            sleep(SLEEP_INT)
            return self.call(hand)
        return self.choices[input_](hand)

    def double(self, hand: Hand) -> str:
        if len(hand.cards) == 2:
            if self.chips >= hand.bet:
                self.chips -= hand.bet
                self.total_bet += hand.bet
                hand.bet += hand.bet
                self.your_turn = False
                return 'd'
        print('You are not allowed to double.')
        sleep(SLEEP_INT)
        return self.call(hand)

    @staticmethod
    def hit(*args) -> str:
        return 'h'

    def stand(self, *args) -> str:
        self.your_turn = False
        return 's'

    def lost(self, hand: Hand) -> None:
        self.hands.remove(hand)
        self.your_turn = False
        return None

    def place_bet(self, minimum_bet: int) -> bool:
        bet = input(f'Player {self.n}; Chips: {self.chips}; Place bet: ')
        if bet:
            try:
                bet = abs(int(bet))
            except ValueError:
                bet = 0
            if bet < minimum_bet:
                print(f'Minimum bet is {minimum_bet}.')
                sleep(SLEEP_INT)
                return self.place_bet(minimum_bet)
            elif bet <= self.chips:
                self.total_bet = 0
                self.hands.append(Hand(bet))
                self.total_bet += bet
                self.chips -= bet
                return True
        return False

    def push(self, hand: Hand) -> None:
        self.chips += hand.bet
        self.hands.remove(hand)
        self.your_turn = False
        return None

    def show_hand(self, *args: Hand) -> None:
        for hand_and_value in [f'{hand.show()}; Value: {hand.value}' for hand in args]:
            print(f"Player {self.n}: {hand_and_value}")
            sleep(SLEEP_INT)
        return None

    def split(self, hand: Hand) -> str:
        if len(hand.cards) == 2 and self.chips >= hand.bet:
            card1, card2 = hand.cards
            if card1.rank == card2.rank:
                self.chips -= hand.bet
                self.total_bet += hand.bet
                self.hands.remove(hand)
                self.hands.extend([Hand(hand.bet, card1), Hand(hand.bet, card2)])
                self.your_turn = False
                return 'y'
        print('You are not allowed to split.')
        sleep(SLEEP_INT)
        return self.call(hand)

    def surrender(self, hand: Hand) -> str:
        if len(hand.cards) == 2:
            self.chips += hand.bet // 2
            self.hands.remove(hand)
            self.your_turn = False
            return 'sur'
        print('You are not allowed to surrender.')
        sleep(SLEEP_INT)
        return self.call(hand)

    def use_insurance(self, hand: Hand) -> None:
        self.chips += self.insurance + hand.bet
        indent = len(f'Player {self.n} insured hand ')
        print(f'Player {self.n} insured hand {hand.show(indent=indent)} for {self.insurance} chips.')
        print(f'You receive {hand.bet} chips insured with {self.insurance} chips insurance.')
        sleep(SLEEP_INT)
        return None

    def won(self, hand: Hand) -> None:
        self.chips += 2 * hand.bet
        self.hands.remove(hand)
        return None

    def won_blackjack(self, hand: Hand) -> None:
        self.chips += int(hand.bet * 2.5)
        self.hands.remove(hand)
        self.your_turn = False
        return None


class Dealer:

    def __init__(self, shoe: Shoe, tray: Tray):
        self.hand = Hand(bet=0)
        self.shoe = shoe
        self.tray = tray
        self.choices = {'h': self.hit, 's': self.void, 'd': self.hit,
                        'y': self.void, 'sur': self.surrender}

    def hand_below_seventeen(self) -> bool:
        val = self.hand.value
        return npany(val < 17) and not npany((17 <= val) & (val <= 21))

    def call_on(self, player: Player, hand: Hand) -> None:
        choice = player.call(hand)
        self.choices[choice](player, hand)
        return None

    def deal_card(self, *args: Hand, face_up=True) -> None:
        for hand in args:
            card = self.shoe.get_card()
            card.face_up = face_up
            hand.add(card)
        return None

    def deal_all(self, players: List[Player]) -> None:
        if self.tray.card_count() >= self.shoe.cut_off:
            self.tray.deck.shuffle()
            ratio = float(input('Deck cut ratio: '))
            self.tray.deck.cut(ratio)
            self.shoe.add(*self.tray.deck.cards)
            self.tray.empty()
            burner_card = self.shoe.get_card()
            self.tray.add(burner_card)
        for player in players:
            self.deal_card(player.hands[0])
        self.deal_card(self.hand, face_up=False)
        for player in players:
            self.deal_card(player.hands[0])
        self.deal_card(self.hand)
        return None

    def discard(self, *args: Hand) -> None:
        for hand in args:
            self.tray.add(*hand.cards)
        return None

    def face_hole_card(self) -> None:
        self.hand.cards[0].face_up = True
        return None

    def hit(self, player: Player, hand: Hand) -> None:
        self.deal_card(hand)
        player.show_hand(hand)
        return None

    def show_hand(self, face_hole_card=True) -> None:
        if face_hole_card:
            print(f'Dealer 0: {self.hand.show()}; Value: {self.hand.value}')
        else:
            print(f'Dealer 0: {self.hand.show()}; Value: {self.hand.cards[1].value}+')
        sleep(SLEEP_INT)
        return None

    def surrender(self, player: Player, hand: Hand) -> None:
        print(f'Player {player.n} surrendered hand.\n'
              f'You reclaim {hand.bet // 2} chips.')
        self.discard(hand)
        sleep(SLEEP_INT)
        return None

    @staticmethod
    def void(*args) -> None:
        pass


class Table:

    def __init__(self, players: int, decks: int, minimum_bet: int, penetration: float):
        deck = Deck()
        for i in range(decks):
            deck.generate()
        deck.shuffle()
        shoe, tray = Shoe(deck, penetration=penetration), Tray()
        self.dealer = Dealer(shoe, tray)
        self.players = [Player(i) for i in range(1, players + 1)]
        self.minimum_bet = minimum_bet

    def beat_house(self, hand: Hand) -> bool:
        winning_val_in = vectorize(
            lambda i: npany((self.dealer.hand.value < i) & (i <= 21)))
        return npany(winning_val_in(hand))

    @staticmethod
    def blackjack(hand: Hand) -> bool:
        return npany(hand.value == Int8(21))

    @staticmethod
    def bust(hand: Hand) -> bool:
        return npall(hand.value > Int8(21))

    def play(self) -> None:
        sleep(SLEEP_INT)
        self.dealer.discard(self.dealer.hand)
        self.dealer.hand = Hand(bet=0)
        current_players = []
        for player in self.players:
            if player.place_bet(self.minimum_bet):
                current_players.append(player)
        if not current_players:
            return None
        self.dealer.deal_all(current_players)
        self.dealer.show_hand(face_hole_card=False)
        for player in current_players:
            for hand in player.hands:
                player.show_hand(hand)
        face_up_card = self.dealer.hand.cards[1]
        if face_up_card.ace:
            for player in current_players:
                player.ask_for_insurance()
        if self.blackjack(self.dealer.hand):
            self.dealer.face_hole_card()
            self.dealer.show_hand()
            for player in current_players:
                for hand in player.hands.copy():
                    if self.blackjack(hand):
                        if player.insurance:
                            player.use_insurance(hand)
                        player.push(hand)
                        self.show_score(player, hand, 'tied')
                    else:
                        if player.insurance:
                            player.use_insurance(hand)
                            player.hands.remove(hand)
                        else:
                            player.lost(hand)
                            hand.bet += player.insurance
                            self.show_score(player, hand, 'lost')
                    self.dealer.discard(hand)
            return self.play()
        for player in current_players:
            player_hands_copy = player.hands.copy()
            for hand in player_hands_copy:
                player.your_turn = True
                player.show_hand(hand)
                if self.blackjack(hand):
                    player.won_blackjack(hand)
                    self.show_score(player, hand, 'won', blackjack=True)
                    self.dealer.discard(hand)
                while player.your_turn:
                    self.dealer.call_on(player, hand)
                    if len(player_hands_copy) < len(player.hands):
                        split_hands = player.hands[-2:]
                        self.dealer.deal_card(*split_hands)
                        player.show_hand(*split_hands)
                        player_hands_copy.extend(player.hands)
                    elif self.bust(hand):
                        player.lost(hand)
                        self.show_score(player, hand, 'lost')
                        self.dealer.discard(hand)
        self.dealer.face_hole_card()
        self.dealer.show_hand()
        if not any(player.hands for player in current_players):
            return self.play()
        while self.dealer.hand_below_seventeen():
            self.dealer.deal_card(self.dealer.hand)
            self.dealer.show_hand()
        if self.bust(self.dealer.hand):
            for player in current_players:
                for hand in player.hands.copy():
                    player.won(hand)
                    self.show_score(player, hand, 'won')
                    self.dealer.discard(hand)
            return self.play()
        for player in current_players:
            for hand in player.hands.copy():
                if self.beat_house(hand):
                    player.won(hand)
                    self.show_score(player, hand, 'won')
                elif self.tie_with_house(hand):
                    player.push(hand)
                    self.show_score(player, hand, 'tied')
                else:
                    player.lost(hand)
                    self.show_score(player, hand, 'lost')
                self.dealer.discard(hand)
        return self.play()

    @staticmethod
    def show_score(player: Player, hand: Hand, result: str, blackjack: bool = False) -> None:
        def if_result(s: str) -> int:
            return int(result == s)
        title = 'Winner' * if_result('won') + 'Loser' * if_result('lost') + 'Standoff' * if_result('tied')
        multiplier = (0.5 * int(blackjack)) + 1
        indent = len(f'{title}: ')
        print(f"Player {player.n} {result}{' Blackjack' * blackjack}!\n"
              f"{title}: {hand.show(indent=indent)}; Value: {hand.value}\n"
              f"You {result} {int(((result == 'won') * multiplier * hand.bet) + hand.bet)} chips.")
        sleep(SLEEP_INT)
        return None

    def tie_with_house(self, hand: Hand) -> bool:
        return npany(hand.value == self.dealer.hand.value)


if __name__ == '__main__':
    table = Table(players=2, decks=6, minimum_bet=50, penetration=0.75)
    table.play()
