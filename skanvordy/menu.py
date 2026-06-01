# menu.py
import tkinter as tk
from config import *

class MainMenu:
    def __init__(self, root, start_game):
        self.root = root
        self.start_game = start_game

        # Фон
        self.root.configure(bg=BG_COLOR)

        # Крестик
        close_btn = tk.Button(root, text="✕", font=("Arial", 16, "bold"),
                              bd=0, fg="red", bg=BG_COLOR, activebackground=BG_COLOR,
                              command=root.quit)
        close_btn.place(x=850, y=20)

        # Заголовок
        title = tk.Label(root, text="Сканворды", font=("Arial", 48, "bold"),
                         bg=BG_COLOR, fg="black")
        title.place(relx=0.5, rely=0.35, anchor="center")

        # Кнопка Играть
        play_btn = tk.Button(root, text="Играть", font=("Arial", 18, "bold"),
                             bg="black", fg="white", width=15, height=2,
                             command=start_game)
        play_btn.place(relx=0.5, rely=0.55, anchor="center")