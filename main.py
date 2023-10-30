from tkinter import Tk
from gui import BlackjackGUI
from game import BlackjackGame

if __name__ == "__main__":
    root = Tk()
    game = BlackjackGame()
    gui = BlackjackGUI(root, game)
    root.mainloop()
