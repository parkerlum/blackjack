import tkinter as tk
import random
from PIL import Image, ImageTk

card_values = {
'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
'J': 10, 'Q': 10, 'K': 10, 'A': 11
}
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
player_hand_frame = None
dealer_hand_frame = None
player_hand = []
dealer_hand = []
player_score = 0
dealer_score = 0
current_bet = 0
current_stack = 0

def start_game():
    global player_score, dealer_score, stack, num_decks, deck, player_hand, dealer_hand
    player_hand = []
    player_score = 0
    dealer_hand = []
    dealer_score = 0
    deck = [(rank, suit) for suit in suits for rank in ranks] * num_decks
    random.shuffle(deck)
    player_score_label.config(text=f"Player Score: {player_score}")
    dealer_score_label.config(text=f"Dealer Score: {dealer_score}")
    main_frame.pack_forget()  # Hide main screen
    place_bet()
    

def setup_game_screen():
    global current_bet, current_stack
    current_bet = int(bet_entry.get())
    if current_bet > current_stack:
        bet_error_label.config(text="Error: Bet cannot be greater than current stack")
        return
    elif current_bet <= 0:
        bet_error_label.config(text="Error: Bet cannot be less than or equal to 0")
        return
    bet_screen.pack_forget() 
    deal_initial_cards()
    update_labels()
    enable_buttons()
    display_player_hand()
    display_initial_dealer_hand()
    game_screen.pack()
    
def deal_initial_cards():
    global deck, player_hand, player_score, dealer_hand, dealer_score
    player_card_1 = deal_card()
    player_card_2 = deal_card()
    player_hand.append(player_card_1)
    player_hand.append(player_card_2)
    player_score += card_values[player_card_1[0]] + card_values[player_card_2[0]]
    dealer_card_1 = deal_card()
    dealer_card_2 = deal_card()
    dealer_hand.append(dealer_card_1)
    dealer_hand.append(dealer_card_2)
    dealer_score += card_values[dealer_card_1[0]] + card_values[dealer_card_2[0]]

def play_again():
    global player_score, dealer_score, player_hand, dealer_hand
    dealer_hand = []
    player_hand = []
    player_score = 0
    dealer_score = 0
    update_result_label()
    game_screen.pack_forget()
    place_bet()

def place_bet():
    update_current_stack_label_bet()
    bet_screen.pack()

def update_labels():
    update_player_score_label()
    update_dealer_score_label()
    update_current_bet_label()
    update_current_stack_label()
    update_current_stack_label_bet()
    update_dealer_hand_label()
    update_player_hand_label()
    display_dealer_hand()
    display_player_hand()


def enable_buttons():
    hit_button.config(state=tk.NORMAL)
    stand_button.config(state=tk.NORMAL)
    split_button.config(state=tk.NORMAL)
    double_down_button.config(state=tk.NORMAL)
    surrender_button.config(state=tk.NORMAL)
    play_again_button.config(state=tk.DISABLED)

def edit_post_game_buttons():
    hit_button.config(state=tk.DISABLED)
    stand_button.config(state=tk.DISABLED)
    split_button.config(state=tk.DISABLED)
    double_down_button.config(state=tk.DISABLED)
    surrender_button.config(state=tk.DISABLED)
    play_again_button.config(state=tk.NORMAL)

def hit():
    global player_score, card_values, player_hand
    card = deal_card()
    player_hand.append(card)
    player_score += card_values[card[0]]
    update_player_hand_label()
    update_player_score_label()
    display_player_hand()
    if player_score > 21:
        global current_stack
        update_result_label("Player Bust! Dealer Wins.")
        edit_post_game_buttons()
        current_stack -= current_bet
def split():
    pass
def double_down():
    pass
def surrender():
    pass
def stand():
    global dealer_score, dealer_hand
    hit_button.config(state=tk.DISABLED) 
    stand_button.config(state=tk.DISABLED)  
    def deal_next_card():
        global dealer_score
        if dealer_score < 17:
            card = deal_card()
            dealer_score += card_values[card[0]]
            dealer_hand.append(card)
            update_dealer_score_label()
            update_dealer_hand_label()
            display_dealer_hand()
            root.after(500, deal_next_card)  # Add a 1-second delay between card reveals
        else:
            display_dealer_hand()
            reveal_result()
    display_dealer_hand()
    root.after(500, deal_next_card)

def reveal_result():
    global current_bet, current_stack
    if dealer_score > 21 or dealer_score < player_score:
        edit_post_game_buttons()
        current_stack += current_bet
        update_result_label("Player Wins!")
    elif dealer_score == player_score:
        edit_post_game_buttons()
        update_result_label("It's a Tie!")
    else:
        edit_post_game_buttons()
        current_stack -= current_bet
        update_result_label("Dealer Wins.")

def deal_card():
    return deck.pop()

def start_game_from_main():
    global current_stack, num_decks
    current_stack = int(stack_entry.get())
    num_decks = int(decks_entry.get())
    start_game()

def display_player_hand():
    for label in player_hand_labels:
        label.destroy()  # Destroy existing labels

    for i, (rank, suit) in enumerate(player_hand):
        card_image = ImageTk.PhotoImage(card_images[(rank, suit)])
        label = tk.Label(player_hand_frame, image=card_image)
        label.image = card_image
        label.grid(row=0, column=i, padx=5)  # Use grid layout
        player_hand_labels.append(label)

def display_dealer_hand():
    for label in dealer_hand_labels:
        label.destroy()  # Destroy existing labels
    for i, (rank, suit) in enumerate(dealer_hand):
        card_image = ImageTk.PhotoImage(card_images[(rank, suit)])
        label = tk.Label(dealer_hand_frame, image=card_image)
        label.image = card_image
        label.grid(row=0, column=i, padx=5)  # Use grid layout
        dealer_hand_labels.append(label)

