while True:
    n = int(input('choose a number'))
    print('-=' * 30)
    if n < 0:
        break
    for c in range(1, 11):
        print(f'{n} x {c:2} = {n * c}')
    print('-=' * 30)
    