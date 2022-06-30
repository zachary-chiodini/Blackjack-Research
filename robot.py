from blackjack import Hand, Player


class BasicStrategy(Player):

    def __init__(self):
        super().__init__(0)
        self.name = 'Basic Strategy'
        # This decision tree was generated using the C4.5 Decision Tree Learning Algorithm.
        self.decision_tree = {
            'Pair': {
                '1': {'Total': {
                    '20': {'Up Card': {'5': {'s': None}, '7': {'s': None}, '9': {'s': None}, '4': {'s': None},
                                       '2': {'s': None}, '10': {'s': None}, '8': {'s': None}, '3': {'s': None},
                                       '11': {'s': None}, '6': {'s': None}}},
                    '18': {'Up Card': {'5': {'y': None}, '7': {'s': None}, '9': {'y': None}, '4': {'y': None},
                                       '2': {'y': None}, '10': {'s': None}, '8': {'y': None}, '3': {'y': None},
                                       '11': {'s': None}, '6': {'y': None}}},
                    '16': {'Up Card': {'5': {'y': None}, '7': {'y': None}, '9': {'y': None}, '3': {'y': None},
                                       '2': {'y': None}, '10': {'y': None}, '8': {'y': None}, '4': {'y': None},
                                       '11': {'y': None}, '6': {'y': None}}},
                    '14': {'Up Card': {'5': {'y': None}, '7': {'y': None}, '9': {'h': None}, '4': {'y': None},
                                       '2': {'y': None}, '10': {'h': None}, '3': {'y': None}, '8': {'h': None},
                                       '11': {'h': None}, '6': {'y': None}}},
                    '12': {
                        'Ace': {
                            '1': {'Up Card': {'5': {'y': None}, '7': {'y': None}, '9': {'y': None}, '4': {'y': None},
                                              '3': {'y': None}, '10': {'y': None}, '8': {'y': None}, '2': {'y': None},
                                              '11': {'y': None}, '6': {'y': None}}},
                            '0': {'Up Card': {'5': {'y': None}, '7': {'h': None}, '9': {'h': None}, '4': {'y': None},
                                              '3': {'y': None}, '2': {'yn': None}, '8': {'h': None}, '10': {'h': None},
                                              '11': {'h': None}, '6': {'y': None}}}}},
                    '10': {'Up Card': {'5': {'d': None}, '7': {'d': None}, '9': {'d': None}, '4': {'d': None},
                                       '3': {'d': None}, '10': {'d': None}, '8': {'d': None}, '2': {'d': None},
                                       '11': {'d': None}, '6': {'d': None}}},
                    '8': {'Up Card': {'5': {'yn': None}, '7': {'h': None}, '9': {'h': None}, '3': {'h': None},
                                      '2': {'h': None}, '4': {'h': None}, '10': {'h': None}, '8': {'h': None},
                                      '11': {'h': None}, '6': {'yn': None}}},
                    '6': {'Up Card': {'5': {'y': None}, '7': {'y': None}, '9': {'h': None}, '3': {'yn': None},
                                      '2': {'yn': None}, '10': {'h': None}, '4': {'y': None}, '8': {'h': None},
                                      '11': {'h': None}, '6': {'y': None}}},
                    '4': {'Up Card': {'5': {'y': None}, '7': {'y': None}, '9': {'h': None}, '4': {'y': None},
                                      '2': {'yn': None}, '10': {'h': None}, '8': {'h': None}, '3': {'yn': None},
                                      '11': {'h': None}, '6': {'y': None}}}}},
                '0': {'Total': {
                    '21': {'s': None},
                    '20': {'s': None},
                    '19': {'Up Card': {'5': {'s': None}, '7': {'s': None}, '9': {'s': None}, '3': {'s': None},
                                       '2': {'s': None}, '10': {'s': None}, '8': {'s': None}, '4': {'s': None},
                                       '11': {'s': None},
                                       '6': {'Ace': {'1': {'ds': None},
                                                     '0': {'s': None}}}}},
                    '18': {
                        'Ace': {
                            '1': {'Up Card': {'5': {'ds': None}, '7': {'s': None}, '9': {'h': None}, '4': {'ds': None},
                                              '2': {'ds': None}, '10': {'h': None}, '8': {'s': None}, '3': {'ds': None},
                                              '11': {'h': None}, '6': {'ds': None}}},
                            '0': {'s': None}}},
                    '17': {
                        'Ace': {
                            '1': {'Up Card': {'5': {'d': None}, '7': {'h': None}, '9': {'h': None}, '3': {'d': None},
                                              '4': {'d': None}, '2': {'h': None}, '10': {'h': None}, '8': {'h': None},
                                              '11': {'h': None}, '6': {'d': None}}},
                            '0': {'s': None}}},
                    '16': {
                        'Ace': {
                            '1': {'Up Card': {'5': {'d': None}, '7': {'h': None}, '9': {'h': None}, '3': {'h': None},
                                              '2': {'h': None}, '10': {'h': None}, '8': {'h': None}, '4': {'d': None},
                                              '11': {'h': None}, '6': {'d': None}}},
                            '0': {'Up Card': {'5': {'s': None}, '7': {'h': None}, '9': {'h': None}, '4': {'s': None},
                                              '3': {'s': None}, '10': {'h': None}, '8': {'h': None}, '2': {'s': None},
                                              '11': {'h': None}, '6': {'s': None}}}}},
                    '15': {
                        'Ace': {
                            '1': {'Up Card': {'5': {'d': None}, '7': {'h': None}, '9': {'h': None}, '4': {'d': None},
                                              '2': {'h': None}, '10': {'h': None}, '3': {'h': None}, '8': {'h': None},
                                              '11': {'h': None}, '6': {'d': None}}},
                            '0': {'Up Card': {'5': {'s': None}, '7': {'h': None}, '9': {'h': None}, '4': {'s': None},
                                              '2': {'s': None}, '10': {'h': None}, '8': {'h': None}, '3': {'s': None},
                                              '11': {'h': None}, '6': {'s': None}}}}},
                    '14': {
                        'Ace': {
                            '1': {'Up Card': {'5': {'d': None}, '7': {'h': None}, '9': {'h': None}, '3': {'h': None},
                                              '2': {'h': None}, '10': {'h': None}, '8': {'h': None}, '4': {'h': None},
                                              '11': {'h': None}, '6': {'d': None}}},
                            '0': {'Up Card': {'5': {'s': None}, '7': {'h': None}, '9': {'h': None}, '3': {'s': None},
                                              '2': {'s': None}, '10': {'h': None}, '8': {'h': None}, '4': {'s': None},
                                              '11': {'h': None}, '6': {'s': None}}}}},
                    '13': {
                        'Ace': {
                            '1': {'Up Card': {'5': {'d': None}, '7': {'h': None}, '9': {'h': None}, '3': {'h': None},
                                              '2': {'h': None}, '10': {'h': None}, '8': {'h': None}, '4': {'h': None},
                                              '11': {'h': None}, '6': {'d': None}}},
                            '0': {'Up Card': {'5': {'s': None}, '7': {'h': None}, '9': {'h': None}, '3': {'s': None},
                                              '2': {'s': None}, '10': {'h': None}, '8': {'h': None}, '4': {'s': None},
                                              '11': {'h': None}, '6': {'s': None}}}}},
                    '12': {'Up Card': {'5': {'s': None}, '7': {'h': None}, '9': {'h': None}, '3': {'h': None},
                                       '2': {'h': None}, '10': {'h': None}, '8': {'h': None}, '4': {'s': None},
                                       '11': {'h': None}, '6': {'s': None}}},
                    '11': {'Up Card': {'5': {'d': None}, '7': {'d': None}, '9': {'d': None}, '4': {'d': None},
                                       '2': {'d': None}, '10': {'d': None}, '8': {'d': None}, '3': {'d': None},
                                       '11': {'d': None}, '6': {'d': None}}},
                    '10': {'Up Card': {'5': {'d': None}, '7': {'d': None}, '9': {'d': None}, '3': {'d': None},
                                       '2': {'d': None}, '10': {'h': None}, '4': {'d': None}, '8': {'d': None},
                                       '11': {'h': None}, '6': {'d': None}}},
                    '9': {'Up Card': {'5': {'d': None}, '7': {'h': None}, '9': {'h': None}, '3': {'d': None},
                                      '4': {'d': None}, '10': {'h': None}, '8': {'h': None}, '2': {'h': None},
                                      '11': {'h': None}, '6': {'d': None}}},
                    '8': {'h': None},
                    '7': {'h': None},
                    '6': {'h': None},
                    '5': {'h': None},
                    '4': {'h': None}}}}}

    def call(self, hand: Hand) -> str:
        pass

    def place_bet(self, minimum_bet: int) -> bool:
        pass
