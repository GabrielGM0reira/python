menu = {'pizza': 8.5, 
        'nachos': 7.0, 
        'popcorn': 6.5,
        'fries': 3.5,
        'chips': 2.5,
        'pretzel': 4.0,
        'soda': 2.5,
        'lemonade': 2.0
        }

cart = []
total = 0

print('~~Welcome to the Snack Bar!~~')
for key, value in menu.items():
    print(f"{key:10}: ${value:.2f}")  
print('~' * 30)

while True:
    food = input('What would you like to order? (type "q" to finish) ').lower()
    if food == 'q':
        break
    elif menu.get(food) is not None:
        cart.append(food)
       
print("\n--- Your Order ---")
for food in cart:
   total += menu.get(food)
   print(food, end=' ')

print()
print(f"\nTotal: ${total:.2f}")