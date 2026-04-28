import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
from pathlib import Path

class GameLauncher:
    def __init__(self, root):
        self.root = root
        self.script_dir = Path(__file__).parent  # Get the directory of this script
        self.active_processes = []  # Track running processes
        self.game_buttons = {}  # Store button references for state management
        
        self.root.title("🎮 Minigames Launcher")
        self.root.geometry("600x700")
        self.root.configure(bg="#1e1e1e")
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background="#1e1e1e")
        style.configure('Title.TLabel', background="#1e1e1e", foreground="#00ff00", font=("Arial", 20, "bold"))
        style.configure('Game.TButton', font=("Arial", 12, "bold"), padding=20)
        style.configure('Description.TLabel', background="#1e1e1e", foreground="#cccccc", font=("Arial", 10))
        
        # Main frame
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame, text="🎮 MINIGAMES LAUNCHER", style='Title.TLabel')
        title_label.pack(pady=(0, 30))
        
        # Canvas for scrollable content
        canvas = tk.Canvas(main_frame, bg="#1e1e1e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add mouse wheel scrolling support
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Games list with validation
        games_config = [
            {
                "name": "🎲 Dice Roller",
                "file": "diceRoller_gui.py",
                "description": "Roll dice with up to 4 players and see the ranking!"
            },
            {
                "name": "🎰 Slot Machine",
                "file": "slotMachine_gui.py",
                "description": "Try your luck on the slot machine and win big!"
            },
            {
                "name": "✋ Jokenpo (Rock-Paper-Scissors)",
                "file": "jokenpo_gui.py",
                "description": "Classic rock, paper, scissors game against the computer"
            },
            {
                "name": "🎯 Quiz Game",
                "file": "simpleQuiz_gui.py",
                "description": "Answer trivia questions and test your knowledge"
            },
            {
                "name": "🎮 Hangman",
                "file": "hangMan_gui.py",
                "description": "Guess the word before the hangman is complete!"
            }
        ]
        
        # Filter games by checking if files exist
        self.games = []
        for game in games_config:
            game_path = self.script_dir / game["file"]
            if game_path.exists():
                game["full_path"] = str(game_path)
                self.games.append(game)
            else:
                print(f"Warning: Game file not found: {game_path}")
        
        # Create buttons for each game
        for game in self.games:
            self._create_game_button(scrollable_frame, game)
        
        canvas.pack(side="left", fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Footer
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(pady=(20, 0))
        exit_button = tk.Button(footer_frame, text="Exit Launcher", command=root.quit, 
                               bg="#ff4444", fg="white", font=("Arial", 11, "bold"), 
                               padx=20, pady=10, cursor="hand2")
        exit_button.pack()
    
    def _create_game_button(self, parent, game):
        # Game frame
        game_frame = tk.Frame(parent, bg="#2d2d2d", relief=tk.RAISED, bd=1)
        game_frame.pack(fill=tk.X, pady=10)
        
        # Game name button
        name_button = tk.Button(
            game_frame,
            text=game["name"],
            command=lambda g=game: self._launch_game(g, name_button),
            bg="#0066cc",
            fg="white",
            font=("Arial", 13, "bold"),
            padx=20,
            pady=12,
            cursor="hand2",
            relief=tk.RAISED,
            bd=2,
            activebackground="#0052a3"
        )
        name_button.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        # Store button reference for state management
        self.game_buttons[game["file"]] = name_button
        
        # Description label
        desc_label = ttk.Label(game_frame, text=game["description"], style='Description.TLabel')
        desc_label.pack(padx=15, pady=(0, 10))
    
    def _launch_game(self, game, button):
        try:
            # Check if file exists
            game_path = Path(game["full_path"])
            if not game_path.exists():
                messagebox.showerror("Error", f"Game file not found:\n{game_path}")
                return
            
            # Disable button and show launching status
            button.config(state=tk.DISABLED, bg="#666666", text=f"{game['name']} (Launching...)")
            self.root.update()
            
            # Launch game with full path
            process = subprocess.Popen(
                [sys.executable, str(game_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Track process
            self.active_processes.append(process)
            
            # Show success notification
            messagebox.showinfo("Success", f"Launched: {game['name']}")
            
            # Re-enable button after a brief delay
            self.root.after(1500, lambda: self._reset_button(button, game))
            
        except Exception as e:
            # Show error notification
            messagebox.showerror("Launch Error", f"Failed to launch {game['name']}:\n{str(e)}")
            # Reset button on error
            button.config(state=tk.NORMAL, bg="#0066cc", text=game["name"])
    
    def _reset_button(self, button, game):
        """Reset button state after game launch"""
        button.config(state=tk.NORMAL, bg="#0066cc", text=game["name"])

if __name__ == "__main__":
    root = tk.Tk()
    app = GameLauncher(root)
    root.mainloop()
