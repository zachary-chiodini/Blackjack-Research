from robots.basic_strategy import Player


class ReinforcementLearner(Player):

    def __init__(self):
        super().__init__(0)
        self.name = 'Reinforcement Learner'
