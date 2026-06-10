# game.py

import tkinter as tk
from tkinter import messagebox
import os
import time
from config import *


class GameScreen:

    def __init__(self, root, back_to_menu, show_win):

        self.root = root
        self.back_to_menu = back_to_menu
        self.show_win = show_win

        self.entries = {}
        self.words = []
        self.active_cells = set()

        # ==================== ТАЙМЕР ====================

        self.timer_started = False
        self.start_time = 0
        self.elapsed_time = 0

        # =================================================

        self.load_words()
        self.prepare_grid()
        self.create_widgets()

    # =====================================================

    def load_words(self):

        path = os.path.join("data", "words.txt")

        if not os.path.exists(path):
            messagebox.showerror(
                "Ошибка",
                f"Файл не найден: {path}"
            )
            return

        with open(path, "r", encoding="utf-8") as f:

            for line in f:

                line = line.strip()

                if line and not line.startswith("#"):

                    parts = [x.strip() for x in line.split("|")]

                    if len(parts) == 5:

                        word, clue, direction, r, c = parts

                        self.words.append({
                            "word": word.upper(),
                            "clue": clue,
                            "dir": direction,
                            "row": int(r),
                            "col": int(c),
                            "number": len(self.words) + 1
                        })

    # =====================================================

    def prepare_grid(self):

        for word in self.words:

            r = word["row"]
            c = word["col"]

            for i in range(len(word["word"])):

                if word["dir"] == "across":
                    pos = (r, c + i)

                else:
                    pos = (r + i, c)

                self.active_cells.add(pos)

    # =====================================================

    def create_widgets(self):

        # ==================== НАЗАД ====================

        btn_back = tk.Button(
            self.root,
            text="← Назад",
            font=("Arial", 12),
            command=self.back_to_menu
        )

        btn_back.pack(anchor="nw", padx=20, pady=10)

        # ==================== ЗАГОЛОВОК ====================

        tk.Label(
            self.root,
            text="Сканворд",
            font=("Arial", 24, "bold")
        ).pack(pady=5)

        # ==================== ТАЙМЕР ====================

        self.timer_label = tk.Label(
            self.root,
            text="Время: 00:00",
            font=("Arial", 16, "bold"),
            fg="#333333"
        )

        self.timer_label.pack(pady=5)

        # ==================================================

        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=10)

        # ==================================================

        grid_frame = tk.Frame(main_frame)
        grid_frame.pack(side="left", padx=20)

        # ==================================================

        for i in range(GRID_SIZE):

            for j in range(GRID_SIZE):

                is_active = (i, j) in self.active_cells

                cell_frame = tk.Frame(
                    grid_frame,
                    width=CELL_SIZE,
                    height=CELL_SIZE,
                    bg="white" if is_active else "#333333",
                    highlightbackground="#666",
                    highlightthickness=1
                )

                cell_frame.grid(
                    row=i,
                    column=j,
                    padx=1,
                    pady=1
                )

                cell_frame.grid_propagate(False)

                # ==========================================
                # ЧЁРНАЯ КЛЕТКА
                # ==========================================

                if not is_active:
                    continue

                # ==========================================
                # ЦИФРЫ
                # ==========================================

                number = self.get_number_at(i, j)

                if number:

                    number_bg = tk.Frame(
                        cell_frame,
                        width=24,
                        height=16,
                        bg="white"
                    )

                    number_bg.place(x=0, y=0)

                    num_label = tk.Label(
                        number_bg,
                        text=str(number),
                        font=("Arial", 9, "bold"),
                        fg="#0022aa",
                        bg="white"
                    )

                    num_label.place(x=1, y=-1)

                    num_label.lift()

                # ==========================================
                # ПОЛЕ ВВОДА
                # ==========================================

                entry = tk.Entry(
                    cell_frame,
                    font=("Arial", 18, "bold"),
                    justify="center",
                    relief="flat",
                    bd=0,
                    bg="white",
                    insertbackground="black"
                )

                entry.place(
                    relx=0.16,
                    rely=0.42,
                    relwidth=0.70,
                    relheight=0.45
                )

                # ==========================================
                # СОБЫТИЯ
                # ==========================================

                entry.bind(
                    "<KeyRelease>",
                    lambda e, pos=(i, j):
                    self.on_key_release(e, pos)
                )

                entry.bind(
                    "<FocusIn>",
                    lambda e, pos=(i, j):
                    self.on_entry_focus(pos)
                )

                self.entries[(i, j)] = entry

        # ==================================================
        # ПОДСКАЗКИ
        # ==================================================

        clues_frame = tk.Frame(main_frame, width=380)
        clues_frame.pack(side="right", padx=30, fill="y")

        tk.Label(
            clues_frame,
            text="Подсказки:",
            font=("Arial", 16, "bold")
        ).pack(anchor="w", pady=(0, 10))

        for word in self.words:

            direction = (
                "→"
                if word["dir"] == "across"
                else "↓"
            )

            text = (
                f"{word['number']}. "
                f"{word['clue']} ({direction})"
            )

            lbl = tk.Label(
                clues_frame,
                text=text,
                font=("Arial", 12),
                anchor="w",
                justify="left",
                wraplength=350
            )

            lbl.pack(anchor="w", pady=4)

        # ==================================================
        # ПРОВЕРКА
        # ==================================================

        check_btn = tk.Button(
            self.root,
            text="Проверить",
            font=("Arial", 16, "bold"),
            bg="#4CAF50",
            fg="white",
            width=18,
            height=2,
            command=self.check_solution
        )

        check_btn.pack(pady=20)

    # =====================================================

    def start_timer(self):

        self.timer_started = True
        self.start_time = time.time()

        self.update_timer()

    # =====================================================

    def update_timer(self):

        if self.timer_started:

            self.elapsed_time = int(
                time.time() - self.start_time
            )

            minutes = self.elapsed_time // 60
            seconds = self.elapsed_time % 60

            self.timer_label.config(
                text=f"Время: {minutes:02}:{seconds:02}"
            )

            self.root.after(1000, self.update_timer)

    # =====================================================

    def stop_timer(self):

        self.timer_started = False

    # =====================================================

    def get_time_string(self):

        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60

        return f"{minutes:02}:{seconds:02}"

    # =====================================================

    def get_number_at(self, row, col):

        for word in self.words:

            if (
                word["row"] == row and
                word["col"] == col
            ):
                return word["number"]

        return None

    # =====================================================

    def on_key_release(self, event, pos):

        # ==================== СТАРТ ТАЙМЕРА ====================

        if not self.timer_started:
            self.start_timer()

        # ======================================================

        entry = self.entries[pos]

        text = entry.get().upper()

        if len(text) > 1:
            text = text[-1]

        entry.delete(0, tk.END)
        entry.insert(0, text)

        # автопереход

        if text:
            self.focus_next(pos)

    # =====================================================

    def focus_next(self, pos):

        row, col = pos

        possible = [
            (row, col + 1),
            (row + 1, col)
        ]

        for p in possible:

            if p in self.entries:
                self.entries[p].focus_set()
                break

    # =====================================================

    def on_entry_focus(self, pos):

        self.clear_highlight()

        for word in self.words:

            if self.is_in_word(pos, word):
                self.highlight_word(word)
                break

    # =====================================================

    def is_in_word(self, pos, word):

        r, c = pos

        wr = word["row"]
        wc = word["col"]

        length = len(word["word"])

        if word["dir"] == "across":

            return (
                r == wr and
                wc <= c < wc + length
            )

        else:

            return (
                c == wc and
                wr <= r < wr + length
            )

    # =====================================================

    def highlight_word(self, word):

        for i in range(len(word["word"])):

            if word["dir"] == "across":

                pos = (
                    word["row"],
                    word["col"] + i
                )

            else:

                pos = (
                    word["row"] + i,
                    word["col"]
                )

            if pos in self.entries:

                self.entries[pos].config(
                    bg=SELECTED_COLOR
                )

    # =====================================================

    def clear_highlight(self):

        for entry in self.entries.values():
            entry.config(bg="white")

    # =====================================================

    def check_solution(self):

        self.clear_highlight()

        correct = True

        for word in self.words:

            user_word = ""

            for i in range(len(word["word"])):

                if word["dir"] == "across":

                    pos = (
                        word["row"],
                        word["col"] + i
                    )

                else:

                    pos = (
                        word["row"] + i,
                        word["col"]
                    )

                user_word += (
                    self.entries[pos]
                    .get()
                    .strip()
                    .upper()
                )

            # ==============================================

            if user_word != word["word"]:

                correct = False

                for i in range(len(word["word"])):

                    if word["dir"] == "across":

                        pos = (
                            word["row"],
                            word["col"] + i
                        )

                    else:

                        pos = (
                            word["row"] + i,
                            word["col"]
                        )

                    if pos in self.entries:

                        self.entries[pos].config(
                            bg=WRONG_COLOR
                        )

        # ==============================================

        if correct:

            self.stop_timer()

            result_time = self.get_time_string()

            messagebox.showinfo(
                "Победа!",
                f"Вы решили сканворд!\n\n"
                f"Время: {result_time}"
            )

            self.show_win()

        else:

            messagebox.showinfo(
                "Результат",
                "Есть ошибки!\nКрасным выделены неверные буквы."
            )

