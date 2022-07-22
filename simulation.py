from blackjack import Table
from robots.card_counter import CardCounter

if __name__ == '__main__':
    # Let's see if the card counter dies.
    card_counter = CardCounter()
    card_counter.chips = 1000
    table = Table(players=1, decks=6, minimum_bet=25, penetration=0.75)
    table.sleep_int = 0
    table.players = [card_counter]
    n_games = 1000
    table.play(condition=lambda: card_counter.rounds < n_games)
    if card_counter.rounds < n_games:
        print(f'Card Counter DIED with {card_counter.chips} chips after {card_counter.rounds} rounds '
              f'and {round(card_counter.rounds / 50, 2)} hours.')
    else:
        print(f'Card Counter SURVIVED with {card_counter.chips} after {card_counter.rounds} rounds '
              f'and {round(card_counter.rounds / 50, 2)} hours.')
