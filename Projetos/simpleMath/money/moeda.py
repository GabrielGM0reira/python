def metade(num=0.0, formato=False):
    res = num / 2
    return res if not formato else moeda(res)

def dobro(num=0.0, formato=False):
    res = num * 2
    return res if not formato else moeda(res)

def aumentar(num=0.0, taxa=0, formato=False):
    res = ((num * taxa) / 100) + num
    return res if formato is False else moeda(res)

def diminuir(num=0.0, taxa=0, formato=False):
    res = num - ((num * taxa) / 100)
    return res if formato is False else moeda(res)

def moeda(num=0.0, moeda='R$'):
    return f'{moeda}{num}'.replace('.', ',')

def resumo(num= 0, taxas= 10, taxar= 15):
    print("~" * 30)
    print("Resumo do valor".center(30))
    print("~" * 30)
    print(f"Preco analizado: {moeda(num)}")
    print(f"Dobro do Preco: {dobro(num, True)}")
    print(f"Metaade Preco: {metade(num, True)}")
    print(f"{taxas}% de aumento: {aumentar(num,taxas, True)}")
    print(f"{taxar}% de reducao: {diminuir(num, taxar, True)}")
    print("~" * 30)