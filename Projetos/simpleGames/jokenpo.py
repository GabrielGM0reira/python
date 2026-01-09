from random import randint
from time import sleep

items = ('rock', 'paper', 'scissors')
pc = randint(0, 2)
print("-=" * 30)
print("Welcome to Jokenpo Game! choose your move:")
print("-=" * 30)
print('''Your options:
0 Rock
1 Paper
2 Scissors''')

player = int(input('Choose your move:'))
print(f'You choosen {items[player]}')
print(f'The computer choosen {items[pc]}')

print("jo")
sleep(1)
print("ken")
sleep(1)
print("po!!!")
sleep(1)

if pc == 0:
    if player == 0:
        print('It is a tie!')
    elif player == 1:
        print('You win!')
    elif player == 2:
        print('Computer wins!')
    else:
        print('Invalid move!')
elif pc == 1:
    if player == 0:
        print('Computer wins!')
    elif player == 1:
        print('It is a tie!')
    elif player == 2:
        print('You win!')
    else:
        print('Invalid move!')
elif pc == 2:
    if player == 0:
        print('You win!')
    elif player == 1:
        print('Computer wins!')
    elif player == 2:
        print('It is a tie!')
    else:
        print('Invalid move!')