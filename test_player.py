from ai.neural_network import NeuralNetwork, MultilayerPerceptron
from blackjack_robots.reinforcement_learner import Card, Hand, ReinforcementLearner, sleep, Table


class TestPlayer(ReinforcementLearner):

    def __init__(self, neural_network: NeuralNetwork = MultilayerPerceptron([30])):
        super().__init__(neural_network)
        self.name = 'Test Player'

    def ask_for_insurance(self) -> None:
        hand = self.hands[0]
        up_card = Card('A', '', face_up=True)
        choice = self.decision(hand, up_card, insurance=1)
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

    def place_bet(self, minimum_bet: int) -> bool:
        def wrong_input_response() -> bool:
            print(f'Minimum bet is {minimum_bet} chips.')
            sleep(self.sleep_int)
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
                self.total_bet = bet
                self.total_reward = 0
                self.hands.append(Hand(bet=bet))
                self.chips -= bet
                self.rounds += 1
                self._your_turn = True
                return True
        return False

    def call(self, hand: Hand) -> str:
        up_card = self.dealer_ref.hand.cards[1]
        choice = self.decision(hand, up_card)
        input_ = str(input(f'Chips: {self.chips}; Bet: {self.total_bet}; Your turn: '))
        if input_ not in self.choices:
            print(f'You must choose {self.choices.keys()}.')
            sleep(self.sleep_int)
            return self.call(hand)
        return self.choices[input_](hand)

    def _reset(self) -> None:
        if not self.hands:
            slice_ = self.reward_path_array[self.episode_index:]
            slice_[slice_ == 0] = self.total_reward
            print(self.state_path_matrix)
            print(self.action_path_matrix)
            print(self.reward_path_array)
        return None


if __name__ == '__main__':
    table = Table(players=2, decks=6, minimum_bet=50, penetration=0.75)
    table.players = [TestPlayer()]
    table.play()
