from typing import List, Optional, Tuple

from cards import Card, Deck, Hand


class Player:

    def __init__(self, n: int, chips: int = 1000):
        self.n = n
        self.hands = [Hand()]
        self.chips = chips
        self.bet = 0
        self.choice = ''

    def place_bet(self, minimum_bet: int) -> None:
        if self.chips >= minimum_bet:
            bet = abs(int(input(f'Player: {self.n}\nChips: {self.chips}\nPlace bet: ')))
            if bet and bet < minimum_bet:
                print(f'Minimum bet is {minimum_bet}.')
                return self.place_bet(minimum_bet)
            else:
                self.bet = bet
                self.chips -= bet
        else:
            self.bet = 0
        return None

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

    def __init__(self, players: int, decks: int, minimum_bet: int):
        self.deck = Deck()
        for i in range(decks):
            self.deck.generate()
        self.deck.shuffle()
        self.minimum_bet = minimum_bet
        self.dealer = Dealer(self.deck)
        self.players = [Player(i) for i in range(1, players + 1)]

    def play(self) -> None:
        current_players = []
        for player in self.players:
            player.place_bet(self.minimum_bet)
            if player.bet:
                current_players.append(player)
        self.dealer.deal_all(*current_players)
        for player in current_players:
            pass

    def show(self) -> None:
        pass
