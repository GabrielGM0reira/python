import tkinter as tk
from tkinter import messagebox
from wordsHang import words
import random

class HangmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Hangman")
        self.root.geometry("600x650")
        self.root.configure(bg="#1e1e1e")
        
        self.hangman_art = {
            0: "   \n   \n   ",
            1: " o \n   \n   ",
            2: " o \n | \n   ",
            3: " o \n/| \n   ",
            4: " o \n/|\\\n   ",
            5: " o \n/|\\\n/  ",
            6: " o \n/|\\\n/ \\"
        }
        
        self.reset_game()
        self.setup_ui()
    
    def reset_game(self):
        self.answer = random.choice(words).upper()
        self.hint = ['_'] * len(self.answer)
        self.wrong_guesses = 0
        self.guessed_letters = set()
        self.is_running = True
    
    def setup_ui(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Title
        title = tk.Label(self.root, text="🎮 HANGMAN", bg="#1e1e1e", fg="#00ff00",
                        font=("Arial", 16, "bold"))
        title.pack(pady=(20, 10))
        
        # Hangman display
        self.hangman_label = tk.Label(self.root, text=self.hangman_art[self.wrong_guesses],
                                      bg="#1e1e1e", fg="#ffff00", font=("Courier", 11),
                                      justify=tk.CENTER)
        self.hangman_label.pack()
        
        # Wrong guesses counter
        self.wrong_label = tk.Label(self.root, text=f"Wrong guesses: {self.wrong_guesses}/{len(self.hangman_art)-1}",
                                   bg="#1e1e1e", fg="#ff6666", font=("Arial", 11, "bold"))
        self.wrong_label.pack(pady=10)
        
        # Word display
        self.word_label = tk.Label(self.root, text=" ".join(self.hint), bg="#1e1e1e",
                                  fg="#00ff00", font=("Arial", 20, "bold"))
        self.word_label.pack(pady=15)
        
        # Guessed letters display
        self.guessed_label = tk.Label(self.root, text=f"Guessed: {', '.join(sorted(self.guessed_letters)) or 'None'}",
                                     bg="#1e1e1e", fg="#cccccc", font=("Arial", 10),
                                     wraplength=550)
        self.guessed_label.pack(pady=10)
        
        # Input frame
        input_frame = tk.Frame(self.root, bg="#1e1e1e")
        input_frame.pack(pady=15)
        
        tk.Label(input_frame, text="Guess a letter:", bg="#1e1e1e", fg="#cccccc",
                font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
        
        self.letter_var = tk.StringVar()
        self.letter_entry = tk.Entry(input_frame, textvariable=self.letter_var, width=5,
                                    font=("Arial", 14, "bold"), bg="#333333", fg="#ffff00")
        self.letter_entry.pack(side=tk.LEFT, padx=5)
        self.letter_entry.bind('<Return>', lambda e: self.guess_letter())
        
        guess_btn = tk.Button(input_frame, text="Guess", command=self.guess_letter,
                             bg="#0066cc", fg="white", font=("Arial", 11, "bold"),
                             padx=15, pady=5, cursor="hand2")
        guess_btn.pack(side=tk.LEFT, padx=5)
        
        # Result frame
        self.result_frame = tk.Frame(self.root, bg="#2d2d2d", relief=tk.SUNKEN, bd=2)
        self.result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.result_label = tk.Label(self.result_frame, text="", bg="#2d2d2d", fg="#ffff00",
                                    font=("Arial", 12), justify=tk.CENTER)
        self.result_label.pack(fill=tk.BOTH, expand=True)
        
        # Buttons frame
        btn_frame = tk.Frame(self.root, bg="#1e1e1e")
        btn_frame.pack(pady=(10, 20))
        
        new_game_btn = tk.Button(btn_frame, text="New Game", command=self.new_game,
                                bg="#ff6600", fg="white", font=("Arial", 10, "bold"),
                                padx=15, pady=8, cursor="hand2")
        new_game_btn.pack(side=tk.LEFT, padx=5)
        
        hint_btn = tk.Button(btn_frame, text="Show Answer", command=self.show_answer,
                           bg="#666600", fg="white", font=("Arial", 10, "bold"),
                           padx=15, pady=8, cursor="hand2")
        hint_btn.pack(side=tk.LEFT, padx=5)
    
    def guess_letter(self):
        guess = self.letter_var.get().strip().upper()
        self.letter_var.set("")
        
        if not guess:
            messagebox.showerror("Invalid", "Please enter a letter")
            return
        
        if len(guess) != 1:
            messagebox.showerror("Invalid", "Please enter only ONE letter")
            return
        
        if not guess.isalpha():
            messagebox.showerror("Invalid", "Please enter a letter (A-Z only)")
            return
        
        if guess in self.guessed_letters:
            messagebox.showinfo("Already guessed", f"{guess} was already guessed")
            return
        
        self.guessed_letters.add(guess)
        
        if guess in self.answer:
            for i in range(len(self.answer)):
                if self.answer[i] == guess:
                    self.hint[i] = guess
        else:
            self.wrong_guesses += 1
        
        # Update display
        self.hangman_label.config(text=self.hangman_art[self.wrong_guesses])
        self.word_label.config(text=" ".join(self.hint))
        self.wrong_label.config(text=f"Wrong guesses: {self.wrong_guesses}/{len(self.hangman_art)-1}")
        self.guessed_label.config(text=f"Guessed: {', '.join(sorted(self.guessed_letters))}")
        
        # Check win/loss
        if "_" not in self.hint:
            self.result_label.config(text="🎉 YOU WIN! 🎉", fg="#00ff00")
            self.is_running = False
            self.letter_entry.config(state=tk.DISABLED)
        elif self.wrong_guesses >= len(self.hangman_art) - 1:
            self.result_label.config(text=f"😢 YOU LOSE! 😢\n\nThe word was: {self.answer}", fg="#ff6666")
            self.is_running = False
            self.letter_entry.config(state=tk.DISABLED)
    
    def new_game(self):
        self.reset_game()
        self.setup_ui()
    
    def show_answer(self):
        if not self.is_running:
            messagebox.showinfo("Game Over", "Game has ended")
            return
        self.result_label.config(text=f"The answer is: {self.answer}", fg="#ffff00")

if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanGUI(root)
    root.mainloop()
