import json
import random
import threading
from pathlib import Path
from leaderboard_db import (
    initialize_database, save_score, get_leaderboard, 
    get_player_stats, get_player_history, get_ranking
)

# Load questions from JSON file
def load_questions():
    """Load quiz questions from JSON file"""
    json_file = Path(__file__).parent / "questions.json"
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

quiz_data = load_questions()

# Initialize database
initialize_database()

# Global variable to handle timed input
user_input = None
input_ready = False

def get_input_with_timeout(prompt, timeout=30):
    """Get user input with timeout"""
    global user_input, input_ready
    user_input = None
    input_ready = False
    
    def input_thread():
        global user_input, input_ready
        try:
            user_input = input(prompt)
        except:
            user_input = ""
        input_ready = True
    
    thread = threading.Thread(target=input_thread, daemon=True)
    thread.start()
    thread.join(timeout=timeout)
    
    if not input_ready:
        print(f"\n⏰ Time's up! ({timeout}s)")
        return None
    return user_input

# Welcome screen
print("=" * 60)
print("     🎯 WELCOME TO THE QUIZ GAME 🎯")
print("=" * 60)

# Username input
while True:
    username = input("\n👤 Enter your username (2-20 characters): ").strip()
    if 2 <= len(username) <= 20:
        print(f"✓ Welcome, {username}!")
        break
    else:
        print("❌ Username must be 2-20 characters. Please try again.")

# Menu system
def show_main_menu():
    print("\n" + "=" * 60)
    print("     MAIN MENU")
    print("=" * 60)
    print("1. Play Quiz")
    print("2. View Leaderboard")
    print("3. View My Statistics")
    print("4. Exit Game")
    print("-" * 60)

# Category selector
def select_categories():
    """Let player select specific categories or all categories"""
    print("\n" + "=" * 60)
    print("     SELECT CATEGORIES")
    print("=" * 60)
    
    categories = list(quiz_data["categories"].keys())
    for idx, category in enumerate(categories, 1):
        num_q = len(quiz_data["categories"][category])
        print(f"{idx}. {category} ({num_q} questions)")
    print(f"{len(categories) + 1}. All Categories")
    print("-" * 60)
    
    while True:
        choice = input("Enter category number (or press Enter for all): ").strip()
        
        if not choice:
            return categories
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(categories):
                return [categories[choice_num - 1]]
            elif choice_num == len(categories) + 1:
                return categories
            else:
                print("❌ Invalid choice!")
        except ValueError:
            print("❌ Please enter a number!")

# Difficulty selector
def select_difficulty():
    print("\n" + "=" * 60)
    print("     SELECT DIFFICULTY LEVEL")
    print("=" * 60)
    print("1. EASY   - 10 questions")
    print("2. MEDIUM - 30 questions")
    print("3. HARD   - All available questions")
    print("4. Custom - Specify number of questions")
    print("-" * 60)
    
    while True:
        difficulty_choice = input("\nEnter choice (1, 2, 3, or 4): ").strip()
        
        if difficulty_choice == "1":
            difficulty_name = "EASY"
            num_questions = 10
            break
        elif difficulty_choice == "2":
            difficulty_name = "MEDIUM"
            num_questions = 30
            break
        elif difficulty_choice == "3":
            difficulty_name = "HARD"
            num_questions = None  # Will be set to all available
            break
        elif difficulty_choice == "4":
            try:
                num_questions = int(input("Enter number of questions: "))
                difficulty_name = "CUSTOM"
                break
            except ValueError:
                print("❌ Please enter a valid number!")
        else:
            print("❌ Invalid choice! Please enter 1, 2, 3, or 4.")
    
    return difficulty_name, num_questions

# Settings menu
def show_settings():
    print("\n" + "=" * 60)
    print("     QUIZ SETTINGS")
    print("=" * 60)
    print("1. Enable time limit per question")
    print("2. Disable time limit")
    print("-" * 60)
    
    while True:
        choice = input("Enter choice (1 or 2): ").strip()
        if choice == "1":
            return 30  # 30 seconds timeout
        elif choice == "2":
            return None  # No timeout
        else:
            print("❌ Invalid choice!")

