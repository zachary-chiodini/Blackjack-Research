from typing import List, NoReturn, Tuple

from nptyping import Int8
from numpy import any as npany, all as npall

from cards import Deck, Hand, Shoe, Tray


class Player:

    def __init__(self, n: int, chips: int = 1000):
        self.n = n
        self.hand: List[Hand] = []
        self.chips = chips
        self.total_bet = 0
        self.choices = {'h': self.void, 's': self.void, 'd': self.double,
                        'y': self.split, 'sur': self.surrender}

    def call(self, hand: Hand) -> str:
        input_ = str(input(f'Player: {self.n}\nChips: {self.chips}\nBet: {self.total_bet}\n Your turn: '))
        if input_ not in self.choices:
            print(f'You must choose {self.choices.keys()}.')
            return self.call()
        self.choices[input_](hand)
        return input_

    def double(self, hand: Hand) -> None:
        if self.chips <= hand.bet:
            self.chips -= hand.bet
            self.total_bet += hand.bet
            hand.bet *= 2
        return None

    def place_bet(self, minimum_bet: int) -> bool:
        self.total_bet = 0
        if self.chips >= minimum_bet:
            bet = abs(int(input(f'Player: {self.n}\nChips: {self.chips}\nPlace bet: ')))
            if bet:
                if bet < minimum_bet:
                    print(f'Minimum bet is {minimum_bet}.')
                    return self.place_bet(minimum_bet)
                else:
                    self.hand.append(Hand(bet))
                    self.total_bet += bet
                    self.chips -= bet
                    return True
        return False

    def push(self, hand: Hand) -> None:
        self.chips += hand.bet
        return None

    def show_hand(self) -> List[List[Tuple[str, str]]]:
        return [hand.show() for hand in self.hand]

    def split(self, hand: Hand) -> None:
        card1, card2 = hand.cards
        self.hand.remove(hand)
        split_bet = hand.bet // 2
        self.hand.extend(Hand(split_bet, card1), Hand(split_bet, card2))
        return None

    def surrender(self, hand: Hand) -> None:
        self.chips += hand.bet // 2
        return None

    def won(self, hand: Hand) -> None:
        self.chips += 2 * hand.bet
        return None

    def won_blackjack(self, hand: Hand) -> None:
        self.chips += int(hand.bet * 1.5)
        return None

    @staticmethod
    def void(*args) -> None:
        pass


class Dealer:

    def __init__(self, shoe: Shoe, tray: Tray):
        self.hand = Hand(bet=0)
        self.shoe = shoe
        self.tray = tray
        self.choices = {'h': self.deal_card, 's': self.void, 'd': self.deal_card,
                        'y': self.void, 'sur': self.discard}

    def below_seventeen(self) -> bool:
        return not npany(Int8(21) >= self.hand.value >= Int8(17))

    def call_on(self, player: Player, hand: Hand) -> None:
        choice = player.call(hand)
        self.choices[choice](hand)
        return None

    def deal_card(self, hand: Hand, face_up=True) -> None:
        card = self.shoe.get_card()
        card.face_up = face_up
        hand.add(card)
        return None

    def deal_all(self, players: List[Player]) -> None:
        if self.tray.card_count >= self.shoe.cut_off:
            self.tray.deck.shuffle()
            ratio = float(input('Player: 1\nDeck cut ratio: '))
            self.tray.deck.cut(ratio)
            self.shoe.add(*self.tray.deck.cards)
            self.tray.empty()
            burn_card = self.shoe.get_card()
            self.tray.add(burn_card)
        for player in players:
            self.deal_card(player.hand[0])
        self.deal_card(self.hand)
        for player in players.copy():
            self.deal_card(player.hand[0])
        self.deal_card(self.hand, face_up=False)
        return None

    def discard(self, player: Player, hand: Hand) -> None:
        if isinstance(player.hand, list):
            player.hand.remove(hand)
        else:
            player.hand = Hand(0)
        self.tray.add(*hand.cards)
        return None

    def face_hole_card(self) -> None:
        self.hand.cards[1].face_up = True
        return None

    def show_hand(self) -> List[Tuple[str, str]]:
        return self.hand.show()

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
        return npany(hand.value > self.dealer.hand.value)

    @staticmethod
    def blackjack(hand: Hand) -> bool:
        return npany(hand.value == Int8(21))

    @staticmethod
    def bust(hand: Hand) -> bool:
        return npall(hand.value > Int8(21))

    def play(self) -> NoReturn:
        while True:
            current_players = []
            for player in self.players:
                if player.place_bet(self.minimum_bet):
                    current_players.append(player)
            self.dealer.deal_all(current_players)
            for player in current_players:
                for hand in player.hand:
                    self.dealer.call_on(player, hand)
                    if self.blackjack(hand):
                        player.won_blackjack(hand)
                        self.dealer.discard(hand)
                    elif self.bust(hand):
                        self.dealer.discard(hand)
            self.dealer.face_hole_card()
            while self.dealer.below_seventeen():
                self.dealer.deal_card(self.dealer.hand)
            if self.bust(self.dealer.hand):
                for player in current_players:
                    for hand in player.hand:
                        player.won(hand)
            else:
                for player in current_players:
                    for hand in player.hand:
                        if self.beat_house(hand):
                            player.won(hand)
                            self.dealer.discard(hand)
                        elif self.tie_with_house(hand):
                            player.push(hand)
                            self.dealer.discard(hand)
                        else:
                            self.dealer.discard(hand)
            self.dealer.discard(self.dealer.hand)

    def show(self) -> None:
        pass

    def tie_with_house(self, hand: Hand) -> bool:
        return npany(hand.value == self.dealer.hand.value)
