from card_counter import CardCounter
from neural_network import MultilayerPerceptron


class OptimizeBetSpread(CardCounter):

    def __init__(self):
        super().__init__()
        self.name = 'AI'
        self.mlp = MultilayerPerceptron()
