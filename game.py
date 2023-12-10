import random

class BlackjackGame:
    def __init__(self):
        self.suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.card_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}
        self.player_hand = [[]]
        self.dealer_hand = []
        self.player_score = [0]
        self.dealer_score = 0
        self.current_bet = 0
        self.current_stack = 0
        self.current_player_hand = 0
        self.double_down_count = [0]
        self.game_end_callback = False
        self.num_aces = [0]
        self.deck = [(rank, suit) for suit in self.suits for rank in self.ranks]
        self.weight = 0

    def start_game(self, numDecks):
        self.player_hand = [[]]
        self.player_score = [0]
        self.dealer_hand = []
        self.dealer_score = 0
        self.deck *= numDecks
        random.shuffle(self.deck)
        self.deal_initial_cards()
    
    def check_game_over(self):
        if self.current_player_hand >= len(self.player_hand):
            self.dealer_showdown()
            self.calculate_result()
            return True
        else:
            return False

    def deal_initial_cards(self):
        self.hit()
        self.hit()
        dealer_card_1 = self.deal_card()
        dealer_card_2 = self.deal_card()
        self.calculate_weight(dealer_card_1[0])
        self.dealer_hand.append(dealer_card_1)
        self.dealer_hand.append(dealer_card_2)
        self.dealer_score += self.card_values[dealer_card_1[0]] + self.card_values[dealer_card_2[0]]

    def play_again(self):
        self.dealer_hand = []
        self.player_hand = [[]]
        self.player_score = [0]
        self.dealer_score = 0
        self.current_player_hand = 0
        self.double_down_count = [0]
        self.deal_initial_cards() 
    
    def validate_bet(self, bet):
        if bet > 0 and bet <= self.current_stack:
            self.current_bet = bet
            self.current_stack -= bet
            return True
        return False

    def hit(self):
        card = self.deal_card()
        self.calculate_weight(card[0])
        self.player_hand[self.current_player_hand].append(card)
        self.player_score[self.current_player_hand] += self.card_values[card[0]]

        if self.player_score[self.current_player_hand] > 21:
            if self.has_ace():
                if self.bust_with_aces():
                    self.double_down_count.append(0)
                    self.current_player_hand += 1
            else:
                self.double_down_count.append(0)
                self.current_player_hand += 1
    
    def has_ace(self):
        for card in self.player_hand[self.current_player_hand]:
            if card[0] == 'A':
                return True
        return False

    def adjust_for_aces(self):
        aces = self.player_hand[self.current_player_hand].count(('A', 'Hearts')) + self.player_hand[self.current_player_hand].count(('A', 'Diamonds')) + self.player_hand[self.current_player_hand].count(('A', 'Clubs')) + self.player_hand[self.current_player_hand].count(('A', 'Spades'))
        score = sum(self.card_values[card[0]] for card in self.player_hand[self.current_player_hand])
        while aces > 0 and score > 21:
            score -= 10
            aces -= 1
        return score 
        
    def bust_with_aces(self):
        if self.adjust_for_aces() > 21 and self.has_ace():
            return True
        return False

    def split(self):
        if self.current_stack < self.current_bet:
            return False
        else:
            if len(self.player_hand[self.current_player_hand]) == 2 and self.player_hand[self.current_player_hand][0][0] == self.player_hand[self.current_player_hand][1][0]:
                new_hand = [self.player_hand[self.current_player_hand].pop()]  # Create a new hand and move one card
                self.player_hand.append(new_hand)
                self.player_score[self.current_player_hand] -= self.card_values[new_hand[0][0]]  # Update scores
                self.player_score.append(self.card_values[new_hand[0][0]])
                self.double_down_count.append(0)
                self.current_stack -= self.current_bet
                return True
            return False

    def double_down(self):
        if self.current_stack >= self.current_bet:
            self.current_stack -= self.current_bet
            self.double_down_count[self.current_player_hand] = 1
            card = self.deal_card()
            self.calculate_weight(card[0])
            self.player_hand[self.current_player_hand].append(card)
            self.player_score[self.current_player_hand] += self.card_values[card[0]]
            if self.player_score[self.current_player_hand] > 21 and self.has_ace():
                if self.has_ace():
                    self.adjust_for_aces()
                else:
                    self.double_down_count.append(0)
                    self.current_player_hand += 1
            self.current_player_hand += 1
            return True
        return False

    def surrender(self):
        self.player_hand.pop(self.current_player_hand)
        self.double_down_count.pop(self.current_player_hand)
        self.player_score.pop(self.current_player_hand)
        self.current_stack += (self.current_bet / 2)

    def stand(self):
        self.current_player_hand += 1

    def dealer_showdown(self):
        self.calculate_weight(self.dealer_hand[1][0])
        while self.dealer_score < 17:
            card = self.deal_card()
            self.calculate_weight(card[0])
            self.dealer_hand.append(card)
            self.dealer_score += self.card_values[card[0]]

    def calculate_result(self):
        if self.dealer_score > 21:
            self.handle_dealer_busted()
        else:
            self.handle_dealer_not_busted()
    
    def handle_dealer_busted(self):
        for i in range(len(self.player_score)):
            if self.player_score[i] <= 21 and self.double_down_count[i]:
                self.current_stack += 4 * self.current_bet
            elif self.player_score[i] <= 21:
                self.current_stack += 2* self.current_bet

    def handle_dealer_not_busted(self):
        for i in range(len(self.player_score)):
            if self.player_score[i] > self.dealer_score and self.double_down_count[i]:
                self.current_stack += 4 * self.current_bet
            elif self.player_score[i] <= 21:
                self.current_stack += self.current_bet

    def deal_card(self):
        return self.deck.pop()

    def calculate_weight(self, card):
        if card == "2" or card == "3" or card == "4" or card == "5" or card == "6":
            self.weight += 1
        elif card == "10" or card == "J" or card == "Q" or card == "K" or card == "A":
            self.weight -= 1



