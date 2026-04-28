import tkinter as tk
from tkinter import messagebox, ttk
import random

class SimpleQuizGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Simple Quiz")
        self.root.geometry("600x650")
        self.root.configure(bg="#1e1e1e")
        
        self.questions = ("How many elements are in the periodic table?",
                         "Which animal lays eggs?",
                         "What is the most abundant gas in the earth's atmosphere?",
                         "How many bones are in the human body?",
                         "Which planet in the solar system is the hottest?",
                         "What is the capital of France?",
                         "How many continents are there?",
                         "What is the largest ocean?",
                         "In what year did the Titanic sink?",
                         "Who painted the Mona Lisa?",
                         "What is the smallest country in the world?",
                         "How many strings does a violin have?",
                         "What is the tallest mountain?",
                         "How many sides does a hexagon have?",
                         "What is the speed of light?")
        
        self.options = (("A. 116", "B. 117", "C. 118", "D. 119"),
                       ("A. Whale", "B. Crocodile", "C. Elephant", "D. Ostrich"),
                       ("A. Nitrogen", "B. Oxygen", "C. Carbon Dioxide", "D. Hydrogen"),
                       ("A. 206", "B. 207", "C. 208", "D. 209"),
                       ("A. Mercury", "B. Venus", "C. Earth", "D. Mars"),
                       ("A. London", "B. Paris", "C. Berlin", "D. Madrid"),
                       ("A. 5", "B. 6", "C. 7", "D. 8"),
                       ("A. Atlantic", "B. Pacific", "C. Arctic", "D. Indian"),
                       ("A. 1912", "B. 1913", "C. 1911", "D. 1915"),
                       ("A. Van Gogh", "B. Da Vinci", "C. Picasso", "D. Monet"),
                       ("A. Monaco", "B. Vatican", "C. San Marino", "D. Liechtenstein"),
                       ("A. 2", "B. 3", "C. 4", "D. 5"),
                       ("A. Mount Everest", "B. K2", "C. Kangchenjunga", "D. Lhotse"),
                       ("A. 4", "B. 5", "C. 6", "D. 8"),
                       ("A. 3 x 10^8 m/s", "B. 2 x 10^8 m/s", "C. 4 x 10^8 m/s", "D. 5 x 10^8 m/s"))
        
        self.answers = ("C", "D", "A", "A", "B", "B", "C", "B", "A", "B", "B", "C", "A", "C", "A")
        self.current_question = 0
        self.score = 0
        self.guesses = []
        self.user_answers = [None] * len(self.questions)
        
        # Shuffle questions with their corresponding options and answers
        combined = list(zip(self.questions, self.options, self.answers))
        random.shuffle(combined)
        self.questions, self.options, self.answers = zip(*combined)
        self.questions = list(self.questions)
        self.options = list(self.options)
        self.answers = list(self.answers)
        self.user_answers = [None] * len(self.questions)
        
        # Title
        title = tk.Label(root, text="🎯 QUIZ GAME", bg="#1e1e1e", fg="#00ff00",
                        font=("Arial", 16, "bold"))
        title.pack(pady=(20, 10))
        
        # Question number
        self.progress_label = tk.Label(root, text="", bg="#1e1e1e", fg="#cccccc",
                                      font=("Arial", 10))
        self.progress_label.pack()
        
        # Question text
        self.question_label = tk.Label(root, text="", bg="#1e1e1e", fg="#ffff00",
                                      font=("Arial", 12, "bold"), wraplength=550,
                                      justify=tk.CENTER)
        self.question_label.pack(pady=(20, 20))
        
        # Options frame
        self.options_frame = tk.Frame(root, bg="#1e1e1e")
        self.options_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)
        
        self.option_buttons = []
        self.selected_var = tk.StringVar()
        
        for i in range(4):
            btn = tk.Radiobutton(self.options_frame, text="", variable=self.selected_var,
                                value="", bg="#1e1e1e", fg="#cccccc", font=("Arial", 11),
                                selectcolor="#0066cc", activebackground="#1e1e1e",
                                activeforeground="#ffff00")
            btn.pack(anchor=tk.W, pady=8, padx=20)
            self.option_buttons.append(btn)
        
        # Navigation frame
        nav_frame = tk.Frame(root, bg="#1e1e1e")
        nav_frame.pack(pady=20)
        
        prev_btn = tk.Button(nav_frame, text="← Previous", command=self.prev_question,
                            bg="#0066cc", fg="white", font=("Arial", 10, "bold"),
                            padx=10, pady=8, cursor="hand2")
        prev_btn.pack(side=tk.LEFT, padx=5)
        
        next_btn = tk.Button(nav_frame, text="Next →", command=self.next_question,
                            bg="#0066cc", fg="white", font=("Arial", 10, "bold"),
                            padx=10, pady=8, cursor="hand2")
        next_btn.pack(side=tk.LEFT, padx=5)
        
        submit_btn = tk.Button(nav_frame, text="Submit Quiz", command=self.submit_quiz,
                              bg="#ff6600", fg="white", font=("Arial", 10, "bold"),
                              padx=10, pady=8, cursor="hand2")
        submit_btn.pack(side=tk.LEFT, padx=5)
        
        self.load_question()
    
    def load_question(self):
        self.progress_label.config(text=f"Question {self.current_question + 1}/{len(self.questions)}")
        self.question_label.config(text=self.questions[self.current_question])
        
        options = self.options[self.current_question]
        for i, option in enumerate(options):
            option_letter = option[0]
            self.option_buttons[i].config(text=option, value=option_letter)
        
        # Restore previous answer if exists
        if self.user_answers[self.current_question]:
            self.selected_var.set(self.user_answers[self.current_question])
        else:
            self.selected_var.set("")
    
    def prev_question(self):
        if self.current_question > 0:
            self.user_answers[self.current_question] = self.selected_var.get()
            self.current_question -= 1
            self.load_question()
    
    def next_question(self):
        if self.current_question < len(self.questions) - 1:
            self.user_answers[self.current_question] = self.selected_var.get()
            self.current_question += 1
            self.load_question()
    
    def submit_quiz(self):
        # Save last answer
        self.user_answers[self.current_question] = self.selected_var.get()
        
        # Check for unanswered questions
        if any(answer is None or answer == "" for answer in self.user_answers):
            messagebox.showwarning("Incomplete", "Please answer all questions before submitting")
            return
        
        # Calculate score
        score = 0
        for i, (answer, guess) in enumerate(zip(self.answers, self.user_answers)):
            if guess == answer:
                score += 1
        
        percentage = (score / len(self.questions)) * 100
        
        # Show results
        results_window = tk.Toplevel(self.root)
        results_window.title("Quiz Results")
        results_window.geometry("400x300")
        results_window.configure(bg="#1e1e1e")
        
        score_label = tk.Label(results_window, text="📊 QUIZ RESULTS", bg="#1e1e1e",
                              fg="#00ff00", font=("Arial", 14, "bold"))
        score_label.pack(pady=(20, 10))
        
        result_text = tk.Label(results_window, text=f"Your score:\n{score}/{len(self.questions)}\n{percentage:.1f}%",
                              bg="#1e1e1e", fg="#ffff00", font=("Arial", 16, "bold"))
        result_text.pack(pady=20)
        
        # Detailed results
        details_frame = tk.Frame(results_window, bg="#2d2d2d", relief=tk.SUNKEN, bd=2)
        details_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        details_text = tk.Text(details_frame, bg="#1e1e1e", fg="#ffff00", height=8,
                              font=("Courier", 9), relief=tk.FLAT)
        details_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for i, (question, user_answer, correct_answer) in enumerate(zip(self.questions, self.user_answers, self.answers)):
            status = "✓" if user_answer == correct_answer else "✗"
            details_text.insert(tk.END, f"{i+1}. {status}\n   Your answer: {user_answer}\n   Correct: {correct_answer}\n\n")
        
        details_text.config(state=tk.DISABLED)
        
        # Close button
        close_btn = tk.Button(results_window, text="Close", command=results_window.destroy,
                             bg="#0066cc", fg="white", font=("Arial", 10, "bold"),
                             padx=20, pady=10)
        close_btn.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleQuizGUI(root)
    root.mainloop()