def play_quiz(username):
    """Run the quiz game"""
    selected_categories = select_categories()
    difficulty_name, num_questions_specified = select_difficulty()
    time_limit = show_settings()
    
    # Get questions from selected categories
    all_questions = []
    for category in selected_categories:
        all_questions.extend(quiz_data["categories"][category])
    
    # Shuffle questions
    random.shuffle(all_questions)
    
    # Limit number of questions
    if num_questions_specified:
        questions_list = all_questions[:num_questions_specified]
    else:
        questions_list = all_questions
    
    num_questions = len(questions_list)
    
    print("\n" + "=" * 60)
    print(f"Starting {difficulty_name} Quiz with {num_questions} questions!")
    if time_limit:
        print(f"⏱️  Time limit: {time_limit} seconds per question")
    print("=" * 60 + "\n")
    
    guesses = []
    score = 0
    question_num = 0
    correct_answers = []
    skipped = 0
    
    for question_data in questions_list:
        print('-----------------------------')
        print(f"Question {question_num + 1}/{num_questions}")
        print(question_data["question"])
        
        # Shuffle options and keep track of which is correct
        options_with_labels = list(enumerate(question_data["options"]))
        random.shuffle(options_with_labels)
        
        # Show shuffled options
        shuffled_options = []
        correct_answer_new = None
        for new_idx, (orig_idx, option) in enumerate(options_with_labels):
            label = chr(65 + new_idx)  # A, B, C, D
            print(f"{label}. {option.split('. ', 1)[1]}")
            shuffled_options.append(option)
            # Find which label corresponds to the correct answer
            if question_data["answer"] in option:
                correct_answer_new = label
        
        if time_limit:
            print(f"\n⏱️  Time remaining: {time_limit}s")
        
        if time_limit:
            guess = get_input_with_timeout("Enter (A, B, C, or D): ", timeout=time_limit)
            if guess is None:
                guesses.append("SKIP")
                correct_answers.append(correct_answer_new)
                skipped += 1
                print("⏭️  Skipped!")
                question_num += 1
                continue
        else:
            guess = input("Enter (A, B, C, or D): ")
        
        guess = guess.upper().strip()
        guesses.append(guess)
        correct_answers.append(correct_answer_new)
        
        if guess == correct_answer_new:
            score += 1
            print("✓ CORRECT!")
        else:
            print("✗ WRONG!")
            print(f"Correct answer is: {correct_answer_new}")
        question_num += 1
    
    # Display results
    print('\n' + '=' * 60)
    print("QUIZ COMPLETED - RESULTS")    
    print('=' * 60)
    
    print(f"\nPlayer: {username}")
    print(f"Difficulty: {difficulty_name}")
    print(f"Categories: {', '.join(selected_categories)}")
    print(f"Total Questions: {num_questions}")
    if skipped > 0:
        print(f"Skipped: {skipped}")
    print("\nCorrect Answers: ", end="")
    for answer in correct_answers:
        print(answer, end=" ")
    
    print("\nYour Guesses:     ", end="")
    for guess in guesses:
        print(guess, end=" ")
        
    percentage_score = score / num_questions * 100
    print(f"\n\nYour Score: {score}/{num_questions} ({percentage_score:.1f}%)")
    
    if percentage_score == 100:
        print("🏆 PERFECT SCORE! You're a genius!")
    elif percentage_score >= 80:
        print("🥇 Excellent! Great job!")
    elif percentage_score >= 60:
        print("🥈 Good effort! Keep learning!")
    elif percentage_score >= 40:
        print("🥉 Not bad! Practice more!")
    else:
        print("💪 Keep trying! You'll do better next time!")
    
    # Save score to leaderboard
    save_score(username, score, num_questions, difficulty_name)
    
    # Get player ranking
    ranking = get_ranking(username, difficulty_name)
    print(f"\n📊 Your Ranking in {difficulty_name}: #{ranking}")
    
    return score, num_questions, percentage_score, difficulty_name


