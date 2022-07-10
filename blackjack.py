from random import randint, uniform
from time import sleep
from typing import Dict, Text, List, Tuple, Union

from nptyping import Int8, NDArray, Shape
from numpy import any as npany, array, all as npall, max as npmax, min as npmin


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
        self.ace = rank == 'A'
        self.value: Union[IntArray, Int8] = self.rank_map[rank]

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

    def beat(self, hand: 'Hand') -> bool:
        enemy_min, enemy_max = npmin(hand.value), npmax(hand.value)
        if enemy_max <= 21:
            return npany((21 >= self.value) & (self.value > enemy_max))
        if enemy_min <= 21:
            return npany((21 >= self.value) & (self.value > enemy_min))
        return True

    def blackjack(self) -> bool:
        return npany(self.value == Int8(21))

    def bust(self) -> bool:
        return npall(self.value > Int8(21))

    def has_ace(self) -> bool:
        return npany([card.ace for card in self.cards])

    def pair(self) -> bool:
        if len(self.cards) == 2:
            card1, card2 = self.cards
            return card1.rank == card2.rank
        return False

    def recalc_value(self) -> None:
        self.value = Int8(0)
        self._add_values(*self.cards)
        return None

    def show(self, text_before_cards: str = '') -> str:
        top, bottom = '', ''
        for card in self.cards:
            rank, suit = card.show()
            top += f'|{rank} {suit}|'
            bottom += f'|{suit} {rank}|'
        top += '\n'
        bottom = (' ' * len(text_before_cards)) + bottom
        return top + bottom

    def tie_with(self, hand: 'Hand') -> bool:
        return npany(self.value == hand.value)

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
        self.name = f'Player {n}'
        self.hands: List[Hand] = []
        self.chips = chips
        self.total_bet = 0
        self.insurance = 0
        self.dealer_ref: Union[Dealer, None] = None   # This is for robot players to use.
        self.choices = {'h': self.hit, 's': self.stand, 'd': self.double,
                        'y': self.split, 'sur': self.surrender}
        self._your_turn = False

    def ask_for_insurance(self) -> None:
        input_ = str(input(f'{self.name}; Chips: {self.chips}; Insurance? (y/n) '))
        if input_.lower().replace('es', '').strip() == 'y' or input_.strip() == '1':
            price = self.total_bet // 2
            if self.chips >= price:
                self.chips -= price
                self.total_bet += price
                self.insurance = price
                return None
        self.insurance = 0
        return None

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
                self.insurance = 0
                self._your_turn = False
                return 'd'
        print('You are not allowed to double.')
        sleep(SLEEP_INT)
        return self.call(hand)

    @staticmethod
    def hit(*args) -> str:
        return 'h'

    def stand(self, *args) -> str:
        self.insurance = 0
        self._your_turn = False
        return 's'

    def lost(self, hand: Hand) -> None:
        self.hands.remove(hand)
        self.show_score(hand, 'lost')
        self.insurance = 0
        self._your_turn = False
        return None

    def place_bet(self, minimum_bet: int) -> bool:
        def wrong_input_response() -> bool:
            print(f'Minimum bet is {minimum_bet} chips.')
            sleep(SLEEP_INT)
            return self.place_bet(minimum_bet)
        bet = input(f'{self.name}; Chips: {self.chips}; Place bet: ')
        if bet:
            try:
                bet = abs(int(bet))
            except ValueError:
                return wrong_input_response()
            if bet < minimum_bet:
                return wrong_input_response()
            if bet <= self.chips:
                self.total_bet = 0
                self.hands.append(Hand(bet))
                self.total_bet += bet
                self.chips -= bet
                self._your_turn = True
                return True
        return False

    def push(self, hand: Hand) -> None:
        self.chips += hand.bet
        self.hands.remove(hand)
        self.show_score(hand, 'tied')
        self.insurance = 0
        self._your_turn = False
        return None

    def show_hand(self, *args: Hand) -> None:
        for hand in args:
            print(f"{self.name}: {hand.show(f'{self.name}: ')}; Value: {hand.value}")
            sleep(SLEEP_INT)
        return None

    def show_score(self, hand: Hand, result: str, blackjack: bool = False) -> None:
        def if_result(s: str) -> int:
            return int(result == s)
        title = 'Winner' * if_result('won') + 'Loser' * if_result('lost') + 'Standoff' * if_result('tied')
        multiplier = (0.5 * int(blackjack)) + 1
        print(f"{self.name} {result}{' Blackjack' * blackjack}!\n"
              f"{title}: {hand.show(f'{title}: ')}; Value: {hand.value}\n"
              f"You {result} {int(((result == 'won') * multiplier * hand.bet) + hand.bet)} chips.")
        sleep(SLEEP_INT)
        return None

    def split(self, hand: Hand) -> str:
        if self.chips >= hand.bet and hand.pair():
            self.chips -= hand.bet
            self.total_bet += hand.bet
            self.insurance = 0
            self._your_turn = False
            return 'y'
        print('You are not allowed to split.')
        sleep(SLEEP_INT)
        return self.call(hand)

    def surrender(self, hand: Hand) -> str:
        if len(hand.cards) == 2:
            self.chips += hand.bet // 2
            self.hands.remove(hand)
            self.insurance = 0
            self._your_turn = False
            return 'sur'
        print('You are not allowed to surrender.')
        sleep(SLEEP_INT)
        return self.call(hand)

    def use_insurance(self, hand: Hand) -> None:
        self.chips += self.insurance + hand.bet
        self.insurance = 0
        print(f"{self.name} insured hand {hand.show(f'{self.name} insured hand ')} for {self.insurance} chips.")
        print(f'You receive {hand.bet} chips insured with {self.insurance} chips insurance.')
        if hand in self.hands:
            self.hands.remove(hand)
        self._your_turn = False
        sleep(SLEEP_INT)
        return None

    def won(self, hand: Hand) -> None:
        self.chips += 2 * hand.bet
        self.hands.remove(hand)
        self.show_score(hand, 'won')
        self.insurance = 0
        self._your_turn = False
        return None

    def won_blackjack(self, hand: Hand) -> None:
        self.chips += int(hand.bet * 2.5)
        self.hands.remove(hand)
        self.show_score(hand, 'won', blackjack=True)
        self.insurance = 0
        self._your_turn = False
        return None

    def your_turn(self) -> bool:
        if self._your_turn:
            return True
        self._your_turn = True
        return False


