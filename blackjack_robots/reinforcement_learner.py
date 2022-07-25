from numpy import argmax, array, empty, vstack, max as npmax, min as npmin

from ai.neural_network import Input_Matrix, MultilayerPerceptron, NDArray, NeuralNetwork, Output_Matrix
from blackjack import Card, Hand, List, Player, randint, Table
from blackjack_robots.card_counter import BasicStrategy, sleep


Blackjack_State = NDArray[int]  # NDArray(Pair, Ace, Hand_Min, Hand_Max, Upcard, Insurance)


class ReinforcementLearner(BasicStrategy):

    def __init__(self, neural_network: NeuralNetwork):
        if not neural_network.instantiated:
            raise ValueError('The argument "neural_network" must be an instantiated "NeuralNetwork" class object.')
        super().__init__()
        self.name = 'Reinforcement Learner'
        self.policy = neural_network
        self.actions = ['h', 's', 'd', 'y', 'sur']
        self.policy.initialize(number_of_features=5, number_of_targets=6)
        self.total_reward = 0
        self.games_played: List[Input_Matrix] = []
        self.actions_played: List[Output_Matrix] = []
        self.rewards: List[int] = []
        self.state_path_matrix: Input_Matrix = empty(shape=(0, 5), dtype=int)
        self.action_path_matrix: Output_Matrix = empty(shape=(0, 6), dtype=int)

    def action_indices_of(self, state_matrix: Input_Matrix) -> NDArray[int]:
        prob_actions: Output_Matrix = self.policy.forward_propagation(state_matrix)
        return argmax(prob_actions, axis=1)

    def ask_for_insurance(self) -> None:
        hand = self.hands[0]
        up_card = Card('A', '', face_up=True)
        choice = self.decision(hand, up_card, insurance=1)
        if choice == 'h':
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
        return self.choices[choice](hand)

    def decision(self, hand: Hand, up_card: Card, insurance: int = 0) -> str:
        state: Blackjack_State = self.get_current_state(hand, up_card, insurance)
        self.state_path_matrix = vstack([self.state_path_matrix, array([state])])
        prob_actions: Output_Matrix = self.policy.forward_propagation(array([state]))
        self.action_path_matrix = vstack([self.action_path_matrix, prob_actions])
        index = argmax(prob_actions, axis=1).item()
        return self.actions[index]

    @staticmethod
    def get_current_state(hand: Hand, up_card: Card, insurance: int = 0) -> Blackjack_State:
        hand_min, hand_max = npmin(hand.value), npmax(hand.value)
        is_pair = int(hand.pair())
        has_ace = int(hand.has_ace())
        up_card_value = npmax(up_card.get_value())
        state = array([is_pair, has_ace, hand_min, hand_max, up_card_value, insurance])
        return state

    def lost(self, hand: Hand) -> None:
        self.total_reward -= hand.bet
        self.hands.remove(hand)
        self.show_score(hand, 'lost')
        self.insurance = 0
        self._your_turn = False
        self._reset()
        return None

    def push(self, hand: Hand) -> None:
        self.total_reward += hand.bet
        self.chips += hand.bet
        self.hands.remove(hand)
        self.show_score(hand, 'tied')
        self.insurance = 0
        self._your_turn = False
        self._reset()
        return None

    def surrender(self, hand: Hand) -> str:
        if len(hand.cards) == 2:
            self.total_reward += hand.bet // 2
            self.chips += hand.bet // 2
            self.hands.remove(hand)
            self.insurance = 0
            self._your_turn = False
            self._reset()
            return 'sur'
        self.stand()
        return 's'

    def use_insurance(self, hand: Hand) -> None:
        self.total_reward += self.insurance + hand.bet
        self.chips += self.insurance + hand.bet
        print(f"{self.name} insured hand {hand.show(f'{self.name} insured hand ')} for {self.insurance} chips.")
        print(f'You receive {hand.bet} chips insured with {self.insurance} chips insurance.')
        sleep(self.sleep_int)
        if self.hands:
            self.hands.remove(hand)
        self.insurance = 0
        self._your_turn = False
        self._reset()
        return None

    def won(self, hand: Hand) -> None:
        self.total_reward += 2 * hand.bet
        self.chips += 2 * hand.bet
        self.hands.remove(hand)
        self.show_score(hand, 'won')
        self.insurance = 0
        self._your_turn = False
        self._reset()
        return None

    def _reset(self) -> None:
        if not self.hands:
            self.games_played.append(self.state_path_matrix)
            self.actions_played.append(self.action_path_matrix)
            self.rewards.append(self.total_reward)
            print(self.state_path_matrix)
            print(self.action_path_matrix)
            print(self.rewards)
            self.state_path_matrix = empty(shape=(0, 5), dtype=int)
            self.action_path_matrix = empty(shape=(0, 5), dtype=int)
            self.total_reward = 0
        return None


if __name__ == '__main__':
    neural_network = MultilayerPerceptron(perceptrons_per_hidden_layer=[30])
    table = Table(players=2, decks=6, minimum_bet=50, penetration=0.75)
    table.players = [Player(1), ReinforcementLearner(neural_network)]
    table.play()
