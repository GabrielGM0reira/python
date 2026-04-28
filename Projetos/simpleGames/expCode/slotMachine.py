import random

def spin_row():
    symbols = ['chery', 'watermelon', 'lemon', 'bell', 'star']

    return [random.choice(symbols) for _ in range(3)]

def print_row(row):
    print('~' * 20)
    print(' | '.join(row))
    print('~' * 20)
                   
def get_payout(row, bet):
    if row[0] == row[1] == row[2]:
        if row[0] == 'cherry':
            return bet * 3
        elif row[0] == 'watermelon':
            return bet * 4
        elif row[0] == 'lemon':
            return bet * 5
        elif row[0] == 'bell':
            return bet * 10
        elif row[0] == 'star':
            return bet * 20
    return 0

def main():
    balance = 100
    
    print('~' * 20)
    print('Welcome to the Slot Machine!')
    print('Symbols: chery watermelon lemon bell star seven')
    print('~' * 20)

    while balance > 0:
        print(f'Current balance: ${balance}')
        
        bet = (input('Enter your bet amount: '))
        
        if not bet.isdigit():
            print('Invalid input. Please enter a numeric value.')
            continue
        
        bet = int(bet)
        
        if bet > balance:
            print('Insufficient balance. Please enter a valid bet amount.')
            continue
        
        if bet <= 0:
            print("bet must be greater than 0")
            continue
        
        balance -= bet
        
        row = spin_row()
        print("Spinning...")
        print_row(row)
        
        payout = get_payout(row, bet)
        
        if payout > 0:
            print(f"YOU WON ${payout}")
        else:
            print("sorry you lost")
            
        balance += payout
        
if __name__ == '__main__':
    main()
    