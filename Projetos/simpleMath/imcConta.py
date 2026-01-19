peso = float(input("Digite seu peso em kg: "))
altura = float(input("Digite sua altura em metros: "))
imc = peso / (altura ** 2)
if imc < 18.5:
    print(f"Seu IMC é {imc:.2f}. Você está abaixo do peso.")
elif 18.5 <= imc < 25:
    print(f"Seu IMC é {imc:.2f}. Você está com peso normal.")
elif 25 <= imc < 30:
    print(f"Seu IMC é {imc:.2f}. Você está com sobrepeso.")
elif 30 <= imc < 40:
    print(f"Seu IMC é {imc:.2f}. Você está obeso.")
else:
    print(f"Seu IMC é {imc:.2f}. Você está com obesidade mórbida.")