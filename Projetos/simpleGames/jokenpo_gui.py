import tkinter as tk
from tkinter import messagebox
from random import randint

class JokenpoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("✋ Jokenpo (Rock-Paper-Scissors)")
        self.root.geometry("500x450")
        self.root.configure(bg="#1e1e1e")
        
        self.items = ('rock', 'paper', 'scissors')
        self.emojis = {'rock': '🪨', 'paper': '📄', 'scissors': '✂️'}
        self.score_player = 0
        self.score_computer = 0
        self.ties = 0
        
        style_title = tk.Label(root, text="✋ JOKENPO GAME", bg="#1e1e1e", fg="#00ff00", 
                              font=("Arial", 16, "bold"))
        style_title.pack(pady=(20, 10))
        
        # Instructions
        instructions = tk.Label(root, text="Choose your move:", bg="#1e1e1e", fg="#cccccc",
                               font=("Arial", 11))
        instructions.pack(pady=5)
        
        # Buttons frame
        buttons_frame = tk.Frame(root, bg="#1e1e1e")
        buttons_frame.pack(pady=20)
        
        rock_btn = tk.Button(buttons_frame, text="🪨 Rock", command=lambda: self.play(0),
                            bg="#0066cc", fg="white", font=("Arial", 11, "bold"),
                            padx=15, pady=10, cursor="hand2")
        rock_btn.pack(side=tk.LEFT, padx=10)
        
        paper_btn = tk.Button(buttons_frame, text="📄 Paper", command=lambda: self.play(1),
                             bg="#0066cc", fg="white", font=("Arial", 11, "bold"),
                             padx=15, pady=10, cursor="hand2")
        paper_btn.pack(side=tk.LEFT, padx=10)
        
        scissors_btn = tk.Button(buttons_frame, text="✂️ Scissors", command=lambda: self.play(2),
                                bg="#0066cc", fg="white", font=("Arial", 11, "bold"),
                                padx=15, pady=10, cursor="hand2")
        scissors_btn.pack(side=tk.LEFT, padx=10)
        
        # Result frame
        result_frame = tk.Frame(root, bg="#2d2d2d", relief=tk.SUNKEN, bd=2)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.result_label = tk.Label(result_frame, text="", bg="#2d2d2d", fg="#ffff00",
                                    font=("Arial", 12, "bold"), wraplength=400, justify=tk.CENTER)
        self.result_label.pack(fill=tk.BOTH, expand=True)
        
        # Score frame
        score_frame = tk.Frame(root, bg="#1e1e1e")
        score_frame.pack(pady=(10, 20), fill=tk.X, padx=20)
        
        self.score_label = tk.Label(score_frame, text=f"You: {self.score_player} | Computer: {self.score_computer} | Ties: {self.ties}",
                                   bg="#1e1e1e", fg="#00ff00", font=("Arial", 11, "bold"))
        self.score_label.pack()
        
        # Reset button
        reset_btn = tk.Button(root, text="Reset Score", command=self.reset_score,
                             bg="#ff6600", fg="white", font=("Arial", 10, "bold"),
                             padx=15, pady=8, cursor="hand2")
        reset_btn.pack(pady=(0, 20))
    
    def play(self, player_choice):
        computer_choice = randint(0, 2)
        
        player_move = self.items[player_choice]
        computer_move = self.items[computer_choice]
        
        # Determine winner
        if player_choice == computer_choice:
            result = "TIE! 🤝"
            self.ties += 1
        elif (player_choice == 0 and computer_choice == 2) or \
             (player_choice == 1 and computer_choice == 0) or \
             (player_choice == 2 and computer_choice == 1):
            result = "YOU WIN! 🎉"
            self.score_player += 1
        else:
            result = "COMPUTER WINS! 🤖"
            self.score_computer += 1
        
        # Update result display
        result_text = f"You played: {self.emojis[player_move]} {player_move.upper()}\n"
        result_text += f"Computer played: {self.emojis[computer_move]} {computer_move.upper()}\n\n"
        result_text += result
        
        self.result_label.config(text=result_text)
        self.score_label.config(text=f"You: {self.score_player} | Computer: {self.score_computer} | Ties: {self.ties}")
    
    def reset_score(self):
        self.score_player = 0
        self.score_computer = 0
        self.ties = 0
        self.result_label.config(text="")
        self.score_label.config(text=f"You: {self.score_player} | Computer: {self.score_computer} | Ties: {self.ties}")

if __name__ == "__main__":
    root = tk.Tk()
    app = JokenpoGUI(root)
    root.mainloop()
