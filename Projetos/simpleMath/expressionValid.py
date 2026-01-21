exp = str(input('Enter an expression: '))
pile = []
for sym in exp:
    if sym == '(':
        pile.append(sym)
    elif sym == ')':
        if len(pile) > 0:
            pile.pop()
        else:
            pile.append(')')
            break
if len(pile) == 0:
    print('The expression is correct')
else:
    print('The expression is incorrect')