from blackjack import Player, Table


class Robot(Player):

    def __init__(self, n: int):
        super().__init__(n)


if __name__ == '__main__':
    table = Table(players=1, decks=6, minimum_bet=50, penetration=0.75)
    table.players = [Robot(1)]
    table.play()