class Dealer:
    # Hi-Lo Card Counting System
    count_map = {0: 0, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 0, 8: 0, 9: 0, 10: -1, 11: -1}

    def __init__(self, shoe: Shoe, tray: Tray):
        self.hand = Hand(bet=0)
        self.shoe = shoe
        self.tray = tray
        self.running_count = 0
        self.players_hands: Dict[int, List[Hand]] = {}
        self.choices = {'h': self.hit, 's': self.void, 'd': self.hit,
                        'y': self.split, 'sur': self.surrender}

    def add_to_running_count(self, card: Card) -> None:
        self.running_count += self.count_map[npmax(card.value)]
        return None

    def hand_below_seventeen(self) -> bool:
        val = self.hand.value
        return npany(val < 17) and not npany((17 <= val) & (val <= 21))

    def call_on(self, player: Player, hand: Hand) -> None:
        player.dealer_ref = self  # This is for robot players to use.
        player.show_hand(hand)
        choice = player.call(hand)
        self.choices[choice](player, hand)
        return None

    def deal_card(self, *args: Hand, face_up=True) -> None:
        for hand in args:
            card = self.shoe.get_card()
            card.face_up = face_up
            hand.add(card)
            self.add_to_running_count(card)
        return None

    def deal_all(self, players: List[Player]) -> None:
        if self.tray.card_count() >= self.shoe.cut_off:
            self.running_count = 0
            self.tray.deck.shuffle()
            ratio = float(input('Deck cut ratio: '))
            self.tray.deck.cut(ratio)
            self.shoe.add(*self.tray.deck.cards)
            self.tray.empty()
            burner_card = self.shoe.get_card()
            burner_card.face_up = True
            print(Hand(0, burner_card).show())
            self.add_to_running_count(burner_card)
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
        hole_card = self.hand.cards[0]
        hole_card.face_up = True
        self.hand.recalc_value()
        self.add_to_running_count(hole_card)
        return None

    def face_up_card(self) -> Card:
        return self.hand.cards[1]

    def get_true_count(self) -> float:
        round_to_nearest_deck = 1.0
        true_count_decimals = 0
        decks_remaining = len(self.shoe.deck.cards) / 52
        decks_remaining = round(decks_remaining / round_to_nearest_deck) * round_to_nearest_deck
        return round(self.running_count / decks_remaining, true_count_decimals)

    def hit(self, player: Player, hand: Hand) -> None:
        self.deal_card(hand)
        return None

    def peek_at_hole_card(self) -> None:
        hole_card = self.hand.cards[0]
        hole_card.face_up = True
        return None

    def show_hand(self) -> None:
        print(f"Dealer 0: {self.hand.show(f'Dealer 0: ')}; Value: {self.hand.value}")
        sleep(SLEEP_INT)
        return None

    def split(self, player: Player, hand: Hand) -> None:
        card1, card2 = hand.cards
        player.hands.remove(hand)
        split_hands = [Hand(hand.bet, card1), Hand(hand.bet, card2)]
        player.hands.extend(split_hands)
        self.deal_card(*split_hands)
        player.show_hand(*split_hands)
        self.players_hands[player.n].extend(split_hands)
        return None

    def surrender(self, player: Player, hand: Hand) -> None:
        print(f'{player.name} surrendered hand.\n'
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
        for _ in range(decks):
            deck.generate()
        deck.shuffle()
        shoe, tray = Shoe(deck, penetration), Tray()
        self.dealer = Dealer(shoe, tray)
        self.players = [Player(i) for i in range(1, players + 1)]
        self.minimum_bet = minimum_bet

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
        self.dealer.show_hand()
        for player in current_players:
            for hand in player.hands:
                player.show_hand(hand)
        if self.dealer.face_up_card().ace:
            for player in current_players:
                player.ask_for_insurance()
        self.dealer.peek_at_hole_card()
        if self.dealer.hand.blackjack():
            self.dealer.face_hole_card()
            self.dealer.show_hand()
            for player in current_players:
                for hand in player.hands:
                    if hand.blackjack():
                        player.push(hand)
                    if player.insurance:
                        player.use_insurance(hand)
                    else:
                        player.lost(hand)
                    self.dealer.discard(hand)
            return self.play()
        for player in current_players:
            self.dealer.players_hands[player.n] = player.hands.copy()
            dealers_list_ref = self.dealer.players_hands[player.n]
            for hand in dealers_list_ref:
                if hand.blackjack():
                    player.won_blackjack(hand)
                    self.dealer.discard(hand)
                while player.your_turn():
                    self.dealer.call_on(player, hand)
                    if hand.bust():
                        player.lost(hand)
                        self.dealer.discard(hand)
        self.dealer.face_hole_card()
        self.dealer.show_hand()
        if not any(player.hands for player in current_players):
            return self.play()
        while self.dealer.hand_below_seventeen():
            self.dealer.deal_card(self.dealer.hand)
            self.dealer.show_hand()
        if self.dealer.hand.bust():
            for player in current_players:
                for hand in player.hands.copy():
                    player.won(hand)
                    self.dealer.discard(hand)
        for player in current_players:
            for hand in player.hands.copy():
                if hand.beat(self.dealer.hand):
                    player.won(hand)
                elif hand.tie_with(self.dealer.hand):
                    player.push(hand)
                else:
                    player.lost(hand)
                self.dealer.discard(hand)
        return self.play()


if __name__ == '__main__':
    table = Table(players=2, decks=6, minimum_bet=50, penetration=0.75)
    table.play()
