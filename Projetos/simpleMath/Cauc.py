def soma(x, y):
    return x + y

def subt(x, y):
    return x - y

def mult(x, y):
    return x * y
    
def divi(x, y):
    return x / y

def resto(x, y):
    return x % y

print("Selecione operação: \n"
      "1.Soma"
      "2.Subtção\n"
      "3.Multiplição\n"
      "4.Divisão\n"
      "5.Resto Da Divisão"
      )

sel = int(input("Selic=one sua operação (1-5):"))

num1 = int(input("Digite um numero:"))
num2 = int(input("Digite um numero"))

if sel == 1:
    print({num1}, "+", {num2}, "=", soma(num1, num2))
elif sel == 2:
    print({num1}, "-", {num2}, "=", subt(num1, num2))
elif sel == 3:
    print({num1}, "*", {num2}, "=", mult(num1, num2))
elif sel == 4:
    try:
        print({num1}, "/", {num2}, "=", divi(num1, num2))
    except ZeroDivisionError:
        print("Erro não divida por zero")
elif sel == 5:
    print({num1}, "%", {num2}, "=", resto(num1, num2))
else:
    print("digete um numero correto")
