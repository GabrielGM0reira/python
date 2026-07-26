import requests
from bs4 import BeautifulSoup
import csv

url = 'https://books.toscrape.com/'
response = requests.get(url)

print(response.status_code)  # Verifica se a requisição foi bem-sucedida (200)")
print(response.text)  # Imprime o conteúdo HTML da página

soup = BeautifulSoup(response.text, 'html.parser')
books = soup.find_all('article', class_='product_pod')

for book in books:
    title = book.h3.a['title']
    price = book.find('p', class_='price_color').text
    print(f'Título: {title}, Preço: {price}')
    
with open('books.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Título', 'Preço'])  # Escreve o cabeçalho do CSV
    for book in books:
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text
        writer.writerow([title, price])  # Escreve os dados de cada livro no CSV