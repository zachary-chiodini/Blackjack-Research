from ai.neural_network import MultilayerPerceptron
from blackjack import Table
from blackjack_robots.reinforcement_learner import ReinforcementLearner

if __name__ == '__main__':
    neural_network = MultilayerPerceptron(perceptrons_per_hidden_layer=[30])
    player = ReinforcementLearner(neural_network)
    player.chips = 1000
    table = Table(players=1, decks=6, minimum_bet=25, penetration=0.75)
    table.sleep_int = 0
    table.players = [player]
    maximum_rounds = 1000
    total_rounds = 0
    while total_rounds > maximum_rounds:
        table.play(condition=lambda: player.rounds + total_rounds < maximum_rounds)
        total_rounds += player.rounds
