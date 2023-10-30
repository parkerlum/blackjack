import random
from card import Card

class Deck:
    def __init__(self, num_decks=1):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.cards = [Card(rank, suit) for suit in suits for rank in ranks] * num_decks
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)
