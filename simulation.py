from blackjack import Table
from card_counter import CardCounter

if __name__ == '__main__':
    # Let's see if the card counter dies.
    card_counter = CardCounter()
    card_counter.chips = 10000
    table = Table(players=1, decks=6, minimum_bet=10, penetration=0.75)
    table.players = [card_counter]
    n_games = 20000
    table.play(condition=lambda: card_counter.rounds < n_games)
    if card_counter.rounds < n_games:
        print(f'Card Counter DIED with {card_counter.chips} chips after {card_counter.rounds} rounds '
              f'and {round(card_counter.rounds / 50, 2)} hours.')
    else:
        print(f'Card Counter SURVIVED with {card_counter.chips} after {card_counter.rounds} rounds '
              f'and {round(card_counter.rounds / 50, 2)} hours.')
