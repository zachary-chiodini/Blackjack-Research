from blackjack import Table
from card_counter import CardCounter

if __name__ == '__main__':
    # Let's see if the card counter dies.
    card_counter = CardCounter()
    table = Table(players=1, decks=6, minimum_bet=50, penetration=0.75)
    table.players = [card_counter]
    table.play(condition=lambda: card_counter.rounds < 1000)
    if card_counter.rounds < 1000:
        print(f'Card Counter DIED with {card_counter.chips} chips.')
    else:
        print(f'Card Counter SURVIVED with {card_counter.chips} chips.')
