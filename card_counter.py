from typing import Callable

from basic_strategy import BasicStrategy
from blackjack import Hand, sleep, SLEEP_INT


class CardCounter(BasicStrategy):
    decision_tree = {
        'pair': {
            False: {
                'ace': {
                    False: {
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
                    True: {
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
            True: {
                'ace': {
                    False: {
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
                    True: {
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
        super().__init__()
        self.name = 'Card Counter'
        self._apply_deviations()

    def ask_for_insurance(self) -> None:
        if self.dealer_ref.get_true_count() >= 3:
            price = self.total_bet // 2
            if self.chips >= price:
                self.chips -= price
                self.total_bet += price
                self.insurance = price
                return None
        self.insurance = 0
        return None

    def call(self, hand: Hand) -> str:
        up_card = self.dealer_ref.hand.cards[1]
        choice = self.decision(hand, up_card)
        if isinstance(choice, Callable):
            choice = choice()
        if choice == 'ds':
            if len(hand.cards) == 2:
                choice = 'd'
            else:
                choice = 's'
        return self.choices[choice](hand)

    def place_bet(self, minimum_bet: int) -> bool:
        pass

    def show_hand(self, *args: Hand) -> None:
        for hand in args:
            print(f"{self.name}: {hand.show(f'{self.name}: ')}; Value: {hand.value}")
            sleep(SLEEP_INT)
        return None

    def _apply_deviations(self) -> None:
        self.decision_tree['pair'][False]['ace'][False]['total'][16]['upcard'][9] = \
            lambda: 's' if self.dealer_ref.get_true_count() >= 5 else 'h'
        self.decision_tree['pair'][False]['ace'][False]['total'][16]['upcard'][10] = \
            lambda: 's' if self.dealer_ref.get_true_count() >= 0 else 'h'
        self.decision_tree['pair'][False]['ace'][False]['total'][15]['upcard'][10] = \
            lambda: 's' if self.dealer_ref.get_true_count() >= 4 else 'h'
        self.decision_tree['pair'][False]['ace'][False]['total'][13]['upcard'][2] = \
            lambda: 'h' if self.dealer_ref.get_true_count() < -1 else 's'
        self.decision_tree['pair'][False]['ace'][False]['total'][13]['upcard'][3] = \
            lambda: 'h' if self.dealer_ref.get_true_count() < -2 else 's'
        self.decision_tree['pair'][False]['ace'][False]['total'][12]['upcard'][2] = \
            lambda: 's' if self.dealer_ref.get_true_count() >= 4 else 'h'
        self.decision_tree['pair'][False]['ace'][False]['total'][12]['upcard'][3] = \
            lambda: 's' if self.dealer_ref.get_true_count() >= 2 else 'h'
        self.decision_tree['pair'][False]['ace'][False]['total'][12]['upcard'][4] = \
            lambda: 's' if self.dealer_ref.get_true_count() >= 0 else 's'
        self.decision_tree['pair'][False]['ace'][False]['total'][12]['upcard'][5] = \
            lambda: 'h' if self.dealer_ref.get_true_count() < -1 else 's'
        self.decision_tree['pair'][False]['ace'][False]['total'][12]['upcard'][6] = \
            lambda: 'h' if self.dealer_ref.get_true_count() < -1 else 's'
        self.decision_tree['pair'][False]['ace'][False]['total'][11]['upcard'][11] = \
            lambda: 'd' if self.dealer_ref.get_true_count() >= -1 else 'd'
        self.decision_tree['pair'][False]['ace'][False]['total'][10]['upcard'][10] = \
            lambda: 'd' if self.dealer_ref.get_true_count() >= 4 else 'h'
        self.decision_tree['pair'][False]['ace'][False]['total'][10]['upcard'][11] = \
            lambda: 'd' if self.dealer_ref.get_true_count() >= 4 else 'h'
        self.decision_tree['pair'][False]['ace'][False]['total'][9]['upcard'][2] = \
            lambda: 'd' if self.dealer_ref.get_true_count() >= 1 else 'h'
        self.decision_tree['pair'][False]['ace'][False]['total'][9]['upcard'][7] = \
            lambda: 'd' if self.dealer_ref.get_true_count() >= 4 else 'h'
        self.decision_tree['pair'][True]['ace'][False]['total'][20]['upcard'][5] = \
            lambda: 'y' if self.dealer_ref.get_true_count() >= 5 else 's'
        self.decision_tree['pair'][True]['ace'][False]['total'][20]['upcard'][6] = \
            lambda: 'y' if self.dealer_ref.get_true_count() >= 5 else 's'
        return None
