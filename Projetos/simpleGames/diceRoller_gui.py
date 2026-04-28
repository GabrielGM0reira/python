import tkinter as tk
from tkinter import messagebox, ttk
from random import randint
from operator import itemgetter

class DiceRollerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎲 Dice Roller")
        self.root.geometry("500x400")
        self.root.configure(bg="#1e1e1e")
        
        style = ttk.Style()
        style.configure('Title.TLabel', background="#1e1e1e", foreground="#00ff00", font=("Arial", 16, "bold"))
        style.configure('Result.TLabel', background="#1e1e1e", foreground="#ffff00", font=("Arial", 11))
        style.configure('TLabel', background="#1e1e1e", foreground="#cccccc")
        
        # Main frame
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title = ttk.Label(main_frame, text="🎲 DICE ROLLER", style='Title.TLabel')
        title.pack(pady=(0, 20))
        
        # Number of players
        player_frame = ttk.Frame(main_frame)
        player_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(player_frame, text="Number of Players:").pack(side=tk.LEFT, padx=5)
        self.player_var = tk.StringVar(value="4")
        player_spin = ttk.Spinbox(player_frame, from_=2, to=4, textvariable=self.player_var, width=5)
        player_spin.pack(side=tk.LEFT, padx=5)
        
        # Roll button
        button_frame = tk.Frame(main_frame, bg="#1e1e1e")
        button_frame.pack(pady=20)
        
        roll_button = tk.Button(button_frame, text="🎲 ROLL DICE", command=self.roll_dice,
                               bg="#0066cc", fg="white", font=("Arial", 12, "bold"),
                               padx=20, pady=10, cursor="hand2")
        roll_button.pack(side=tk.LEFT, padx=5)
        
        reset_button = tk.Button(button_frame, text="Clear Results", command=self.clear_results,
                                bg="#ff6600", fg="white", font=("Arial", 12, "bold"),
                                padx=20, pady=10, cursor="hand2")
        reset_button.pack(side=tk.LEFT, padx=5)
        
        # Results frame
        result_frame = tk.Frame(main_frame, bg="#2d2d2d", relief=tk.SUNKEN, bd=2)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Results text
        scrollbar = ttk.Scrollbar(result_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.result_text = tk.Text(result_frame, bg="#1e1e1e", fg="#ffff00", 
                                   font=("Courier", 10), yscrollcommand=scrollbar.set,
                                   relief=tk.FLAT, borderwidth=0)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.config(command=self.result_text.yview)
        
    def roll_dice(self):
        try:
            num_players = int(self.player_var.get())
            if num_players < 2 or num_players > 4:
                messagebox.showerror("Error", "Players must be between 2 and 4")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid number of players")
            return
            
            # Roll dice for each player
            game = {}
            for i in range(1, num_players + 1):
                game[f'player{i}'] = randint(1, 6)
            
            # Sort by result
            ranking = sorted(game.items(), key=itemgetter(1), reverse=True)
            
            # Display results
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "=" * 40 + "\n")
            self.result_text.insert(tk.END, "DICE ROLLS:\n")
            self.result_text.insert(tk.END, "=" * 40 + "\n\n")
            
            for player, value in game.items():
                self.result_text.insert(tk.END, f"{player}: {value}\n")
            
            self.result_text.insert(tk.END, "\n" + "=" * 40 + "\n")
            self.result_text.insert(tk.END, "RANKING:\n")
            self.result_text.insert(tk.END, "=" * 40 + "\n")
            
            for i, (player, value) in enumerate(ranking, 1):
                self.result_text.insert(tk.END, f"{i}º place: {player.upper()} with {value}\n")
            
        except ValueError:
            messagebox.showerror("Error", "Invalid number of players")
    
    def clear_results(self):
        """Clear the results display"""
        self.result_text.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = DiceRollerGUI(root)
    root.mainloop()
