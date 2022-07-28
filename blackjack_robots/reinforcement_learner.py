from numpy import argmax, array, empty, hstack, vstack, max as npmax, min as npmin

from ai.neural_network import Input_Matrix, MultilayerPerceptron, NDArray, NeuralNetwork, Output_Matrix
from blackjack import Card, Hand, Player, Table
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
        self.num_features = 6
        self.num_targets = len(self.actions)
        self.policy.initialize(self.num_features, self.num_targets)
        self.episode_index = 0
        self.state_path_matrix: Input_Matrix = empty(shape=(0, self.num_features), dtype=int)
        self.action_path_matrix: Output_Matrix = empty(shape=(0, self.num_targets), dtype=int)
        self.reward_path_array: NDArray[int] = empty(shape=(0,), dtype=int)

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

    def bust(self, hand: Hand) -> None:
        self.reward_path_array[-1] = -hand.bet
        self.total_reward -= hand.bet
        self.chips -= hand.bet
        self.hands.remove(hand)
        self.show_score(hand, 'lost')
        self.insurance = 0
        self._your_turn = False
        self._reset()
        return None

    def call(self, hand: Hand) -> str:
        up_card = self.dealer_ref.hand.cards[1]
        choice = self.decision(hand, up_card)
        return self.choices[choice](hand)

    def decision(self, hand: Hand, up_card: Card, insurance: int = 0) -> str:
        state: Blackjack_State = self.get_current_state(hand, up_card, insurance)
        self.state_path_matrix = vstack([self.state_path_matrix, state])
        prob_actions: Output_Matrix = self.policy.forward_propagation(array([state]))
        self.action_path_matrix = vstack([self.action_path_matrix, prob_actions])
        self.reward_path_array = hstack([self.reward_path_array, 0])
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
        if self.reward_path_array.size and self.reward_path_array[-len(self.hands)] == 0:
            self.reward_path_array[-len(self.hands)] = -hand.bet
        self.total_reward -= hand.bet
        self.chips -= hand.bet
        self.hands.remove(hand)
        self.show_score(hand, 'lost')
        self.insurance = 0
        self._your_turn = False
        self._reset()
        return None

    def place_bet(self, minimum_bet: int) -> bool:
        if self.chips >= minimum_bet:
            print(f'{self.name}; Chips: {self.chips}; Place bet: {minimum_bet}')
            sleep(self.sleep_int)
            self.episode_index = len(self.state_path_matrix)
            self.total_bet = minimum_bet
            self.total_reward = 0
            self.hands.append(Hand(bet=minimum_bet))
            self.chips -= minimum_bet
            self.rounds += 1
            self._your_turn = True
            return True
        return False

    def push(self, hand: Hand) -> None:
        if self.reward_path_array.size and self.reward_path_array[-len(self.hands)] == 0:
            self.reward_path_array[-len(self.hands)] = hand.bet
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
            self.reward_path_array[-len(self.hands)] = hand.bet // 2
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
        self.reward_path_array[-1] = self.insurance + hand.bet
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
        self.reward_path_array[-len(self.hands)] = 2 * hand.bet
        self.total_reward += 2 * hand.bet
        self.chips += 2 * hand.bet
        self.hands.remove(hand)
        self.show_score(hand, 'won')
        self.insurance = 0
        self._your_turn = False
        self._reset()
        return None

    def won_blackjack(self, hand: Hand) -> None:
        if self.reward_path_array.size and self.reward_path_array[-1] == 0:
            self.reward_path_array[-1] = int(hand.bet * 2.5)
        self.total_reward += int(hand.bet * 2.5)
        self.chips += int(hand.bet * 2.5)
        self.hands.remove(hand)
        self.show_score(hand, 'won', blackjack=True)
        self.insurance = 0
        self._your_turn = False
        self._reset()
        return None

    def _reset(self) -> None:
        if not self.hands:
            slice_ = self.reward_path_array[self.episode_index:]
            slice_[slice_ == 0] = self.total_reward
        return None


if __name__ == '__main__':
    neural_network = MultilayerPerceptron(perceptrons_per_hidden_layer=[30])
    table = Table(players=2, decks=6, minimum_bet=50, penetration=0.75)
    table.players = [Player(1), ReinforcementLearner(neural_network)]
    table.play()
