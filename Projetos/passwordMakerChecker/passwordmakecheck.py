import string
import random
import re

def validate(password):
    while True:
        if re.search('[0-9]',password) is None:
            print("Make sure your password has a number in it")
        elif re.search('[A-Z]',password) is None: 
            print("Make sure your password has a capital letter in it")
        elif re.search('[#?!@$%^&*-]',password)is None: 
            print("Make sure your password has a special character in it")
        else:
            print("Your password seems fine")
        break
        
# Getting password length
while(True):
    length = int(input("Enter password length: "))
    if length < 6:
        print("Password length should be at least 6")
        continue
    break
print('''Choose character set for password from these:  1. Digits
        2. Letters
        3. Special characters
        4. Exit''')
        
characterList = ""

# Getting character set for password
while(True):
    choice = int(input("Pick a number "))
    if(choice == 1):
            # Adding letters to possible characters
            characterList += string.ascii_letters
    elif(choice == 2):
            # Adding digits to possible characters
            characterList += string.digits
    elif(choice == 3):
            # Adding special characters to possible
            # characters
            characterList += string.punctuation
    elif(choice == 4):
            break
    else:
        print("Please pick a valid option!")
   
password = []

for i in range(length):
    # Picking a random character from our # character list
    randomchar = random.choice(characterList)
    # appending a random character to password
    password.append(randomchar)

# printing password as a string
print("The random password is " + "".join(password))
validate(''.join(password))

        