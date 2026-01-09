def leiaint(msg):
    while True:
        try:
            n = int(input(msg))
        except (ValueError, TypeError):
             print(f'\033[31m ERRO! Digite um numero valido.\033[m')
             continue
        except (KeyboardInterrupt):
             print(f'\033[31m Usuario preferiu nao digitar esse numero.\033[m')
             return 0 
        else:
            return n

def leifloat(msg):
    while True:
        try:
            n = float(input(msg))
        except (ValueError, TypeError):
             print(f'\033[31m ERRO! Digite um numero valido.\033[m')
             continue
        except (KeyboardInterrupt):
             print(f'\033[31m Usuario preferiu nao digitar esse numero.\033[m')
             return 0 
        else:
            return n

n1 = leiaint('digite um numero inteiro: ')
n2 = leifloat('digite um numero real: ')
print(f"O numero inteiro foi {n1} e o real {n2}")