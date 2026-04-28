import tkinter as tk
from tkinter import messagebox
import random

class SlotMachineGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎰 Slot Machine")
        self.root.geometry("500x550")
        self.root.configure(bg="#1e1e1e")
        
        self.balance = 100
        self.symbols = ['🍒 Cherry', '🍉 Watermelon', '🍋 Lemon', '🔔 Bell', '⭐ Star']
        self.symbol_keys = ['cherry', 'watermelon', 'lemon', 'bell', 'star']
        self.payouts = {'cherry': 3, 'watermelon': 4, 'lemon': 5, 'bell': 10, 'star': 20}
        
        # Title
        title = tk.Label(root, text="🎰 SLOT MACHINE", bg="#1e1e1e", fg="#ffff00",
                        font=("Arial", 16, "bold"))
        title.pack(pady=(20, 10))
        
        # Balance display
        self.balance_label = tk.Label(root, text=f"Balance: ${self.balance}", bg="#1e1e1e",
                                     fg="#00ff00", font=("Arial", 12, "bold"))
        self.balance_label.pack(pady=10)
        
        # Payout table
        payout_info = tk.Label(root, text="Payouts: Cherry(3x) | Watermelon(4x) | Lemon(5x) | Bell(10x) | Star(20x)",
                              bg="#1e1e1e", fg="#cccccc", font=("Arial", 9))
        payout_info.pack(pady=5)
        
        # Slot display frame
        slot_frame = tk.Frame(root, bg="#2d2d2d", relief=tk.RAISED, bd=3)
        slot_frame.pack(pady=20, padx=20)
        
        self.slot_labels = []
        for i in range(3):
            slot_label = tk.Label(slot_frame, text="?", bg="#111111", fg="#ffff00",
                                 font=("Arial", 40, "bold"), width=4, height=2,
                                 relief=tk.SUNKEN, bd=3)
            slot_label.pack(side=tk.LEFT, padx=10, pady=10)
            self.slot_labels.append(slot_label)
        
        # Bet frame
        bet_frame = tk.Frame(root, bg="#1e1e1e")
        bet_frame.pack(pady=10)
        
        tk.Label(bet_frame, text="Bet Amount:", bg="#1e1e1e", fg="#cccccc",
                font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
        
        self.bet_var = tk.StringVar(value="10")
        bet_entry = tk.Entry(bet_frame, textvariable=self.bet_var, width=10,
                           font=("Arial", 11), bg="#333333", fg="#ffff00")
        bet_entry.pack(side=tk.LEFT, padx=5)
        
        # Spin button
        spin_button = tk.Button(root, text="🎰 SPIN", command=self.spin,
                               bg="#ff6600", fg="white", font=("Arial", 12, "bold"),
                               padx=30, pady=15, cursor="hand2")
        spin_button.pack(pady=15)
        
        # Result frame
        result_frame = tk.Frame(root, bg="#2d2d2d", relief=tk.SUNKEN, bd=2)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.result_label = tk.Label(result_frame, text="", bg="#2d2d2d", fg="#ffff00",
                                    font=("Arial", 11), justify=tk.CENTER, wraplength=400)
        self.result_label.pack(fill=tk.BOTH, expand=True)
        
        # Reset button
        reset_button = tk.Button(root, text="Reset Balance", command=self.reset_balance,
                                bg="#0066cc", fg="white", font=("Arial", 10, "bold"),
                                padx=15, pady=8, cursor="hand2")
        reset_button.pack(pady=(0, 20))
    
    def spin(self):
        try:
            bet = int(self.bet_var.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid bet amount (whole number)")
            return
        
        if bet <= 0:
            messagebox.showerror("Error", "Bet must be greater than 0")
            return
        
        if bet > self.balance:
            messagebox.showerror("Error", f"Insufficient balance. You have ${self.balance}")
            return
        
        if bet > 100:
            messagebox.showerror("Error", "Maximum bet is $100")
            return
        
        # Deduct bet
        self.balance -= bet
        
        # Spin
        result = [random.choice(self.symbol_keys) for _ in range(3)]
        
        # Display results
        display_symbols = [self.symbols[self.symbol_keys.index(r)] for r in result]
        for i, symbol in enumerate(display_symbols):
            self.slot_labels[i].config(text=symbol.split()[0])
        
        # Check if won
        payout = 0
        if result[0] == result[1] == result[2]:
            payout = bet * self.payouts[result[0]]
            self.balance += payout
            self.result_label.config(text=f"🎉 JACKPOT! 🎉\n\nYou won ${payout}!")
        else:
            self.result_label.config(text=f"❌ Sorry, you lost ${bet}")
        
        self.balance_label.config(text=f"Balance: ${self.balance}")
        
        if self.balance <= 0:
            messagebox.showinfo("Game Over", "You're out of money! Reset to play again.")
    
    def reset_balance(self):
        self.balance = 100
        self.balance_label.config(text=f"Balance: ${self.balance}")
        for label in self.slot_labels:
            label.config(text="?")
        self.result_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = SlotMachineGUI(root)
    root.mainloop()
