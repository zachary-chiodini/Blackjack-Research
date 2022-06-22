from typing import List, Tuple

from cards import Card, Deck, Hand, Shoe, Tray


class Player:

    def __init__(self, n: int, chips: int = 1000):
        self.n = n
        self.hands: List[Hand] = []
        self.chips = chips

    def double(self, hand: Hand) -> None:
        if self.chips <= hand.bet:
            self.chips -= hand.bet
            hand.bet *= 2
        return None

    def place_bet(self, minimum_bet: int) -> bool:
        if self.chips >= minimum_bet:
            bet = abs(int(input(f'Player: {self.n}\nChips: {self.chips}\nPlace bet: ')))
            if bet and bet < minimum_bet:
                print(f'Minimum bet is {minimum_bet}.')
                return self.place_bet(minimum_bet)
            else:
                self.hands.append(Hand(bet))
                self.chips -= bet
                return True
        return False

    def show_hand(self) -> List[List[Tuple[str, str]]]:
        return [hand.show() for hand in self.hands]

    def split(self, hand: Hand) -> None:
        card1, card2 = hand.cards
        self.hands.remove(hand)
        split_bet = int(hand.bet / 2)
        self.hands.extend(Hand(split_bet, card1), Hand(split_bet, card2))


class Dealer:

    def __init__(self, shoe: Shoe, tray: Tray):
        self.hand = Hand(bet=0)
        self.shoe = shoe
        self.tray = tray

    def deal_card(self, hand: Hand, face_up=True) -> None:
        card = self.shoe.deck.get_card()
        card.face_up = face_up
        hand.add(card)
        return None

    def deal_all(self, *args: Player) -> None:
        if self.tray.card_count >= self.shoe.cut_off:
            self.tray.deck.shuffle()
            ratio = float(input('Player: 1\nDeck cut ratio: '))
            self.tray.deck.cut(ratio)
            self.shoe.add(*self.tray.deck.cards)
            self.tray.empty()
        for player in args:
            self.deal_card(player.hands[0])
        self.deal_card(self.hand)
        for player in args:
            self.deal_card(player.hands[0])
        self.deal_card(self.hand, face_up=False)
        return None

    def discard(self, args: Card) -> None:
        self.tray.add(*args)
        return None

    def show_hand(self) -> List[Tuple[str, str]]:
        return self.hand.show()


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

    def play(self) -> None:
        current_players = []
        for player in self.players:
            if player.place_bet(self.minimum_bet):
                current_players.append(player)
        self.dealer.deal_all(*current_players)
        for player in current_players:
            pass

    def show(self) -> None:
        pass
