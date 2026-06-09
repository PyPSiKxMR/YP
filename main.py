# main.py
import tkinter as tk
from menu import MainMenu
from game import GameScreen
from win_screen import WinScreen

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Сканворды")
        self.root.geometry(f"{900}x{700}")
        self.root.resizable(False, False)
        self.show_main_menu()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear()
        MainMenu(self.root, self.show_game)

    def show_game(self):
        self.clear()
        GameScreen(self.root, self.show_main_menu, self.show_win)

    def show_win(self):
        self.clear()
        WinScreen(self.root, self.show_game, self.show_main_menu)

if __name__ == "__main__":
    app = App()
    app.root.mainloop()
