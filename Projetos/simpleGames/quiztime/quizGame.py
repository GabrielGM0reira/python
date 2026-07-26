import json
import random
import threading
from pathlib import Path
from leaderboard_db import (
    initialize_database, save_score, get_leaderboard, 
    get_player_stats, get_player_history, get_ranking,
    get_current_season, get_seasonal_stats, get_all_seasons
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
    print("     SELECT QUIZ MODE")
    print("=" * 60)
    print("1. EASY   - 10 questions")
    print("2. MEDIUM - 30 questions")
    print("3. HARD   - All available questions")
    print("4. Custom - Specify number of questions")
    print("5. Study Mode - Practice with explanations")
    print("-" * 60)
    
    while True:
        difficulty_choice = input("\nEnter choice (1, 2, 3, 4, or 5): ").strip()
        
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
        elif difficulty_choice == "5":
            difficulty_name = "STUDY"
            num_questions = 10  # Default to 10 for study mode
            break
        else:
            print("❌ Invalid choice! Please enter 1, 2, 3, 4, or 5.")
    
    return difficulty_name, num_questions

# Question difficulty tier selector
def select_question_difficulty():
    """Let player select question difficulty tiers"""
    print("\n" + "=" * 60)
    print("     SELECT QUESTION DIFFICULTY TIER")
    print("=" * 60)
    print("1. Easy Questions Only")
    print("2. Medium Questions Only")
    print("3. Hard Questions Only")
    print("4. Mixed (All difficulties)")
    print("-" * 60)
    
    while True:
        choice = input("Enter choice (1-4): ").strip()
        
        if choice == "1":
            return ["Easy"]
        elif choice == "2":
            return ["Medium"]
        elif choice == "3":
            return ["Hard"]
        elif choice == "4":
            return ["Easy", "Medium", "Hard"]
        else:
            print("❌ Invalid choice!")

# Progress bar function
def create_progress_bar(current, total, width=40):
    """Create a visual progress bar"""
    percentage = current / total
    filled = int(width * percentage)
    bar = "█" * filled + "░" * (width - filled)
    percent_text = f"{percentage * 100:.1f}%"
    return f"[{bar}] {percent_text} ({current}/{total})"

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
    
    # Skip question tier selection and settings for Study Mode
    if difficulty_name == "STUDY":
        question_tiers = ["Easy", "Medium", "Hard"]  # Mixed for study
        time_limit = None  # No time limit for study
    else:
        question_tiers = select_question_difficulty()
        time_limit = show_settings()
    
    # Get questions from selected categories
    all_questions = []
    for category in selected_categories:
        all_questions.extend(quiz_data["categories"][category])
    
    # Filter questions by difficulty tier
    filtered_questions = []
    for q in all_questions:
        if q.get("difficulty") in question_tiers:
            filtered_questions.append(q)
    
    if not filtered_questions:
        print("\n❌ No questions found for selected criteria!")
        return
    
    all_questions = filtered_questions
    
    # Shuffle questions
    random.shuffle(all_questions)
    
    # Limit number of questions
    if num_questions_specified:
        questions_list = all_questions[:num_questions_specified]
    else:
        questions_list = all_questions
    
    num_questions = len(questions_list)
    
    print("\n" + "=" * 60)
    if difficulty_name == "STUDY":
        print(f"📚 Starting STUDY MODE with {num_questions} questions!")
        print("✨ Explanations will be shown after each question")
    else:
        print(f"Starting {difficulty_name} Quiz with {num_questions} questions!")
        if time_limit:
            print(f"⏱️  Time limit: {time_limit} seconds per question")
    print("=" * 60 + "\n")
    
    guesses = []
    score = 0
    question_num = 0
    correct_answers = []
    skipped = 0
    streak = 0
    best_streak = 0
    
    for question_data in questions_list:
        print('\n' + '=' * 60)
        # Display progress bar
        progress = create_progress_bar(question_num, num_questions)
        print(f"📊 Progress: {progress}")
        print(f"🔥 Streak: {streak} | Best Streak: {best_streak}")
        print('=' * 60)
        print(f"\nQuestion {question_num + 1}/{num_questions}")
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
                streak = 0  # Reset streak on skip
                print("⏭️  Skipped! (Streak reset)")
                question_num += 1
                continue
        else:
            guess = input("Enter (A, B, C, or D): ")
        
        guess = guess.upper().strip()
        guesses.append(guess)
        correct_answers.append(correct_answer_new)
        
        if guess == correct_answer_new:
            score += 1
            streak += 1
            if streak > best_streak:
                best_streak = streak
            print(f"✓ CORRECT! 🎉 Streak: {streak}")
        else:
            print("✗ WRONG!")
            print(f"Correct answer is: {correct_answer_new}")
            print(f"Streak ended at: {streak}")
            streak = 0  # Reset streak on wrong answer
        
        # Show explanation in Study Mode
        if difficulty_name == "STUDY" and "explanation" in question_data:
            print(f"\n📚 Explanation: {question_data['explanation']}")
        
        question_num += 1
    
    # Display results
    print('\n' + '=' * 60)
    print("QUIZ COMPLETED - RESULTS")    
    print('=' * 60)
    
    print(f"\nPlayer: {username}")
    print(f"Quiz Mode: {difficulty_name}")
    print(f"Question Difficulty: {', '.join(question_tiers)}")
    print(f"Categories: {', '.join(selected_categories)}")
    print(f"Total Questions: {num_questions}")
    if skipped > 0:
        print(f"Skipped: {skipped}")
    
    print(f"\n🔥 Streak Statistics:")
    print(f"   Best Streak: {best_streak}")
    print(f"   Final Streak: {streak}")
    
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
    
    return score, num_questions, percentage_score, difficulty_name, questions_list, guesses, correct_answers


def show_study_review(questions_list, guesses, correct_answers):
    """Display detailed review of wrong answers with explanations"""
    print("\n" + "=" * 60)
    print("     STUDY MODE - DETAILED REVIEW")
    print("=" * 60)
    
    wrong_count = 0
    reviewed = 0
    
    for i, (question_data, guess, correct) in enumerate(zip(questions_list, guesses, correct_answers)):
        # Show only wrong answers
        if guess != correct and guess != "SKIP":
            wrong_count += 1
            reviewed += 1
            
            print(f"\n{'='*60}")
            print(f"❌ WRONG - Question {i+1}")
            print(f"{'='*60}")
            print(f"\n📝 Question: {question_data['question']}")
            
            # Display the options
            print("\nOptions:")
            for j, option in enumerate(question_data['options']):
                label = chr(65 + j)  # A, B, C, D
                marker = "✓" if label == correct else "✗" if label == guess else " "
                print(f"  {marker} {label}. {option.split('. ', 1)[1]}")
            
            print(f"\n🔴 Your Answer: {guess}")
            print(f"🟢 Correct Answer: {correct}")
            
            # Show explanation
            if "explanation" in question_data:
                print(f"\n📚 Explanation:")
                print(f"   {question_data['explanation']}")
            
            print()
        elif guess == "SKIP" and correct is not None:
            # Count skipped questions
            wrong_count += 1
    
    print("\n" + "=" * 60)
    if wrong_count == 0:
        print("✨ Perfect! No wrong answers to review!")
    else:
        print(f"📊 Review Complete: {reviewed} wrong answer(s) explained")
    print("=" * 60)
    
    input("\nPress Enter to continue...")


def display_leaderboard():
    """Display the global leaderboard with seasonal options"""
    while True:
        print("\n" + "=" * 60)
        print("     LEADERBOARD MENU")
        print("=" * 60)
        
        current_season = get_current_season()
        print(f"\n🌍 Current Season: {current_season}\n")
        
        print("1. Overall Leaderboard (All-Time)")
        print("2. Current Season Leaderboard")
        print("3. Seasonal Archives (View past seasons)")
        print("4. Difficulty-based Leaderboards")
        print("5. Back to Main Menu")
        print("-" * 60)
        
        choice = input("Enter choice (1-5): ").strip()
        
        if choice == "1":
            show_overall_leaderboard()
        elif choice == "2":
            show_seasonal_leaderboard(current_season)
        elif choice == "3":
            show_seasonal_archives()
        elif choice == "4":
            show_difficulty_leaderboards()
        elif choice == "5":
            return
        else:
            print("❌ Invalid choice!")


def show_overall_leaderboard():
    """Display all-time overall leaderboard"""
    print("\n" + "=" * 60)
    print("1. Overall (All difficulties)")
    print("2. Easy Difficulty")
    print("3. Medium Difficulty")
    print("4. Hard Difficulty")
    print("5. Back")
    print("-" * 60)
    
    choice = input("Enter choice (1-5): ").strip()
    
    difficulty_map = {
        "2": "EASY",
        "3": "MEDIUM",
        "4": "HARD"
    }
    
    difficulty_filter = difficulty_map.get(choice)
    title = f"OVERALL TOP 10 {'- ' + choice if difficulty_filter else ''}"
    
    if choice == "1":
        title = "OVERALL TOP 10 PLAYERS - ALL TIME"
        difficulty_filter = None
    elif choice == "2":
        title = "TOP 10 - EASY DIFFICULTY (ALL TIME)"
        difficulty_filter = "EASY"
    elif choice == "3":
        title = "TOP 10 - MEDIUM DIFFICULTY (ALL TIME)"
        difficulty_filter = "MEDIUM"
    elif choice == "4":
        title = "TOP 10 - HARD DIFFICULTY (ALL TIME)"
        difficulty_filter = "HARD"
    elif choice == "5":
        return
    else:
        print("❌ Invalid choice!")
        return
    
    leaderboard = get_leaderboard(limit=10, difficulty=difficulty_filter, season=None)
    
    print("\n" + "=" * 60)
    print(f"     {title}")
    print("=" * 60)
    
    if not leaderboard:
        print("\n📭 No scores recorded yet!")
        input("Press Enter to continue...")
        return
    
    print(f"\n{'Rank':<6} {'Username':<20} {'Score':<15} {'%':<8} {'Difficulty':<12}")
    print("-" * 60)
    
    for rank, record in enumerate(leaderboard, 1):
        if len(record) == 7:  # Old format without season
            username_lb, score, total_q, percentage, difficulty, date_played, id = record
        else:  # New format with season
            username_lb, score, total_q, percentage, difficulty, date_played, id, season = record
        
        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"{rank:2d}."
        print(f"{medal:<6} {username_lb:<20} {score}/{total_q:<12} {percentage:>5.1f}%  {difficulty:<12}")
    
    input("\nPress Enter to continue...")


def show_seasonal_leaderboard(season):
    """Display leaderboard for a specific season"""
    print("\n" + "=" * 60)
    print("1. Overall (All difficulties)")
    print("2. Easy Difficulty")
    print("3. Medium Difficulty")
    print("4. Hard Difficulty")
    print("5. Back")
    print("-" * 60)
    
    choice = input("Enter choice (1-5): ").strip()
    
    difficulty_map = {
        "2": "EASY",
        "3": "MEDIUM",
        "4": "HARD"
    }
    
    difficulty_filter = difficulty_map.get(choice)
    
    if choice == "1":
        title = f"TOP 10 PLAYERS - {season.upper()}"
        difficulty_filter = None
    elif choice == "2":
        title = f"TOP 10 - EASY ({season.upper()})"
        difficulty_filter = "EASY"
    elif choice == "3":
        title = f"TOP 10 - MEDIUM ({season.upper()})"
        difficulty_filter = "MEDIUM"
    elif choice == "4":
        title = f"TOP 10 - HARD ({season.upper()})"
        difficulty_filter = "HARD"
    elif choice == "5":
        return
    else:
        print("❌ Invalid choice!")
        return
    
    leaderboard = get_leaderboard(limit=10, difficulty=difficulty_filter, season=season)
    
    print("\n" + "=" * 60)
    print(f"     {title}")
    print("=" * 60)
    
    if not leaderboard:
        print(f"\n📭 No scores recorded for {season}!")
        input("Press Enter to continue...")
        return
    
    print(f"\n{'Rank':<6} {'Username':<20} {'Score':<15} {'%':<8} {'Difficulty':<12}")
    print("-" * 60)
    
    for rank, record in enumerate(leaderboard, 1):
        if len(record) == 7:  # Old format without season
            username_lb, score, total_q, percentage, difficulty, date_played, id = record
        else:  # New format with season
            username_lb, score, total_q, percentage, difficulty, date_played, id, season_val = record
        
        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"{rank:2d}."
        print(f"{medal:<6} {username_lb:<20} {score}/{total_q:<12} {percentage:>5.1f}%  {difficulty:<12}")
    
    input("\nPress Enter to continue...")


def show_seasonal_archives():
    """Display leaderboards for past seasons"""
    seasons = get_all_seasons()
    
    if not seasons:
        print("\n📭 No seasonal data available!")
        input("Press Enter to continue...")
        return
    
    print("\n" + "=" * 60)
    print("     SEASONAL ARCHIVES")
    print("=" * 60)
    print("\nAvailable Seasons:\n")
    
    for idx, season in enumerate(seasons, 1):
        print(f"{idx}. {season}")
    
    print(f"{len(seasons) + 1}. Back")
    print("-" * 60)
    
    choice = input("Select a season: ").strip()
    
    try:
        choice_num = int(choice)
        if 1 <= choice_num <= len(seasons):
            selected_season = seasons[choice_num - 1]
            show_seasonal_leaderboard(selected_season)
        elif choice_num == len(seasons) + 1:
            return
        else:
            print("❌ Invalid choice!")
    except ValueError:
        print("❌ Please enter a number!")


def show_difficulty_leaderboards():
    """Display difficulty-based leaderboards"""
    print("\n" + "=" * 60)
    print("     DIFFICULTY-BASED LEADERBOARDS")
    print("=" * 60)
    
    print("\n1. Easy (All-Time)")
    print("2. Medium (All-Time)")
    print("3. Hard (All-Time)")
    print("4. Easy (Current Season)")
    print("5. Medium (Current Season)")
    print("6. Hard (Current Season)")
    print("7. Back")
    print("-" * 60)
    
    current_season = get_current_season()
    choice = input("Enter choice (1-7): ").strip()
    
    if choice == "1":
        show_overall_leaderboard_difficulty("EASY", None)
    elif choice == "2":
        show_overall_leaderboard_difficulty("MEDIUM", None)
    elif choice == "3":
        show_overall_leaderboard_difficulty("HARD", None)
    elif choice == "4":
        show_overall_leaderboard_difficulty("EASY", current_season)
    elif choice == "5":
        show_overall_leaderboard_difficulty("MEDIUM", current_season)
    elif choice == "6":
        show_overall_leaderboard_difficulty("HARD", current_season)
    elif choice == "7":
        return
    else:
        print("❌ Invalid choice!")


def show_overall_leaderboard_difficulty(difficulty, season=None):
    """Helper function to display leaderboard by difficulty"""
    season_str = f" - {season.upper()}" if season else " - ALL TIME"
    title = f"TOP 10 - {difficulty}{season_str}"
    
    leaderboard = get_leaderboard(limit=10, difficulty=difficulty, season=season)
    
    print("\n" + "=" * 60)
    print(f"     {title}")
    print("=" * 60)
    
    if not leaderboard:
        print("\n📭 No scores recorded!")
        input("Press Enter to continue...")
        return
    
    print(f"\n{'Rank':<6} {'Username':<20} {'Score':<15} {'%':<8}")
    print("-" * 60)
    
    for rank, record in enumerate(leaderboard, 1):
        if len(record) == 7:  # Old format without season
            username_lb, score, total_q, percentage, difficulty_val, date_played, id = record
        else:  # New format with season
            username_lb, score, total_q, percentage, difficulty_val, date_played, id, season_val = record
        
        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"{rank:2d}."
        print(f"{medal:<6} {username_lb:<20} {score}/{total_q:<12} {percentage:>5.1f}%")
    
    input("\nPress Enter to continue...")


def display_player_stats(username):
    """Display player statistics with seasonal options"""
    while True:
        print("\n" + "=" * 60)
        print(f"     PLAYER STATISTICS - {username}")
        print("=" * 60)
        
        current_season = get_current_season()
        print(f"\n🌍 Current Season: {current_season}\n")
        
        print("1. All-Time Statistics")
        print("2. Current Season Statistics")
        print("3. Past Season Statistics")
        print("4. Recent Games (All-Time)")
        print("5. Recent Games (Current Season)")
        print("6. Back to Main Menu")
        print("-" * 60)
        
        choice = input("Enter choice (1-6): ").strip()
        
        if choice == "1":
            show_alltime_stats(username)
        elif choice == "2":
            show_seasonal_player_stats(username, current_season)
        elif choice == "3":
            show_past_seasonal_stats(username)
        elif choice == "4":
            show_player_history(username)
        elif choice == "5":
            show_player_history(username, season=current_season)
        elif choice == "6":
            return
        else:
            print("❌ Invalid choice!")


def show_alltime_stats(username):
    """Display all-time player statistics"""
    print("\n" + "=" * 60)
    print(f"     ALL-TIME STATISTICS - {username}")
    print("=" * 60)
    
    stats = get_player_stats(username)
    
    if not stats or stats[0] == 0:
        print("\n📭 No games played yet!")
        input("Press Enter to continue...")
        return
    
    total_plays, avg_score, best_score, best_score_raw, best_total_q = stats
    
    print(f"\n📊 Overall Statistics:")
    print(f"   Total Games Played: {total_plays}")
    print(f"   Average Score: {avg_score}%")
    print(f"   Best Score: {best_score:.1f}% ({best_score_raw}/{best_total_q})")
    print(f"   Overall Ranking: #{get_ranking(username)}")
    
    print("\n" + "-" * 60)
    print("     RECENT GAMES (ALL-TIME)")
    print("-" * 60)
    
    history = get_player_history(username, limit=10)
    print(f"\n{'#':<4} {'Score':<15} {'%':<8} {'Difficulty':<12} {'Season':<15} {'Date':<12}")
    print("-" * 80)
    
    for idx, record in enumerate(history, 1):
        if len(record) == 6:  # Old format without season
            uname, score, total_q, percentage, difficulty, date_played = record
            season_val = "N/A"
        else:  # New format with season
            uname, score, total_q, percentage, difficulty, date_played, season_val = record
        
        print(f"{idx:<4} {score}/{total_q:<12} {percentage:>5.1f}%  {difficulty:<12} {season_val:<15} {date_played:<12}")
    
    input("\nPress Enter to continue...")


def show_seasonal_player_stats(username, season):
    """Display seasonal player statistics"""
    print("\n" + "=" * 60)
    print(f"     {season.upper()} STATISTICS - {username}")
    print("=" * 60)
    
    stats = get_seasonal_stats(username, season)
    
    if not stats or stats[0] == 0:
        print(f"\n📭 No games played in {season}!")
        input("Press Enter to continue...")
        return
    
    total_plays, avg_score, best_score, best_score_raw, best_total_q = stats
    
    print(f"\n📊 Season Statistics for {season}:")
    print(f"   Games Played: {total_plays}")
    print(f"   Average Score: {avg_score}%")
    print(f"   Best Score: {best_score:.1f}% ({best_score_raw}/{best_total_q})")
    print(f"   Seasonal Ranking: #{get_ranking(username, season=season)}")
    
    print("\n" + "-" * 60)
    print(f"     RECENT GAMES - {season.upper()}")
    print("-" * 60)
    
    history = get_player_history(username, limit=10, season=season)
    
    if not history:
        print(f"\n📭 No games played in {season}!")
        input("Press Enter to continue...")
        return
    
    print(f"\n{'#':<4} {'Score':<15} {'%':<8} {'Difficulty':<12} {'Date':<12}")
    print("-" * 60)
    
    for idx, record in enumerate(history, 1):
        if len(record) == 6:  # Old format without season
            uname, score, total_q, percentage, difficulty, date_played = record
        else:  # New format with season
            uname, score, total_q, percentage, difficulty, date_played, season_val = record
        
        print(f"{idx:<4} {score}/{total_q:<12} {percentage:>5.1f}%  {difficulty:<12} {date_played:<12}")
    
    input("\nPress Enter to continue...")


def show_past_seasonal_stats(username):
    """Display statistics for past seasons"""
    seasons = get_all_seasons()
    
    if not seasons:
        print("\n📭 No seasonal data available!")
        input("Press Enter to continue...")
        return
    
    print("\n" + "=" * 60)
    print("     SEASONAL ARCHIVES")
    print("=" * 60)
    print("\nAvailable Seasons:\n")
    
    for idx, season in enumerate(seasons, 1):
        print(f"{idx}. {season}")
    
    print(f"{len(seasons) + 1}. Back")
    print("-" * 60)
    
    choice = input("Select a season: ").strip()
    
    try:
        choice_num = int(choice)
        if 1 <= choice_num <= len(seasons):
            selected_season = seasons[choice_num - 1]
            show_seasonal_player_stats(username, selected_season)
        elif choice_num == len(seasons) + 1:
            return
        else:
            print("❌ Invalid choice!")
    except ValueError:
        print("❌ Please enter a number!")


def show_player_history(username, season=None):
    """Display player's recent games"""
    if season:
        title = f"RECENT GAMES - {season.upper()}"
    else:
        title = "RECENT GAMES - ALL TIME"
    
    print("\n" + "=" * 60)
    print(f"     {title}")
    print("=" * 60)
    
    history = get_player_history(username, limit=20, season=season)
    
    if not history:
        if season:
            print(f"\n📭 No games played in {season}!")
        else:
            print("\n📭 No games played yet!")
        input("Press Enter to continue...")
        return
    
    if season:
        print(f"\n{'#':<4} {'Score':<15} {'%':<8} {'Difficulty':<12} {'Date':<12}")
        print("-" * 60)
        
        for idx, record in enumerate(history, 1):
            if len(record) == 6:
                uname, score, total_q, percentage, difficulty, date_played = record
            else:
                uname, score, total_q, percentage, difficulty, date_played, season_val = record
            
            print(f"{idx:<4} {score}/{total_q:<12} {percentage:>5.1f}%  {difficulty:<12} {date_played:<12}")
    else:
        print(f"\n{'#':<4} {'Score':<15} {'%':<8} {'Difficulty':<12} {'Season':<15} {'Date':<12}")
        print("-" * 80)
        
        for idx, record in enumerate(history, 1):
            if len(record) == 6:
                uname, score, total_q, percentage, difficulty, date_played = record
                season_val = "N/A"
            else:
                uname, score, total_q, percentage, difficulty, date_played, season_val = record
            
            print(f"{idx:<4} {score}/{total_q:<12} {percentage:>5.1f}%  {difficulty:<12} {season_val:<15} {date_played:<12}")
    
    input("\nPress Enter to continue...")


# Main game loop
def main_game_loop():
    """Main game loop"""
    while True:
        show_main_menu()
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            result = play_quiz(username)
            if result:
                score, num_questions, percentage_score, difficulty_name, questions_list, guesses, correct_answers = result
                
                # For Study Mode, skip the review prompt (explanations already shown)
                # For other modes, ask if user wants to review
                if difficulty_name != "STUDY":
                    print("\n" + "=" * 60)
                    review_choice = input("Would you like to review your wrong answers? (y/n): ").strip().lower()
                    if review_choice == 'y':
                        show_study_review(questions_list, guesses, correct_answers)
                    else:
                        input("\nPress Enter to continue...")
                else:
                    input("\nPress Enter to continue...")
            else:
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
