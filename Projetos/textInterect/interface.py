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

def linha(tam = 42):
    return '~' * tam
    
def cabe(txt):
    print(linha())
    print(txt.center(42))
    print(linha())
    
def menu(lista):
    cabe('Menu Principal')
    c = 1
    for item in lista:
        print(f'\033[33m{c} - {item}\033[m')
        c += 1
    print(linha())
    opc = leiaint('Sua Opçao: ')
    return opc
    