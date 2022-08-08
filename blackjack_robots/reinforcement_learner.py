from time import sleep
from typing import Any, List, Optional

from numpy import argmax, array, empty, hstack, vstack, max as npmax, min as npmin, ndarray, zeros

from ai.neural_network import InputMatrix, MultilayerPerceptron, NeuralNetwork, OutputMatrix
from blackjack import Card, Hand, Player, Table
from blackjack_robots.basic_strategy import BasicStrategy


State = ndarray[6, int]  # NDArray(Pair, Ace, Hand_Min, Hand_Max, Upcard, Insurance)
Action = ndarray[5, float]  # NDArray(prob h, prob s, prob d, prob y, prob sur)


class Node:

    def __init__(self, state: State = zeros(shape=(6,), dtype=int),
                 action: Action = zeros(shape=(5,), dtype=int),
                 reward: int = 0,
                 parent: Optional['Node'] = None,
                 children: Optional[List['Node']] = None):
        self.state = state
        self.action = action
        self.reward = reward
        self.parent = parent
        if children:
            self.children = children
        else:
            self.children = []

    def calc_reward(self) -> int:
        """
        The reward given to a state-action pair before a split
        should be a sum of all rewards after the split.

        For a node n with reward r:
            the calculated reward r' is given by
            r'(n) = sum(ri) from i = n (node number) to i = c (number of children)
        """
        rewards = []

        # This is a depth first search for rewards.
        def recurse(node: 'Node') -> None:
            rewards.append(node.reward)
            for child in node.children:
                recurse(child)
            return None

        recurse(self)
        return sum(rewards)

    def get_root_node(self) -> 'Node':
        node = self
        while node.parent:
            node = node.parent
        return node


