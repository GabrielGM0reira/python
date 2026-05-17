from questions import questions, options, answers

# Difficulty selector
print("=" * 50)
print("     🎯 WELCOME TO THE QUIZ GAME 🎯")
print("=" * 50)
print("\nSelect Difficulty Level:")
print("1. EASY   - 10 questions")
print("2. MEDIUM - 30 questions")
print("3. HARD   - All 70 questions")
print("-" * 50)

while True:
    difficulty_choice = input("\nEnter choice (1, 2, or 3): ").strip()
    
    if difficulty_cho65ice == "1":
        num_questions = 10
        difficulty_name = "EASY"
        break
    elif difficulty_choice == "2":
        num_questions = 30
        difficulty_name = "MEDIUM"
        break
    elif difficulty_choice == "3":
        num_questions = 70
        difficulty_name = "HARD"
        break
    else:
        print("Invalid choice! Please enter 1, 2, or 3.")

# Select questions based on difficulty
selected_questions = questions[:num_questions]
selected_options = options[:num_questions]
selected_answers = answers[:num_questions]

print("\n" + "=" * 50)
print(f"Starting {difficulty_name} Quiz with {num_questions} questions!")
print("=" * 50 + "\n")

guesses = []
score = 0
question_num = 0   

for question in selected_questions:
    print('-----------------------------')
    print(f"Question {question_num + 1}/{num_questions}")
    print(question)
    for option in selected_options[question_num]:
        print(option)
        
    guess = input("Enter (A, B, C, or D): ").upper()
    guesses.append(guess)
    if guess == selected_answers[question_num]:
        score += 1
        print("✓ CORRECT!")
    else:
        print("✗ WRONG!")
        print(f"Correct answer is: {selected_answers[question_num]}")
    question_num += 1
    
print('\n' + '=' * 50)
print("RESULTS")    
print('=' * 50)

print(f"\nDifficulty: {difficulty_name}")
print(f"Total Questions: {num_questions}")
print("\nCorrect Answers: ", end="")
for answer in selected_answers:
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