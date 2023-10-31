import tkinter as tk
from PIL import Image, ImageTk

class BlackjackGUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.card_images = {}
        self.suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.player_hand_frame = None
        self.dealer_hand_frame = None
        self.player_hand_labels = []
        self.dealer_hand_labels = []

        self.setup_main_screen()  # Call the function to set up the main screen
          # Use main_frame instead of game_screen
        self.game_screen = tk.Frame(self.root)  # Create game_screen frame

    def setup_main_screen(self):
        self.root.title("Blackjack")

        # Main screen
        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0)

        self.stack_label = self.create_label("Enter Stack:", self.main_frame, 0, 0)
        self.stack_entry = self.create_entry(self.main_frame, 0, 1)

        self.decks_label = self.create_label("Enter Number of Decks:", self.main_frame, 1, 0)
        self.decks_entry = self.create_entry(self.main_frame, 1, 1)

        self.start_button = self.create_button("Start Game", self.start_game_from_main, self.main_frame, 2, 0, 2)
       
    def setup_bet_screen(self):
        # Bet Screen
        self.main_frame.grid_forget()
        self.bet_screen = tk.Frame(self.root)

        bet_label = self.create_label("Enter intended bet:", self.bet_screen, 0, 0)
        bet_entry = self.create_entry(self.bet_screen, 0, 1)

        bet_error_label = self.create_label("", self.bet_screen, 1, 0, fg="red")
        current_stack_label_bet = self.create_label(f"Current Stack: {self.game.current_stack}", self.bet_screen, 2, 0, columnspan=2)

        def set_current_bet():
            bet = int(bet_entry.get())
            if self.game.validate_bet(bet):
                self.setup_game_screen()
            else:
                bet_error_label.config(text="Invalid bet. Please try again.", fg="red")
        
        play_button = self.create_button("Play", set_current_bet, self.bet_screen, 3, 0, 2)

        self.bet_screen.grid(row=0, column=0)


    def setup_game_screen(self):
        # Game screen
        self.bet_screen.grid_forget()
        self.game_screen = tk.Frame(self.root)
        
        # Labels
        self.player_score_label = self.create_label(f"Player Score: {self.game.player_score} ", self.game_screen, 0, 0)
        self.player_hand_label = self.create_label(f"Player Hand: {self.game.player_hand} ", self.game_screen, 1, 0)
        self.dealer_score_label = self.create_label(f"Dealer Score: {self.game.dealer_score} ", self.game_screen, 2, 0)
        self.dealer_hand_label = self.create_label(f"Dealer Hand: {self.game.dealer_hand} ", self.game_screen, 3, 0)
        self.current_bet_label = self.create_label(f"Current Bet: {self.game.current_bet} ", self.game_screen, 4, 0)
        self.current_stack_label = self.create_label(f"Current Stack: {self.game.current_stack} ", self.game_screen, 5, 0)
        self.double_down_label = self.create_label(f"Double Downs: {self.game.double_down_count}", self.game_screen, 6, 0)
        self.result_label = self.create_label("", self.game_screen, 7, 0)
        self.game_screen.grid(row=0, column=0)
        # Buttons
        button_frame = tk.Frame(self.game_screen)
        self.hit_button = self.create_button("Hit", self.hit, button_frame, 0, 0, padx=5, pady=10)
        self.stand_button = self.create_button("Stand", self.stand, button_frame, 0, 1, padx=5, pady=10)
        self.split_button = self.create_button("Split", self.split, button_frame, 0, 2, padx=5, pady=10)
        self.double_down_button = self.create_button("Double", self.double_down, button_frame, 0, 3, padx=5, pady=10)
        self.surrender_button = self.create_button("Surrender", self.surrender, button_frame, 0, 4, padx=5, pady=10)
        self.play_again_button = self.create_button("Play Again", self.play_again, button_frame, 0, 5, padx=5, pady=10, state=tk.DISABLED)
        button_frame.grid(row=8, column=0)

        # Player and dealer hands
        self.player_hand_frame = self.create_frame(self.game_screen)
        self.dealer_hand_frame = self.create_frame(self.game_screen)
        self.player_hand_frame.grid(row=11, column=0)
        self.dealer_hand_frame.grid(row=12, column=0)

        self.load_card_images()

        # Update player and dealer hands after dealing initial cards
        self.display_player_hand()
        self.display_initial_dealer_hand()

        self.display_labels()

        # Start the GUI event loop
        self.root.mainloop()

    def setup_post_game_screen(self):
        pass

    def create_label(self, text, parent, row=None, column=None, columnspan=1, fg="black"):
        label = tk.Label(parent, text=text, fg=fg)
        label.grid(row=row, column=column, columnspan=columnspan)
        return label

    def create_entry(self, parent, row, column):
        entry = tk.Entry(parent)
        entry.grid(row=row, column=column)
        return entry

    def create_button(self, text, command, parent, row, column, padx=0, pady=0, state=tk.NORMAL):
        button = tk.Button(parent, text=text, command=command, state=state)
        button.grid(row=row, column=column, padx=padx, pady=pady)
        return button

    def create_frame(self, parent):
        frame = tk.Frame(parent)
        frame.grid(row=0, column=0)
        return frame

    def load_card_images(self):
        for suit in self.suits:
            for rank in self.ranks:
                image_path = f"images/{rank}_{suit}.png"
                self.card_images[(rank, suit)] = Image.open(image_path)
        self.card_images['back'] = Image.open("images/card_back.png")

    def display_labels(self):
        self.player_score_label.grid(row=0, column=0)
        self.player_hand_label.grid(row=1, column=0)
        self.dealer_score_label.grid(row=2, column=0)
        self.dealer_hand_label.grid(row=3, column=0)
        self.current_bet_label.grid(row=4, column=0)
        self.current_stack_label.grid(row=5, column=0)
        self.double_down_label.grid(row=6, column=0)
        self.result_label.grid(row=7, column=0)


    def display_player_hand(self):
        for label in self.player_hand_labels:
            label.destroy()
        for i in range(len(self.game.player_hand)):
            for j, (rank, suit) in enumerate(self.game.player_hand[i]):
                card_image = ImageTk.PhotoImage(self.card_images[(rank, suit)])
                label = tk.Label(self.player_hand_frame, image=card_image)
                label.image = card_image
                label.grid(row=i, column=j, padx=5)
                self.player_hand_labels.append(label)

    def display_initial_dealer_hand(self):
        for label in self.dealer_hand_labels:
            label.destroy()

        first_card = self.game.dealer_hand[0]
        card_image = ImageTk.PhotoImage(self.card_images[first_card])
        label = tk.Label(self.dealer_hand_frame, image=card_image)
        label.image = card_image
        label.grid(row=0, column=0, padx=5)
        self.dealer_hand_labels.append(label)

        face_down_image = ImageTk.PhotoImage(self.card_images['back'])
        label = tk.Label(self.dealer_hand_frame, image=face_down_image)
        label.image = face_down_image
        label.grid(row=0, column=1, padx=5)
        self.dealer_hand_labels.append(label)

    def update_dealer_score_label(self):
        self.dealer_score_label.config(text=f"Dealer Score: {self.game.dealer_score}")

    def update_dealer_hand_label(self):
        self.dealer_hand_label.config(text=f"Dealer Hand: {self.game.dealer_hand}")

    def update_player_score_label(self):
        self.player_score_label.config(text=f"Player Score: {self.game.player_score}")
    
    def update_double_down_label(self):
        self.double_down_label.config(text=f"Double Downs: {self.game.double_down_count}")

    def update_player_hand_label(self):
        self.player_hand_label.config(text=f"Player Hand: {self.game.player_hand}")

    def update_current_bet_label(self):
        self.current_bet_label.config(text=f"Current Bet: {self.game.current_bet}")

    def update_current_stack_label(self):
        self.current_stack_label.config(text=f"Current Stack: {self.current_stack.get()}")

    def update_current_stack_label_bet(self):
        self.current_stack_label_bet.config(text=f"Current Stack: {self.current_stack.get()}")

    def update_result_label(self, label=None):
        if label is not None:
            self.result_label.config(text=f"{label}")
        else:
            self.result_label.config(text="")

    def start_game_from_main(self):
        self.game.current_stack = int(self.stack_entry.get())
        num_decks = int(self.decks_entry.get())
        self.game.start_game(num_decks)
        self.main_frame.grid_forget()  # Hide the main frame
        self.setup_bet_screen() 
        
    def hit(self):
        self.game.hit()
        self.post_action_updates()

    def split(self):
        if self.game.split():
            self.post_action_updates()
        else:
            self.update_result_label("Cannot split due to insufficient funds or unsplittable hand.")

    def double_down(self):
        if self.game.double_down():
            self.post_action_updates()
        else:
            self.update_result_label("Cannot double down due to insufficient funds.")

    def surrender(self):
        self.game.surrender()
        self.update_result_label("You surrendered!")

    def stand(self):
        self.game.stand()
        if self.game.current_player_hand == len(self.game.player_hand) - 1:
            self.hit_button.config(state=tk.DISABLED)
            self.stand_button.config(state=tk.DISABLED)

            def deal_next_card():
                if self.game.dealer_score < 17:
                    card = self.game.deck.deal_card()
                    self.game.dealer_score += card_values[card[0]]
                    self.game.dealer_hand.append(card)
                    self.update_dealer_score_label()
                    self.update_dealer_hand_label()
                    self.display_dealer_hand()
                    self.root.after(500, deal_next_card)
                else:
                    self.display_dealer_hand()
                    self.reveal_result()

            self.display_dealer_hand()
            self.root.after(500, deal_next_card)
        else:
            self.game.current_player_hand += 1
            self.update_result_label(f"Standing on hand {self.game.current_player_hand}")

    def post_action_updates(self):
        self.update_player_hand_label()
        self.update_player_score_label()
        self.update_double_down_label()
        self.display_player_hand()
        if self.game.check_game_over():
            self.edit_post_game_buttons()
            self.setup_post_game_screen()
            
    def play_again(self):
        self.game.play_again()
        self.update_result_label()
        self.game_screen.pack_forget()
        self.setup_bet_screen()

    def edit_post_game_buttons(self):
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.split_button.config(state=tk.DISABLED)
        self.double_down_button.config(state=tk.DISABLED)
        self.surrender_button.config(state=tk.DISABLED)
        self.play_again_button.config(state=tk.NORMAL)

    def display_dealer_hand(self):
        for label in self.dealer_hand_labels:
            label.destroy()
        for i, (rank, suit) in enumerate(self.game.dealer_hand):
            card_image = ImageTk.PhotoImage(self.card_images[(rank, suit)])
            label = tk.Label(self.dealer_hand_frame, image=card_image)
            label.image = card_image
            label.grid(row=0, column=i, padx=5)
            self.dealer_hand_labels.append(label)

    def display_player_hand(self):
        for label in self.player_hand_labels:
            label.destroy()
        for i in range(len(self.game.player_hand)):
            for j, (rank, suit) in enumerate(self.game.player_hand[i]):
                card_image = ImageTk.PhotoImage(self.card_images[(rank, suit)])
                label = tk.Label(self.player_hand_frame, image=card_image)
                label.image = card_image
                label.grid(row=i, column=j, padx=5)
                self.player_hand_labels.append(label)

    def display_initial_dealer_hand(self):
        for label in self.dealer_hand_labels:
            label.destroy()

        first_card = self.game.dealer_hand[0]
        card_image = ImageTk.PhotoImage(self.card_images[first_card])
        label = tk.Label(self.dealer_hand_frame, image=card_image)
        label.image = card_image
        label.grid(row=0, column=0, padx=5)
        self.dealer_hand_labels.append(label)

        face_down_image = ImageTk.PhotoImage(self.card_images['back'])
        label = tk.Label(self.dealer_hand_frame, image=face_down_image)
        label.image = face_down_image
        label.grid(row=0, column=1, padx=5)
        self.dealer_hand_labels.append(label)