class ReinforcementLearner(BasicStrategy):

    def __init__(self, neural_network: NeuralNetwork):
        if not neural_network.instantiated:
            raise ValueError('The argument "neural_network" must be an instantiated "NeuralNetwork" class object.')
        super().__init__()
        self.asked_insurance = False
        self.name = 'Reinforcement Learner'
        self.policy = neural_network
        self.actions = ['h', 's', 'd', 'y', 'sur']
        self.num_features = 6
        self.num_targets = len(self.actions)
        self.policy.initialize(self.num_features, self.num_targets)
        self.episode_index = 0
        self.current_node = Node()
        self.root_node = self.current_node
        self.split_queue: List[Node] = []  # This is a FIFO queue.
        self.reward_queue: List[Node] = []  # This is a FIFO queue.
        self.state_path_matrix: InputMatrix = empty(shape=(0, self.num_features), dtype=int)
        self.action_path_matrix: OutputMatrix = empty(shape=(0, self.num_targets), dtype=float)
        self.reward_path_array: ndarray[Any, int] = empty(shape=(0,), dtype=int)

    def action_indices_of(self, state_matrix: InputMatrix) -> ndarray[Any, int]:
        prob_actions: OutputMatrix = self.policy.forward_propagation(state_matrix)
        return argmax(prob_actions, axis=1)

    def ask_for_insurance(self) -> None:
        self.asked_insurance = True
        hand = self.hands[0]
        up_card = Card('A', '', face_up=True)
        choice = self.decision(hand, up_card, insurance=1)
        price = hand.bet // 2
        if choice == 'h':
            if self.chips >= price:
                self.chips -= price
                self.total_bet += price
                self.insurance = price
                return None
        return None

    def bust(self, hand: Hand) -> None:
        self.current_node.reward = -hand.bet
        self.hands.remove(hand)
        self.show_score(hand, 'lost')
        self._reset()
        return None

    def call(self, hand: Hand) -> str:
        up_card = self.dealer_ref.hand.cards[1]
        choice = self.decision(hand, up_card)
        return self.choices[choice](hand)

    def decision(self, hand: Hand, up_card: Card, insurance: int = 0) -> str:
        state: State = self.get_current_state(hand, up_card, insurance)
        action: Action = self.policy.forward_propagation(array([state]))
        self.state_path_matrix = vstack([self.state_path_matrix, state])
        self.action_path_matrix = vstack([self.action_path_matrix, action])
        self.current_node.state, self.current_node.action = state, action.flatten()
        child = Node(parent=self.current_node)
        self.current_node.children.append(child)
        self.current_node = child
        action_index = argmax(action, axis=1).item()
        return self.actions[action_index]

    def double(self, hand: Hand) -> str:
        if len(hand.cards) == 2:
            if self.chips >= hand.bet:
                self.reward_queue.append(self.current_node)
                self.chips -= hand.bet
                self.total_bet += hand.bet
                hand.bet += hand.bet
                self._reset()
                return 'd'
        return 'h'

    @staticmethod
    def get_current_state(hand: Hand, up_card: Card, insurance: int = 0) -> State:
        hand_min, hand_max = npmin(hand.value), npmax(hand.value)
        is_pair = int(hand.pair())
        has_ace = int(hand.has_ace())
        up_card_max = npmax(up_card.get_value())
        state = array([is_pair, has_ace, hand_min, hand_max, up_card_max, insurance])
        return state

    def lost(self, hand: Hand) -> None:
        if self.reward_queue:
            node = self.reward_queue.pop(0)
            node.reward = -hand.bet
        else:
            self.current_node.reward = -hand.bet
        self.hands.remove(hand)
        self.show_score(hand, 'lost')
        self._reset()
        return None

    def place_bet(self, minimum_bet: int) -> bool:
        if self.chips >= minimum_bet:
            print(f'{self.name}; Chips: {self.chips}; Place bet: {minimum_bet}')
            sleep(self.sleep_int)
            self.episode_index = len(self.state_path_matrix)
            self.total_bet = minimum_bet
            self.hands.append(Hand(bet=minimum_bet))
            self.chips -= minimum_bet
            self.rounds += 1
            self._your_turn = True
            return True
        return False

    def push(self, hand: Hand) -> None:
        if self.reward_queue:
            node = self.reward_queue.pop(0)
            node.reward = hand.bet
        else:
            self.current_node.reward = hand.bet
        self.chips += hand.bet
        self.hands.remove(hand)
        self.show_score(hand, 'tied')
        self._reset()
        return None

    def split(self, hand: Hand) -> str:
        if self.chips >= hand.bet and hand.pair():
            split_node = self.current_node.parent
            child1, child2 = Node(parent=split_node), Node(parent=split_node)
            split_node.children = [child1, child2]
            self.split_queue.extend([child1, child2])
            self.chips -= hand.bet
            self.total_bet += hand.bet
            self._reset()
            return 'y'
        self.stand()
        return 's'

    def stand(self, *args) -> str:
        self.reward_queue.append(self.current_node)
        self._reset()
        return 's'

    def surrender(self, hand: Hand) -> str:
        if len(hand.cards) == 2:
            self.current_node.reward = hand.bet // 2
            self.chips += hand.bet // 2
            self.hands.remove(hand)
            self._reset()
            return 'sur'
        self.stand()
        return 's'

    def use_insurance(self, hand: Hand) -> None:
        # If insurance is bought and used,
        # the root node has a reward of bet + insurance = +75.
        self.root_node.reward = self.insurance + hand.bet
        self.chips += self.insurance + hand.bet
        print(f"{self.name} insured hand {hand.show(f'{self.name} insured hand ')} for {self.insurance} chips.")
        print(f'You receive {hand.bet} chips insured with {self.insurance} chips insurance.')
        sleep(self.sleep_int)
        if self.hands:
            self.hands.remove(hand)
        self.insurance = 0
        self._reset()
        return None

    def won(self, hand: Hand) -> None:
        if self.reward_queue:
            node = self.reward_queue.pop(0)
            node.reward = 2 * hand.bet
        else:
            self.current_node.reward = 2 * hand.bet
        self.chips += 2 * hand.bet
        self.hands.remove(hand)
        self.show_score(hand, 'won')
        self._reset()
        return None

    def won_blackjack(self, hand: Hand) -> None:
        self.current_node.reward = int(hand.bet * 2.5)
        self.chips += int(hand.bet * 2.5)
        self.hands.remove(hand)
        self.show_score(hand, 'won', blackjack=True)
        self._reset()
        return None

    def _reset(self) -> None:

        def recurse(node: Node) -> None:
            # Leaf nodes are empty.
            if node.state.any():
                total_reward = node.calc_reward()
                self.reward_path_array = hstack([self.reward_path_array, total_reward])
            for child in node.children:
                recurse(child)
            return None

        if not self.hands:
            if self.root_node.state.any():
                if self.asked_insurance:
                    # If insurance is bought and not used,
                    # the root node has a reward of -insurance = -25.
                    if self.insurance:
                        self.root_node.reward = -self.insurance - self.root_node.calc_reward()
                        self.insurance = 0
                    # If insurance is not bought and dealer does not have blackjack,
                    # the root node has a reward of +insurance = +25.
                    elif self.root_node.children[0].state.any():
                        self.root_node.reward = 25 - self.root_node.calc_reward()
                    self.asked_insurance = False
                recurse(self.root_node)
            self.current_node = Node()
            self.root_node = self.current_node
        if self.split_queue:
            self.current_node = self.split_queue.pop(0)
        self._your_turn = False
        return None


if __name__ == '__main__':
    neural_network = MultilayerPerceptron(perceptrons_per_hidden_layer=[30])
    table = Table(players=2, decks=6, minimum_bet=50, penetration=0.75)
    table.players = [Player(1), ReinforcementLearner(neural_network)]
    table.play()
