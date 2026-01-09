from interface import cabe
from interface import linha

def arquivoexiste(nome):
    try:
        a = open(nome, 'rt')
        a.close()
    except FileNotFoundError:
        return False
    else:
        return True
    
def criararquivo(nome):
    try:
        a = open(nome, 'wt+')
        a.close()
    except:
        print('Houve um Erro na crição  do arquivo: ')
    else:
         print(f'Arquivo {nome} criado com sucesso ')
        
def lerarquivo(nome):
    try:
        a = open(nome, 'rt')
    except:
        print('Erro ao ler arquivo')
    else:
        cabe('pessoas cadastradas')
        for linha in a:
            dado = linha.split(';')
            dado[1] = dado[1].replace('\n', '')
            print(f'{dado[0]:<30}{dado[1]:>} anos')
    finally:
        a.close()
    
def cadastrar(arq, nome= 'desconhecido', idade=0):
    try:
        a = open(arq, 'at')
    except:
        print("Houve um erro na abertura do arquivo")
    else:
        try:
            a.write(f'{nome}; {idade}\n')
        except:
            print("Houve um erro ao escrever o arquivo")
        else:
            print(f"Novo registro de {nome} adicionado")  
            a.close()          
    