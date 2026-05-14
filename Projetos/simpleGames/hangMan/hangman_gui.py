import tkinter as tk
from tkinter import messagebox, font
import random
from wordsHang import words
from PIL import Image, ImageTk
import os

# Color scheme
GOLDEN_LIGHT = "#FFD700"
GOLDEN_DARK = "#DAA520"
WOODY_DARK = "#654321"
WOODY_MEDIUM = "#8B4513"
WOODY_LIGHT = "#A0522D"
CREAM = "#F5DEB3"
WHITE = "#FFFFFF"

# Hangman stages (ASCII art)
HANGMAN_STAGES = [
    """
       ------
       |    |
       |
       |
       |
       |
       ---------
    """,
    """
       ------
       |    |
       O    |
       |
       |
       |
       ---------
    """,
    """
       ------
       |    |
       O    |
       |    |
       |
       |
       ---------
    """,
    """
       ------
       |    |
       O    |
      /|    |
       |
       |
       ---------
    """,
    """
       ------
       |    |
       O    |
      /|\\   |
       |
       |
       ---------
    """,
    """
       ------
       |    |
       O    |
      /|\\   |
      /     |
       |
       ---------
    """,
    """
       ------
       |    |
       O    |
      /|\\   |
      / \\   |
       |
       ---------
    """
]

class HangmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game - Golden & Woody Edition")
        self.root.geometry("900x700")
        self.root.configure(bg=WOODY_DARK)
        
        # Set window icon
        icon_path = os.path.join(os.path.dirname(__file__), "hangImages", "hangFav.png")
        if os.path.exists(icon_path):
            try:
                icon_image = Image.open(icon_path)
                icon_photo = ImageTk.PhotoImage(icon_image)
                self.root.iconphoto(False, icon_photo)
                self.icon_photo = icon_photo  # Keep a reference
            except Exception as e:
                print(f"Could not load icon: {e}")
        
        # Game variables
        self.answer = None
        self.hint = None
        self.wrong_guesses = 0
        self.guessed_letters = set()
        self.is_running = False
        
        self.setup_ui()
        self.start_new_game()
        
    def setup_ui(self):
        # Title frame
        title_frame = tk.Frame(self.root, bg=WOODY_DARK)
        title_frame.pack(pady=15)
        
        # Load and display icon image
        icon_path = os.path.join(os.path.dirname(__file__), "hangImages", "hangFav.png")
        if os.path.exists(icon_path):
            try:
                icon_image = Image.open(icon_path)
                icon_image.thumbnail((60, 60), Image.Resampling.LANCZOS)
                icon_photo = ImageTk.PhotoImage(icon_image)
                icon_label = tk.Label(title_frame, image=icon_photo, bg=WOODY_DARK)
                icon_label.pack(side=tk.LEFT, padx=10)
                self.icon_display = icon_photo  # Keep a reference
            except Exception as e:
                print(f"Could not load icon: {e}")
        
        # Title
        title_font = font.Font(family="Helvetica", size=24, weight="bold")
        title_label = tk.Label(
            title_frame,
            text="🎮 HANGMAN GAME 🎮",
            font=title_font,
            fg=GOLDEN_LIGHT,
            bg=WOODY_DARK
        )
        title_label.pack(side=tk.LEFT, padx=10)
        
        # Main frame
        main_frame = tk.Frame(self.root, bg=WOODY_DARK)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left side - Hangman drawing
        left_frame = tk.Frame(main_frame, bg=WOODY_MEDIUM, relief=tk.RAISED, bd=3)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=10)
        
        self.hangman_label = tk.Label(
            left_frame,
            font=("Courier", 11),
            fg=CREAM,
            bg=WOODY_MEDIUM,
            width=30,
            height=20,
            justify=tk.CENTER
        )
        self.hangman_label.pack(padx=10, pady=10)
        
        # Right side
        right_frame = tk.Frame(main_frame, bg=WOODY_DARK)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        
        # Statistics frame
        stats_frame = tk.Frame(right_frame, bg=WOODY_LIGHT, relief=tk.SUNKEN, bd=2)
        stats_frame.pack(fill=tk.X, pady=10)
        
        self.wrong_label = tk.Label(
            stats_frame,
            text="Wrong Guesses: 0/6",
            font=("Helvetica", 12, "bold"),
            fg=CREAM,
            bg=WOODY_LIGHT
        )
        self.wrong_label.pack(pady=10)
        
        # Word display frame
        word_frame = tk.Frame(right_frame, bg=GOLDEN_DARK, relief=tk.RAISED, bd=3)
        word_frame.pack(fill=tk.X, pady=10)
        
        word_label = tk.Label(
            word_frame,
            text="Word to Guess:",
            font=("Helvetica", 11, "bold"),
            fg=WOODY_DARK,
            bg=GOLDEN_DARK
        )
        word_label.pack(pady=5)
        
        self.word_display = tk.Label(
            word_frame,
            font=("Helvetica", 16, "bold"),
            fg=WOODY_DARK,
            bg=GOLDEN_LIGHT,
            padx=20,
            pady=15
        )
        self.word_display.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Guessed letters frame
        letters_frame = tk.Frame(right_frame, bg=WOODY_LIGHT, relief=tk.SUNKEN, bd=2)
        letters_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        letters_label = tk.Label(
            letters_frame,
            text="Guessed Letters:",
            font=("Helvetica", 11, "bold"),
            fg=CREAM,
            bg=WOODY_LIGHT
        )
        letters_label.pack(pady=5)
        
        self.letters_display = tk.Label(
            letters_frame,
            font=("Helvetica", 10),
            fg=GOLDEN_LIGHT,
            bg=WOODY_MEDIUM,
            wraplength=300,
            justify=tk.CENTER,
            padx=10,
            pady=10
        )
        self.letters_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Letter input frame
        input_frame = tk.Frame(right_frame, bg=WOODY_DARK)
        input_frame.pack(fill=tk.X, pady=10)
        
        input_label = tk.Label(
            input_frame,
            text="Enter Letter:",
            font=("Helvetica", 10, "bold"),
            fg=GOLDEN_LIGHT,
            bg=WOODY_DARK
        )
        input_label.pack(side=tk.LEFT, padx=5)
        
        self.input_entry = tk.Entry(
            input_frame,
            font=("Helvetica", 12),
            width=5,
            bg=CREAM,
            fg=WOODY_DARK
        )
        self.input_entry.pack(side=tk.LEFT, padx=5)
        self.input_entry.bind("<Return>", lambda e: self.make_guess())
        
        guess_btn = tk.Button(
            input_frame,
            text="Guess",
            font=("Helvetica", 10, "bold"),
            bg=GOLDEN_DARK,
            fg=WOODY_DARK,
            command=self.make_guess,
            relief=tk.RAISED,
            bd=2
        )
        guess_btn.pack(side=tk.LEFT, padx=5)
        
        # Buttons frame
        buttons_frame = tk.Frame(right_frame, bg=WOODY_DARK)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        new_game_btn = tk.Button(
            buttons_frame,
            text="New Game",
            font=("Helvetica", 10, "bold"),
            bg=GOLDEN_LIGHT,
            fg=WOODY_DARK,
            command=self.start_new_game,
            relief=tk.RAISED,
            bd=2,
            padx=15
        )
        new_game_btn.pack(side=tk.LEFT, padx=5)
        
        hint_btn = tk.Button(
            buttons_frame,
            text="Get Hint",
            font=("Helvetica", 10, "bold"),
            bg=WOODY_LIGHT,
            fg=CREAM,
            command=self.show_hint,
            relief=tk.RAISED,
            bd=2,
            padx=15
        )
        hint_btn.pack(side=tk.LEFT, padx=5)
        
        quit_btn = tk.Button(
            buttons_frame,
            text="Quit",
            font=("Helvetica", 10, "bold"),
            bg=WOODY_MEDIUM,
            fg=CREAM,
            command=self.root.quit,
            relief=tk.RAISED,
            bd=2,
            padx=15
        )
        quit_btn.pack(side=tk.LEFT, padx=5)
        
    def start_new_game(self):
        self.answer = random.choice(words).upper()
        self.hint = ["_"] * len(self.answer)
        self.wrong_guesses = 0
        self.guessed_letters = set()
        self.is_running = True
        self.input_entry.delete(0, tk.END)
        self.input_entry.focus()
        self.update_display()
        
    def make_guess(self):
        if not self.is_running:
            messagebox.showinfo("Game Over", "Please start a new game.")
            return
        
        guess = self.input_entry.get().strip().upper()
        self.input_entry.delete(0, tk.END)
        
        if len(guess) != 1 or not guess.isalpha():
            messagebox.showwarning("Invalid Input", "Please enter a single letter.")
            return
        
        if guess in self.guessed_letters:
            messagebox.showinfo("Already Guessed", f"You already guessed '{guess}'.")
            self.input_entry.focus()
            return
        
        self.guessed_letters.add(guess)
        
        if guess in self.answer:
            for i in range(len(self.answer)):
                if self.answer[i] == guess:
                    self.hint[i] = guess
        else:
            self.wrong_guesses += 1
        
        self.update_display()
        self.check_game_status()
        self.input_entry.focus()
        
    def show_hint(self):
        if not self.is_running:
            messagebox.showinfo("Game Over", "Please start a new game.")
            return
        
        hint_msg = f"The word has {len(self.answer)} letters.\nIt's an animal."
        messagebox.showinfo("Hint", hint_msg)
        
    def update_display(self):
        # Update hangman drawing
        self.hangman_label.config(text=HANGMAN_STAGES[self.wrong_guesses])
        
        # Update word display
        word_display_text = " ".join(self.hint)
        self.word_display.config(text=word_display_text)
        
        # Update wrong guesses
        self.wrong_label.config(text=f"Wrong Guesses: {self.wrong_guesses}/6")
        
        # Update guessed letters
        guessed_text = ", ".join(sorted(self.guessed_letters)) if self.guessed_letters else "None yet"
        self.letters_display.config(text=guessed_text)
        
    def check_game_status(self):
        if "_" not in self.hint:
            self.is_running = False
            messagebox.showinfo("🎉 YOU WIN! 🎉", f"The word was: {self.answer}")
        elif self.wrong_guesses >= 6:
            self.is_running = False
            messagebox.showinfo("💀 YOU LOSE! 💀", f"The word was: {self.answer}")

def main():
    root = tk.Tk()
    app = HangmanGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
