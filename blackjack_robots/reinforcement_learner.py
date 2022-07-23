from numpy import np

from ai.neural_network import Any, Float64, Input_Matrix, NDArray, NeuralNetwork, Output_Matrix
from blackjack import Hand, randint
from blackjack_robots.basic_strategy import Player, sleep


Pair, Ace, Hand_Min, Hand_Max, Upcard = int, int, int, int, int
Blackjack_State = NDArray[Pair, Ace, Hand_Min, Hand_Max, Upcard]
Number_of_Actions = Any
Probability_of_Action = Float64
PolicyOutput = NDArray[Number_of_Actions, Probability_of_Action]


class ReinforcementLearner(Player):

    def __init__(self, neural_network: NeuralNetwork):
        if not neural_network.instantiated:
            raise ValueError('The argument "neural_network" must be an instantiated "NeuralNetwork" class object.')
        super().__init__(0)
        self.name = 'Reinforcement Learner'
        self.policy = neural_network
        self.actions = ['h', 's', 'd', 'y', 'sur']
        self.policy.initialize(number_of_features=4, number_of_actions=len(self.actions))

    def action_indices_of(self, state_matrix: Input_Matrix) -> NDArray[int]:
        prob_actions: Output_Matrix = self.policy.forward_propagation(state_matrix)
        return np.argmax(prob_actions, axis=1)

    def decision(self, hand: Hand) -> str:
        state: Blackjack_State = self.get_current_state(hand)
        prob_actions: PolicyOutput = self.policy.forward_propagation(state)
        index = np.argmax(prob_actions, axis=1).item()
        action = self.actions[index]
        return self.choices[action]

    def get_current_state(self, hand: Hand) -> Blackjack_State:
        hand_min, hand_max = np.min(hand.value), np.max(hand.value)
        is_pair = int(hand.pair())
        has_ace = int(hand.has_ace())
        up_card = self.dealer_ref.face_up_card()
        up_card_value = np.max(up_card.get_value())
        return np.array([is_pair, has_ace, hand_min, hand_max, up_card_value])

    def ask_for_insurance(self, hand: Hand) -> None:
        state: Blackjack_State = self.get_current_state(hand)
        prob_actions: PolicyOutput = self.policy.forward_propagation(state)
        sum_1, sum_2 = prob_actions[0:2].sum(), prob_actions[1:3].sum()
        if sum_1 == sum_2:
            accept = randint(0, 1)
        elif sum_1 > sum_2:
            accept = 1
        else:
            accept = 0
        if accept:
            price = self.total_bet // 2
            if self.chips >= price:
                self.chips -= price
                self.total_bet += price
                self.insurance = price
                return None
        self.insurance = 0
        return None

    def call(self, hand: Hand) -> str:
        choice = self.decision(hand)
        if isinstance(choice, Callable):
            choice = choice()
        if choice == 'ds':
            if len(hand.cards) == 2:
                choice = 'd'
            else:
                choice = 's'
        return self.choices[choice](hand)

    def place_bet(self, minimum_bet: int) -> bool:
        bet = minimum_bet
        if bet <= self.chips:
            print(f'{self.name}; Chips: {self.chips}; Place bet: {bet}')
            sleep(self.sleep_int)
            self.total_bet = 0
            self.hands.append(Hand(bet=bet))
            self.total_bet += bet
            self.chips -= bet
            self.rounds += 1
            self._your_turn = True
            return True
        return False
