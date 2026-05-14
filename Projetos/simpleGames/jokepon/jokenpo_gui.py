import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from random import randint
import os

class JokenpoGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Jokenpo Game - Rock Paper Scissors")
        self.root.geometry("800x650")
        self.root.configure(bg='#f0f0f0')
        
        # Game variables
        self.items = ('rock', 'paper', 'scissors')
        self.player_choice = None
        self.computer_choice = None
        self.result = None
        
        # Score tracking
        self.wins = 0
        self.losses = 0
        self.ties = 0
        
        # Load images
        self.images = {}
        self.load_images()
        
        # Create GUI elements
        self.create_widgets()
        
    def load_images(self):
        """Load images from the images folder"""
        images_folder = os.path.join(os.path.dirname(__file__), 'images')
        
        for item in self.items:
            try:
                img_path = os.path.join(images_folder, f'{item}.png')
                if os.path.exists(img_path):
                    img = Image.open(img_path)
                    img = img.resize((150, 150), Image.Resampling.LANCZOS)
                    self.images[item] = ImageTk.PhotoImage(img)
                else:
                    print(f"Warning: Image not found for {item}")
            except Exception as e:
                print(f"Error loading image for {item}: {e}")
    
    def create_widgets(self):
        """Create all GUI elements"""
        
        # Title
        title = tk.Label(self.root, text="JOKENPO - ROCK PAPER SCISSORS", 
                        font=("Arial", 20, "bold"), bg='#f0f0f0', fg='#333')
        title.pack(pady=20)
        
        # Score frame
        score_frame = ttk.Frame(self.root)
        score_frame.pack(pady=10)
        
        ttk.Label(score_frame, text="Wins:").grid(row=0, column=0, padx=20)
        self.wins_label = ttk.Label(score_frame, text="0", foreground='green')
        self.wins_label.grid(row=0, column=1, padx=5)
        
        ttk.Label(score_frame, text="Ties:").grid(row=0, column=2, padx=20)
        self.ties_label = ttk.Label(score_frame, text="0", foreground='blue')
        self.ties_label.grid(row=0, column=3, padx=5)
        
        ttk.Label(score_frame, text="Losses:").grid(row=0, column=4, padx=20)
        self.losses_label = ttk.Label(score_frame, text="0", foreground='red')
        self.losses_label.grid(row=0, column=5, padx=5)
        
        # Buttons frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)
        
        ttk.Label(button_frame, text="Choose your move:", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=3, pady=10)
        
        # Rock button
        self.rock_btn = tk.Button(button_frame, image=self.images.get('rock'), 
                                  command=lambda: self.play('rock'), bg='white', 
                                  relief='raised', bd=2)
        self.rock_btn.grid(row=1, column=0, padx=15, pady=10)
        ttk.Label(button_frame, text="Rock", font=("Arial", 10)).grid(row=2, column=0)
        
        # Paper button
        self.paper_btn = tk.Button(button_frame, image=self.images.get('paper'), 
                                   command=lambda: self.play('paper'), bg='white', 
                                   relief='raised', bd=2)
        self.paper_btn.grid(row=1, column=1, padx=15, pady=10)
        ttk.Label(button_frame, text="Paper", font=("Arial", 10)).grid(row=2, column=1)
        
        # Scissors button
        self.scissors_btn = tk.Button(button_frame, image=self.images.get('scissors'), 
                                      command=lambda: self.play('scissors'), bg='white', 
                                      relief='raised', bd=2)
        self.scissors_btn.grid(row=1, column=2, padx=15, pady=10)
        ttk.Label(button_frame, text="Scissors", font=("Arial", 10)).grid(row=2, column=2)
        
        # Result frame
        result_frame = ttk.LabelFrame(self.root, text="Result", padding=15)
        result_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Player choice
        ttk.Label(result_frame, text="Your choice:", font=("Arial", 11, "bold")).pack()
        self.player_label = ttk.Label(result_frame, text="---", font=("Arial", 10))
        self.player_label.pack()
        
        # Computer choice
        ttk.Label(result_frame, text="Computer choice:", font=("Arial", 11, "bold")).pack(pady=(15, 0))
        self.computer_label = ttk.Label(result_frame, text="---", font=("Arial", 10))
        self.computer_label.pack()
        
        # Result message
        ttk.Label(result_frame, text="Outcome:", font=("Arial", 11, "bold")).pack(pady=(15, 0))
        self.result_label = ttk.Label(result_frame, text="Make your choice!", 
                                      font=("Arial", 12, "bold"), foreground='blue')
        self.result_label.pack()
        
        # Reset button
        ttk.Button(self.root, text="Reset Score", command=self.reset_score).pack(pady=10)
    
    def play(self, player_choice):
        """Handle player's choice"""
        self.player_choice = player_choice
        self.computer_choice = self.items[randint(0, 2)]
        
        # Update labels
        self.player_label.config(text=self.player_choice.upper())
        self.computer_label.config(text=self.computer_choice.upper())
        
        # Determine result
        if self.player_choice == self.computer_choice:
            self.result = "It's a TIE!"
            self.ties += 1
            color = 'blue'
        elif (self.player_choice == 'rock' and self.computer_choice == 'scissors') or \
             (self.player_choice == 'paper' and self.computer_choice == 'rock') or \
             (self.player_choice == 'scissors' and self.computer_choice == 'paper'):
            self.result = "You WIN! 🎉"
            self.wins += 1
            color = 'green'
        else:
            self.result = "Computer WINS! 😢"
            self.losses += 1
            color = 'red'
        
        # Update result label
        self.result_label.config(text=self.result, foreground=color)
        
        # Update score
        self.wins_label.config(text=str(self.wins))
        self.ties_label.config(text=str(self.ties))
        self.losses_label.config(text=str(self.losses))
    
    def reset_score(self):
        """Reset the score"""
        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.wins_label.config(text="0")
        self.ties_label.config(text="0")
        self.losses_label.config(text="0")
        self.player_label.config(text="---")
        self.computer_label.config(text="---")
        self.result_label.config(text="Make your choice!", foreground='blue')

if __name__ == '__main__':
    root = tk.Tk()
    game = JokenpoGame(root)
    root.mainloop()
