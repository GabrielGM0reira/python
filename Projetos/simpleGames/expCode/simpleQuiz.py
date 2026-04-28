questions = ("how many elements are in the periodic table?",
             "which animal lays eggs?",
             "whatt is the most abundant gas in the earth's atmosphere?",
             "how many bones re in the human body?",
             "which planet in the solar is the hottest?")

options = (("A.116", "B.117", "C.118", "D.119"),
            ("A. whale", "B. Crocodile", "C. Elephant", "D. Ostrich"),           
            ("A. Nitrogen", "B. Oxygen", "C. Carbon Dioxide", "D. Hydrogen"),
            ("A. 206", "B. 207", "C. 208", "D. 209"),
            ("A. mercury", "B. venus", "C. earth", "D. mars")
           )

answers = ("C", "D", "A", "A", "B")
guesses = []
score = 0
question_num = 0   

for question in questions:
    print('-----------------------------')
    print(question)
    for option in options[question_num]:
        print(option)
        
    guess = input("Enter (A, B, C, or D): ").upper()
    guesses.append(guess)
    if guess == answers[question_num]:
        score += 1
        print("CORRECT!")
    else:
        print("WRONG!")
        print(f"Correct answer is: {answers[question_num]}")
    question_num += 1
    
print('-----------------------------')
print("RESULTS")    
print('-----------------------------')

print("Answers: ", end="")
for answer in answers:
    print(answer, end=" ")

print("Guesses: ", end="")
for guess in guesses:
    print(guess, end=" ")
    
score = score / len(questions) * 100
print(f"\nYour score is: {score}%")