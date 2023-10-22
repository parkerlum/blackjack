import random

# Define card values


# Function to start a new game
def start_blackjack():
    # Shuffle the deck
    random.shuffle(deck)

    # Deal initial cards to player and dealer
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    return player_hand, dealer_hand

def calculate_value(hand):
    rank1, rank2 = hand[0][0], hand[1][0]
    value = card_values[rank1] + card_values[rank2]
    return value
# Example usage
def logic():

    player_hand, dealer_hand = start_blackjack()
    print(f'Player\'s hand: {player_hand}')
    print(f'Dealer\'s hand: {dealer_hand[0]}')
    player_value += calculate_value(player_hand)
    dealer_value += calculate_value(dealer_hand)
    print(player_value)
    print(player_value)
if __name__ == "__main__":
    card_values = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
    }

    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = [(rank, suit) for suit in suits for rank in ranks]
    player_value = 0
    dealer_value = 0
    logic()


