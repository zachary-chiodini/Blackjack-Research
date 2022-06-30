from blackjack import Card, Hand, npmax, npmin, Player, sleep, SLEEP_INT, Table


class BasicStrategy(Player):
    decision_tree = {
        'pair': {
            0: {
                'ace': {
                    0: {
                        'total': {
                            21: {'upcard': {2: 's', 3: 's', 4: 's', 5: 's', 6: 's',
                                            7: 's', 8: 's', 9: 's', 10: 's', 11: 's'}},
                            20: {'upcard': {2: 's', 3: 's', 4: 's', 5: 's', 6: 's',
                                            7: 's', 8: 's', 9: 's', 10: 's', 11: 's'}},
                            19: {'upcard': {2: 's', 3: 's', 4: 's', 5: 's', 6: 's',
                                            7: 's', 8: 's', 9: 's', 10: 's', 11: 's'}},
                            18: {'upcard': {2: 's', 3: 's', 4: 's', 5: 's', 6: 's',
                                            7: 's', 8: 's', 9: 's', 10: 's', 11: 's'}},
                            17: {'upcard': {2: 's', 3: 's', 4: 's', 5: 's', 6: 's',
                                            7: 's', 8: 's', 9: 's', 10: 's', 11: 's'}},
                            16: {'upcard': {2: 's', 3: 's', 4: 's', 5: 's', 6: 's',
                                            7: 'h', 8: 'h', 9: 'h', 10: 'h', 11: 'h'}},
                            15: {'upcard': {2: 's', 3: 's', 4: 's', 5: 's', 6: 's',
                                            7: 'h', 8: 'h', 9: 'h', 10: 'h', 11: 'h'}},
                            14: {'upcard': {2: 's', 3: 's', 4: 's', 5: 's', 6: 's',
                                            7: 'h', 8: 'h', 9: 'h', 10: 'h', 11: 'h'}},
                            13: {'upcard': {2: 's', 3: 's', 4: 's', 5: 's', 6: 's',
                                            7: 'h', 8: 'h', 9: 'h', 10: 'h', 11: 'h'}},
                            12: {'upcard': {2: 'h', 3: 'h', 4: 's', 5: 's', 6: 's',
                                            7: 'h', 8: 'h', 9: 'h', 10: 'h', 11: 'h'}},
                            11: {'upcard': {2: 'd', 3: 'd', 4: 'd', 5: 'd', 6: 'd',
                                            7: 'd', 8: 'd', 9: 'd', 10: 'd', 11: 'd'}},
                            10: {'upcard': {2: 'd', 3: 'd', 4: 'd', 5: 'd', 6: 'd',
                                            7: 'd', 8: 'd', 9: 'd', 10: 'h', 11: 'h'}},
                            9: {'upcard': {2: 'h', 3: 'd', 4: 'd', 5: 'd', 6: 'd',
                                           7: 'h', 8: 'h', 9: 'h', 10: 'h', 11: 'h'}},
                            8: {'upcard': {2: 'h', 3: 'h', 4: 'h', 5: 'h', 6: 'h',
                                           7: 'h', 8: 'h', 9: 'h', 10: 'h', 11: 'h'}},
                            7: {'upcard': {2: 'h', 3: 'h', 4: 'h', 5: 'h', 6: 'h',
                                           7: 'h', 8: 'h', 9: 'h', 10: 'h', 11: 'h'}},
                            6: {'upcard': {2: 'h', 3: 'h', 4: 'h', 5: 'h', 6: 'h',
                                           7: 'h', 8: 'h', 9: 'h', 10: 'h', 11: 'h'}},
                            5: {'upcard': {2: 'h', 3: 'h', 4: 'h', 5: 'h', 6: 'h',
                                           7: 'h', 8: 'h', 9: 'h', 10: 'h', 11: 'h'}},
                        }
                    },
                    1: {
                        'total': {
                            21: {'upcard': {2: 's', 3: 's', 4: 's', 5: 's', 6: 's',
                                            7: 's', 8: 's', 9: 's', 10: 's', 11: 's'}},
                            20: {'upcard': {2: 's', 3: 's', 4: 's', 5: 's', 6: 's',
                                            7: 's', 8: 's', 9: 's', 10: 's', 11: 's'}},
                            19: {'upcard': {2: 's', 3: 's', 4: 's', 5: 's', 6: 'ds',
                                            7: 's', 8: 's', 9: 's', 10: 's', 11: 's'}},
                            18: {'upcard': {2: 'ds', 3: 'ds', 4: 'ds', 5: 'ds', 6: 'ds',
                                            7: 's', 8: 's', 9: 'h', 10: 'h', 11: 'h'}},
                            17: {'upcard': {2: 'h', 3: 'd', 4: 'd', 5: 'd', 6: 'd',
                                            7: 'h', 8: 'h', 9: 'h', 10: 'h', 11: 'h'}},
                            16: {'upcard': {2: 'h', 3: 'h', 4: 'd', 5: 'd', 6: 'd',
                                            7: 'h', 8: 'h', 9: 'h', 10: 'h', 11: 'h'}},
                            15: {'upcard': {2: 'h', 3: 'h', 4: 'd', 5: 'd', 6: 'd',
                                            7: 'h', 8: 'h', 9: 'h', 10: 'h', 11: 'h'}},
                            14: {'upcard': {2: 'h', 3: 'h', 4: 'h', 5: 'd', 6: 'd',
                                            7: 'h', 8: 'h', 9: 'h', 10: 'h', 11: 'h'}},
                            13: {'upcard': {2: 'h', 3: 'h', 4: 'h', 5: 'd', 6: 'd',
                                            7: 'h', 8: 'h', 9: 'h', 10: 'h', 11: 'h'}}
                        }
                    }
                }
            },
            1: {
                'ace': {
                    0: {
                        'total': {
                            20: {'upcard': {2: 's', 3: 's', 4: 's', 5: 's', 6: 's',
                                            7: 's', 8: 's', 9: 's', 10: 's', 11: 's'}},
                            18: {'upcard': {2: 'y', 3: 'y', 4: 'y', 5: 'y', 6: 'y',
                                            7: 's', 8: 'y', 9: 'y', 10: 's', 11: 's'}},
                            16: {'upcard': {2: 'y', 3: 'y', 4: 'y', 5: 'y', 6: 'y',
                                            7: 'y', 8: 'y', 9: 'y', 10: 'y', 11: 'y'}},
                            14: {'upcard': {2: 'y', 3: 'y', 4: 'y', 5: 'y', 6: 'y',
                                            7: 'y', 8: 'h', 9: 'h', 10: 'h', 11: 'h'}},
                            12: {'upcard': {2: 'y', 3: 'y', 4: 'y', 5: 'y', 6: 'y',
                                            7: 'h', 8: 'h', 9: 'h', 10: 'h', 11: 'h'}},
                            10: {'upcard': {2: 'd', 3: 'd', 4: 'd', 5: 'd', 6: 'd',
                                            7: 'd', 8: 'd', 9: 'd', 10: 'h', 11: 'h'}},
                            8: {'upcard': {2: 'h', 3: 'h', 4: 'h', 5: 'y', 6: 'y',
                                           7: 'h', 8: 'h', 9: 'h', 10: 'h', 11: 'h'}},
                            6: {'upcard': {2: 'y', 3: 'y', 4: 'y', 5: 'y', 6: 'y', 7: 'y',
                                           8: 'h', 9: 'h', 10: 'h', 11: 'h'}},
                            4: {'upcard': {2: 'y', 3: 'y', 4: 'y', 5: 'y', 6: 'y', 7: 'y',
                                           8: 'h', 9: 'h', 10: 'h', 11: 'h'}}
                        }
                    },
                    1: {
                        'total': {
                            12: {'upcard': {2: 'y', 3: 'y', 4: 'y', 5: 'y', 6: 'y',
                                            7: 'y', 8: 'y', 9: 'y', 10: 'y', 11: 'y'}}
                        }
                    }
                }
            }
        }
    }

    def __init__(self):
        super().__init__(0)
        self.name = 'Basic Strategy'

    def ask_for_insurance(self) -> None:
        pass

    def call(self, hand: Hand) -> str:
        up_card = self.dealer_ref.hand.cards[1]
        choice = self.decision(hand, up_card)
        if choice == 'ds':
            if len(hand.cards) == 2:
                choice = 'd'
            else:
                choice = 's'
        return self.choices[choice](hand)

    def decision(self, hand: Hand, up_card: Card) -> str:
        min_, max_ = npmin(hand.value), npmax(hand.value)
        if max_ > 21:
            total = min_
        else:
            total = max_
        return self.decision_tree['pair'][int(hand.pair())]['ace'][int(hand.has_ace())]\
            ['total'][int(total)]['upcard'][int(npmax(up_card.value))]

    def place_bet(self, minimum_bet: int) -> bool:
        if self.chips >= minimum_bet:
            self.total_bet = 0
            self.hands.append(Hand(minimum_bet))
            self.total_bet += minimum_bet
            self.chips -= minimum_bet
            self._your_turn = True
            f'{self.name}; Chips: {self.chips}; Place bet: {minimum_bet}'
            sleep(SLEEP_INT)
            return True
        return False


if __name__ == '__main__':
    table = Table(players=2, decks=6, minimum_bet=50, penetration=0.75)
    table.players = [Player(1), BasicStrategy()]
    table.play()
