from interface import cabe, menu, linha, leiaint
from interect import arquivoexiste, criararquivo, lerarquivo, cadastrar

arq = 'parquivo.txt'

if not arquivoexiste(arq):
    criararquivo(arq)

while True:
    respota = menu(['ver pessoas cadastradas', 'casdatar novsa pessoa', 'sair'])
    if respota == 1:
        lerarquivo(arq)
    elif respota == 2:
        cabe('Novo cadastro')
        nome = str(input('Nome:'))
        idade = leiaint('idade: ')
        cadastrar(arq, nome, idade)
    elif respota == 3:
        print("Saindo do progama".center(42))
        print(linha())
        break
    else:
        print(f'\033[31m ERRO! Digite algo valido.\033[m')