def display_leaderboard():
    """Display the global leaderboard"""
    print("\n" + "=" * 60)
    print("     GLOBAL LEADERBOARD")
    print("=" * 60)
    
    print("\n1. Overall Leaderboard")
    print("2. Easy Difficulty Leaderboard")
    print("3. Medium Difficulty Leaderboard")
    print("4. Hard Difficulty Leaderboard")
    print("5. Back to Main Menu")
    print("-" * 60)
    
    choice = input("Enter choice (1-5): ").strip()
    
    if choice == "1":
        difficulty_filter = None
        title = "OVERALL TOP 10 PLAYERS"
    elif choice == "2":
        difficulty_filter = "EASY"
        title = "TOP 10 - EASY DIFFICULTY"
    elif choice == "3":
        difficulty_filter = "MEDIUM"
        title = "TOP 10 - MEDIUM DIFFICULTY"
    elif choice == "4":
        difficulty_filter = "HARD"
        title = "TOP 10 - HARD DIFFICULTY"
    elif choice == "5":
        return
    else:
        print("❌ Invalid choice!")
        return
    
    leaderboard = get_leaderboard(limit=10, difficulty=difficulty_filter)
    
    print("\n" + "=" * 60)
    print(f"     {title}")
    print("=" * 60)
    
    if not leaderboard:
        print("\n📭 No scores recorded yet!")
        return
    
    print(f"\n{'Rank':<6} {'Username':<20} {'Score':<15} {'%':<8} {'Difficulty':<12}")
    print("-" * 60)
    
    for rank, (username_lb, score, total_q, percentage, difficulty, date_played, id) in enumerate(leaderboard, 1):
        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"{rank:2d}."
        print(f"{medal:<6} {username_lb:<20} {score}/{total_q:<12} {percentage:>5.1f}%  {difficulty:<12}")
    
    input("\nPress Enter to continue...")


def display_player_stats(username):
    """Display player statistics"""
    print("\n" + "=" * 60)
    print(f"     PLAYER STATISTICS - {username}")
    print("=" * 60)
    
    stats = get_player_stats(username)
    
    if not stats or stats[0] == 0:
        print("\n📭 No games played yet!")
        input("Press Enter to continue...")
        return
    
    total_plays, avg_score, best_score, best_score_raw, best_total_q = stats
    
    print(f"\nTotal Games Played: {total_plays}")
    print(f"Average Score: {avg_score}%")
    print(f"Best Score: {best_score:.1f}% ({best_score_raw}/{best_total_q})")
    print(f"Overall Ranking: #{get_ranking(username)}")
    
    print("\n" + "-" * 60)
    print("     RECENT GAMES")
    print("-" * 60)
    
    history = get_player_history(username, limit=10)
    print(f"\n{'#':<4} {'Score':<15} {'%':<8} {'Difficulty':<12} {'Date':<15}")
    print("-" * 60)
    
    for idx, (uname, score, total_q, percentage, difficulty, date_played) in enumerate(history, 1):
        print(f"{idx:<4} {score}/{total_q:<12} {percentage:>5.1f}%  {difficulty:<12} {date_played:<15}")
    
    input("\nPress Enter to continue...")


# Main game loop
def main_game_loop():
    """Main game loop"""
    while True:
        show_main_menu()
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            play_quiz(username)
            input("\nPress Enter to continue...")
        elif choice == "2":
            display_leaderboard()
        elif choice == "3":
            display_player_stats(username)
        elif choice == "4":
            print("\n" + "=" * 60)
            print("Thank you for playing! Goodbye! 👋")
            print("=" * 60)
            break
        else:
            print("❌ Invalid choice! Please try again.")


# Start the game
if __name__ == "__main__":
    main_game_loop()
