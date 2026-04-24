
principle = 0
rate = 0
time = 0

while True:
    principle = float(input("Enter the principle amount: "))
    if principle < 0:
        print("Principle amount must be greater than 0. Please try again.")
    else:
        break

while True:
    rate = float(input("Enter the rate of interest: "))
    if rate < 0:
        print("Rate of interest must be greater than 0. Please try again.")
    else:
        break
    
while True:
    time = float(input("Enter the time period: "))
    if time < 0:
        print("Time period must be greater than 0. Please try again.")
    else:
        break

total = principle * (1 + (rate / 100) * time)
print(f"The total amount after {time} years is: {total:.2f}") 

