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
        self.deck = [(rank, suit) for suit in self.suits for rank in self.ranks]

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
            self.calculate_result()
            return True
        else:
            return False

    def setup_game_screen(self):
        self.current_bet[0] = int(self.bet_entry.get())
        if self.current_bet[0] > self.current_stack:
            self.bet_error_label.config(text="Error: Bet cannot be greater than current stack")
            return
        elif self.current_bet[0] <= 0:
            self.bet_error_label.config(text="Error: Bet cannot be less than or equal to 0")
            return
        self.current_stack -= self.current_bet[0]
        self.bet_screen.pack_forget()
        self.deal_initial_cards()
        self.update_labels()
        self.enable_buttons()
        self.display_player_hand()
        self.display_initial_dealer_hand()
        self.game_screen.pack()

    def deal_initial_cards(self):
        player_card_1 = ('8', 'Hearts')  # Set the first card to '8 of Hearts'
        player_card_2 = ('8', 'Diamonds')
        self.player_hand[0].append(player_card_1)
        self.player_hand[0].append(player_card_2)
        self.player_score[0] += self.card_values[player_card_1[0]] + self.card_values[player_card_2[0]]
        dealer_card_1 = self.deal_card()
        dealer_card_2 = self.deal_card()
        self.dealer_hand.append(dealer_card_1)
        self.dealer_hand.append(dealer_card_2)
        self.dealer_score += self.card_values[dealer_card_1[0]] + self.card_values[dealer_card_2[0]]


    def play_again(self):
        self.dealer_hand = []
        self.player_hand = [[]]
        self.player_score = [0]
        self.dealer_score = 0
        self.current_player_hand = 0
        self.update_result_label()
        self.game_screen.pack_forget()
        self.place_bet()

    def place_bet(self):
        self.update_current_stack_label_bet()
        self.bet_screen.pack()
    
    def validate_bet(self, bet):
        return bet > 0 and bet > self.current_stack
        

    def update_labels(self):
        self.update_player_score_label()
        self.update_dealer_score_label()
        self.update_current_bet_label()
        self.update_current_stack_label()
        self.update_current_stack_label_bet()
        self.update_dealer_hand_label()
        self.update_player_hand_label()
        self.display_dealer_hand()
        self.display_player_hand()

    def enable_buttons(self):
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)
        self.split_button.config(state=tk.NORMAL)
        self.double_down_button.config(state=tk.NORMAL)
        self.surrender_button.config(state=tk.NORMAL)
        self.play_again_button.config(state=tk.DISABLED)

    def edit_post_game_buttons(self):
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.split_button.config(state=tk.DISABLED)
        self.double_down_button.config(state=tk.DISABLED)
        self.surrender_button.config(state=tk.DISABLED)
        self.play_again_button.config(state=tk.NORMAL)

    def hit(self):
        card = self.deal_card()
        self.player_hand[self.current_player_hand].append(card)
        self.player_score[self.current_player_hand] += self.card_values[card[0]]
        if self.player_score[self.current_player_hand] > 21:
            if self.current_player_hand == len(self.player_hand) - 1:
                self.calculate_result()
                self.game_end_callback = True
            else:
                self.current_player_hand += 1
            self.current_stack -= self.current_bet[self.current_player_hand]

    def split(self):
        if self.current_stack < self.current_bet[0]:
            self.update_result_label("Insufficient funds to split.")
        else:
            if len(self.player_hand[self.current_player_hand]) == 2 and self.player_hand[self.current_player_hand][0][0] == self.player_hand[self.current_player_hand][1][0]:
                new_hand = [self.player_hand[self.current_player_hand].pop()]  # Create a new hand and move one card
                self.player_hand.append(new_hand)
                self.player_score[self.current_player_hand] -= self.card_values[new_hand[0][0]]  # Update scores
                self.player_score.append(self.card_values[new_hand[0][0]])
                self.current_bet.append(self.current_bet[self.current_player_hand])
                self.current_stack -= self.current_bet[0]
                self.update_player_hand_label()
                self.display_player_hand()
            else:
                self.update_result_label("Cannot split this hand.")

    def double_down(self):
        pass

    def surrender(self):
        pass

    def stand(self):
        if self.current_player_hand == len(self.player_hand) - 1:
            self.hit_button.config(state=tk.DISABLED) 
            self.stand_button.config(state=tk.DISABLED)  
            def deal_next_card():
                if self.dealer_score < 17:
                    card = self.deal_card()
                    self.dealer_score += self.card_values[card[0]]
                    self.dealer_hand.append(card)
                    self.update_dealer_score_label()
                    self.update_dealer_hand_label()
                    self.display_dealer_hand()
                    self.root.after(500, deal_next_card)  # Add a 1-second delay between card reveals
                else:
                    self.display_dealer_hand()
                    self.reveal_result()
            self.display_dealer_hand()
            self.root.after(500, deal_next_card)
        else:
            self.current_player_hand += 1
            self.update_result_label(f"Standing on hand {self.current_player_hand}")

    def calculate_result(self):
        if self.dealer_score > 21:
            for i, score in enumerate(self.player_score):
                if score > 21:
                    self.current_stack -= self.current_bet
                else:
                    self.current_stack += self.current_bet
        else:
            for i, score in enumerate(self.player_score):
                if score > 21:
                    self.current_stack -= self.current_bet
                elif score > self.dealer_score:
                    self.current_stack += self.current_bet
                elif score < self.dealer_score:
                    self.current_stack -= self.current_bet
        

    def deal_card(self):
        return self.deck.pop()


