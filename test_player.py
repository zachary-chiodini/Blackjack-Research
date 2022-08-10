from time import sleep

from numpy import hstack, inf, vstack

from ai.neural_network import NeuralNetwork, MultilayerPerceptron
from blackjack import Card, Hand, Table
from blackjack_robots.reinforcement_learner import Node, ReinforcementLearner


class TestPlayer(ReinforcementLearner):

    def __init__(self, neural_network: NeuralNetwork = MultilayerPerceptron([30])):
        super().__init__(neural_network)
        self.name = 'Test Player'
        self.nodes = []

    def ask_for_insurance(self) -> None:
        self.asked_insurance = True
        hand = self.hands[0]
        up_card = Card('A', '', face_up=True)
        choice = self.decision(hand, up_card, insurance=1)
        input_ = str(input(f'{self.name}; Chips: {self.chips}; Insurance? (y/n) '))
        price = hand.bet // 2
        if input_.lower().replace('es', '').strip() == 'y' or input_.strip() == '1':
            if self.chips >= price:
                self.chips -= price
                self.total_bet += price
                self.insurance = price
                return None
        return None

    def call(self, hand: Hand) -> str:
        up_card = self.dealer_ref.hand.cards[1]
        choice = self.decision(hand, up_card)
        input_ = str(input(f'Chips: {self.chips}; Bet: {self.total_bet}; Your turn: '))
        if input_ not in self.choices:
            print(f'You must choose {self.choices.keys()}.')
            sleep(self.sleep_int)
            return self.call(hand)
        return self.choices[input_](hand)

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
                self.episode_index = len(self.state_path_matrix)
                self.total_bet = bet
                self.hands.append(Hand(bet=bet))
                self.chips -= bet
                self.rounds += 1
                self._your_turn = True
                return True
        return False

    def _reset(self) -> None:

        def recurse(node: Node) -> None:
            # Leaf nodes are empty.
            if node.state.any():
                total_reward = node.calc_reward()
                self.state_path_matrix = vstack([self.state_path_matrix, node.state])
                self.action_path_matrix = vstack([self.action_path_matrix, node.action])
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
            print(self.state_path_matrix)
            print(self.action_path_matrix)
            print(self.reward_path_array)
            self.nodes.append(self.root_node)
            self.current_node = Node()
            self.root_node = self.current_node
        if self.split_queue:
            self.current_node = self.split_queue.pop(0)
        self._your_turn = False
        return None


if __name__ == '__main__':
    table = Table(players=1, decks=6, minimum_bet=50, penetration=0.75)
    player = TestPlayer()
    player.chips = inf
    table.players = [player]
    table.play()

    def recurse(node: Node, parent_i=0, child_j=1) -> None:
        print((parent_i, child_j), node.state, node.action, node.reward)
        parent_i = child_j
        child_j += 1
        for child in node.children:
            recurse(child, parent_i, child_j)
            child_j += 1
        return None

    for node_ in player.nodes:
        recurse(node_)
