import random
import string

chars = ' ' + string.ascii_letters + string.digits + string.punctuation
chars = list(chars)
key = chars.copy()

random.shuffle(key)

#encrypt

p_text = input('Enter the password or massage to encrypt: ')
c_text = ''

for l in p_text:
    index = chars.index(l)
    c_text += key[index]
    
print(f'original text: {p_text}')
print(f'encrypted text: {c_text}')

#decrypt

c_text = input('Enter encrypt text: ')
p_text = ''

for l in c_text:
    index = key.index(l)
    p_text += chars[index]
    
print(f'encrypted text: {c_text}')
print(f'original text: {p_text}')