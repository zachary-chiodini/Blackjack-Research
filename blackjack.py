from time import sleep
from typing import List, Union

from nptyping import Int8
from numpy import any as npany, all as npall

from cards import Deck, Hand, Shoe, Tray


SLEEP_INT = 1


class Player:

    def __init__(self, n: int, chips: int = 1000):
        self.n = n
        self.hands: List[Hand] = []
        self.chips = chips
        self.total_bet = 0
        self.your_turn = False
        self.choices = {'h': self.hit, 's': self.stand, 'd': self.double,
                        'y': self.split, 'sur': self.surrender}

    def call(self, hand: Hand) -> str:
        input_ = str(input(f'Chips: {self.chips}\n'
                           f'Bet: {self.total_bet}\n'
                           'Your turn: '))
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
        self.total_bet = 0
        bet = abs(int(input(f'Player: {self.n}\nChips: {self.chips}\nPlace bet: ')))
        if bet:
            if bet < minimum_bet:
                print(f'Minimum bet is {minimum_bet}.')
                sleep(SLEEP_INT)
                return self.place_bet(minimum_bet)
            elif bet <= self.chips:
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

    def show_hand(self, hand: Hand) -> None:
        print(f'Player {self.n}: {hand.show()}; Value: {hand.value}')
        sleep(SLEEP_INT)
        return None

    def split(self, hand: Hand) -> str:
        if len(hand.cards) == 2:
            card1, card2 = hand.cards
            if card1.rank == card2.rank:
                self.hands.remove(hand)
                split_bet = hand.bet // 2
                self.hands.extend([Hand(split_bet, card1), Hand(split_bet, card2)])
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
        self.choices = {'h': self.hit, 's': self.void, 'd': self.double,
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
            ratio = float(input('Player: 1\nDeck cut ratio: '))
            self.tray.deck.cut(ratio)
            self.shoe.add(*self.tray.deck.cards)
            self.tray.empty()
            burner_card = self.shoe.get_card()
            self.tray.add(burner_card)
        for player in players:
            self.deal_card(player.hands[0])
        self.deal_card(self.hand)
        for player in players:
            self.deal_card(player.hands[0])
        self.deal_card(self.hand, face_up=False)
        return None

    def double(self, player: Player, hand: Hand) -> None:
        self.deal_card(hand)
        player.show_hand(hand)
        return None

    def discard(self, *args: Hand) -> None:
        for hand in args:
            self.tray.add(*hand.cards)
        return None

    def face_hole_card(self) -> None:
        self.hand.cards[1].face_up = True
        return None

    def hit(self, player: Player, hand: Hand) -> None:
        self.deal_card(hand)
        player.show_hand(hand)
        return None

    def show_hand(self, face_hole_card=True) -> None:
        if face_hole_card:
            print(f'Dealer 0: {self.hand.show()}; Value: {self.hand.value}')
        else:
            print(f'Dealer 0: {self.hand.show()}; Value: {self.hand.cards[0].value}+')
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
        house = self.dealer.hand.value
        house_bool = (17 <= house) & (house <= 21)
        hand_bool = (house < hand.value) & (hand.value <= 21)
        return npany(house_bool & hand_bool)

    @staticmethod
    def blackjack(hand: Hand) -> bool:
        return npany(hand.value == Int8(21))

    @staticmethod
    def bust(hand: Hand) -> bool:
        return npall(hand.value > Int8(21))

    def play(self) -> None:
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
        if self.blackjack(self.dealer.hand):
            for player in current_players:
                for hand in player.hands:
                    player.show_hand(hand)
            self.dealer.face_hole_card()
            self.dealer.show_hand()
            for player in current_players:
                for hand in player.hands:
                    if self.blackjack(hand):
                        player.push(hand)
                        self.show_score(player, hand, 'tied')
                        self.dealer.discard(hand)
                    else:
                        player.lost(hand)
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
                        for split_hand in split_hands:
                            player.show_hand(split_hand)
                        player_hands_copy.extend(player.hands)
                    elif self.bust(hand):
                        player.lost(hand)
                        self.show_score(player, hand, 'lost')
                        self.dealer.discard(hand)
        self.dealer.face_hole_card()
        self.dealer.show_hand()
        while self.dealer.hand_below_seventeen():
            self.dealer.deal_card(self.dealer.hand)
            self.dealer.show_hand()
        if self.bust(self.dealer.hand):
            for player in current_players:
                for hand in player.hands:
                    player.won(hand)
                    self.show_score(player, hand, 'won')
                    self.dealer.discard(hand)
            return self.play()
        for player in current_players:
            for hand in player.hands:
                if self.beat_house(hand):
                    player.won(hand)
                    self.show_score(player, hand, 'won')
                    self.dealer.discard(hand)
                elif self.tie_with_house(hand):
                    player.push(hand)
                    self.show_score(player, hand, 'tied')
                    self.dealer.discard(hand)
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
        multiplier = 0.5 * int(blackjack) + 1
        print(f"Player {player.n} {result}{' Blackjack' * blackjack}!\n"
              f"{title}: {hand.show()}; Value: {hand.value}\n"
              f"You {result} {int((result == 'won') * multiplier * hand.bet + hand.bet)} chips.")
        sleep(SLEEP_INT)
        return None

    def tie_with_house(self, hand: Hand) -> bool:
        return npany(hand.value == self.dealer.hand.value)


if __name__ == '__main__':
    table = Table(players=1, decks=6, minimum_bet=50, penetration=0.75)
    table.play()
