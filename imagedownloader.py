import os

# Function to map suit abbreviations to full names
def get_full_suit_name(suit):
    suit_mapping = {
        'D': 'Diamonds', 'H': 'Hearts', 'S': 'Spades', 'C': 'Clubs'
    }
    return suit_mapping.get(suit, suit)

# Specify the folder path
folder_path = r"C:\Users\parke\OneDrive\Attachments\Documents\PROJECTS\blackjack\downloaded_images"

# List all files in the folder
files = os.listdir(folder_path)

# Iterate through the files
for file_name in files:
    if len(file_name) == 7:
        rank = file_name[0]
        suit = get_full_suit_name(file_name[1])
        new_file_name = f"{rank}_{suit}.png"
        os.rename(os.path.join(folder_path, file_name), os.path.join(folder_path, new_file_name))
        print(f"Renamed: {file_name} -> {new_file_name}")
    else:
        print(f"Invalid file name format: {file_name}")