def display_initial_dealer_hand():
    for label in dealer_hand_labels:
        label.destroy()  

    first_card = dealer_hand[0]
    card_image = ImageTk.PhotoImage(card_images[first_card])
    label = tk.Label(dealer_hand_frame, image=card_image)
    label.image = card_image
    label.grid(row=0, column=0, padx=5)  # Use grid layout
    dealer_hand_labels.append(label)

    face_down_image = ImageTk.PhotoImage(card_images['back'])  # Assuming you have an image for the face-down card
    label = tk.Label(dealer_hand_frame, image=face_down_image)
    label.image = face_down_image
    label.grid(row=0, column=1, padx=5)  # Use grid layout
    dealer_hand_labels.append(label)

def update_dealer_score_label():
    dealer_score_label.config(text=f"Dealer Score: {dealer_score}")

def update_dealer_hand_label():
    dealer_hand_label.config(text=f"Dealer Hand: {dealer_hand}")

def update_player_score_label():
    player_score_label.config(text=f"Player Score: {player_score}")

def update_player_hand_label():
    player_hand_label.config(text=f"Player Score: {player_hand}")

def update_current_bet_label():
    current_bet_label.config(text=f"Current Bet: {current_bet}")

def update_current_stack_label():
    current_stack_label.config(text=f"Current Stack: {current_stack}")

def update_current_stack_label_bet():
    current_stack_label_bet.config(text=f"Current Stack: {current_stack}")

def update_result_label(label=None):
    if label is not None:
        result_label.config(text=f"{label}")
    else:
        result_label.config(text="")
    
# Create the main window
root = tk.Tk()
root.title("Blackjack")

# Main screen
main_frame = tk.Frame(root)
main_frame.pack()

stack_label = tk.Label(main_frame, text="Enter Stack:")
stack_label.grid(row=0, column=0)

stack_entry = tk.Entry(main_frame)
stack_entry.grid(row=0, column=1)

decks_label = tk.Label(main_frame, text="Enter Number of Decks:")
decks_label.grid(row=1, column=0)

decks_entry = tk.Entry(main_frame)
decks_entry.grid(row=1, column=1)

start_button = tk.Button(main_frame, text="Start Game", command=start_game_from_main)
start_button.grid(row=2, columnspan=2)

# Bet Screen
bet_screen = tk.Frame(root)

bet_label = tk.Label(bet_screen, text="Enter intended bet:")
bet_label.grid(row=0, column=0)

bet_entry = tk.Entry(bet_screen)
bet_entry.grid(row=0, column=1)

bet_error_label = tk.Label(bet_screen, text="", fg="red")
bet_error_label.grid(row=1, column=0, columnspan=2)

current_stack_label_bet = tk.Label(bet_screen, text=f"Current Stack: {current_stack}")
current_stack_label_bet.grid(row=2, columnspan=2)  

play_button = tk.Button(bet_screen, text="Play", command=setup_game_screen)
play_button.grid(row=3, columnspan=2)

# Game screen
game_screen = tk.Frame(root)

player_score_label = tk.Label(game_screen, text=f"Player Score: {player_score}")
player_score_label.pack()

player_hand_label = tk.Label(game_screen, text=f"Player Hand: {player_hand}")
player_hand_label.pack()

dealer_score_label = tk.Label(game_screen, text=f"Dealer Score: {dealer_score}")
dealer_score_label.pack()

dealer_hand_label = tk.Label(game_screen, text=f"Dealer Hand: {dealer_hand}")
dealer_hand_label.pack()

current_bet_label = tk.Label(game_screen, text=f"Current Bet: {current_bet}")
current_bet_label.pack()

current_stack_label = tk.Label(game_screen, text=f"Current Stack: {current_stack}")
current_stack_label.pack()

result_label = tk.Label(game_screen, text="")
result_label.pack()

hit_button = tk.Button(game_screen, text="Hit", command=hit)
hit_button.pack(side=tk.LEFT)

stand_button = tk.Button(game_screen, text="Stand", command=stand)
stand_button.pack(side=tk.LEFT)

split_button = tk.Button(game_screen, text="Split", command=split)
split_button.pack(side=tk.LEFT)

double_down_button = tk.Button(game_screen, text="Double")
double_down_button.pack(side=tk.LEFT)

surrender_button = tk.Button(game_screen, text="Surrender")
surrender_button.pack(side=tk.LEFT)

play_again_button = tk.Button(game_screen, text="Play Again", command=play_again, state=tk.DISABLED)
play_again_button.pack()

card_images = {}
for suit in suits:
    for rank in ranks:
        image_path = f"images/{rank}_{suit}.png"
        card_images[(rank, suit)] = Image.open(image_path)
card_images['back'] = Image.open("images/card_back.png")


# Create labels to display card images
player_hand_labels = []
for i in range(5):  # Create enough labels for up to 5 cards
    label = tk.Label(game_screen, image=None)  # Placeholder image
    label.pack(side=tk.LEFT)  # Pack labels side by side
    player_hand_labels.append(label)

dealer_hand_labels = []
for i in range(5):
    label = tk.Label(game_screen, image=None)  # Placeholder image
    label.pack()
    dealer_hand_labels.append(label)

player_hand_frame = tk.Frame(game_screen)
player_hand_frame.pack()

dealer_hand_frame = tk.Frame(game_screen)
dealer_hand_frame.pack()

# Update player and dealer hands after dealing initial cards
display_player_hand()
display_dealer_hand()

# Start the GUI event loop
root.mainloop()

