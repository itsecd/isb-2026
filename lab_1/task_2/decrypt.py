#!/usr/bin/env python3
"""
Расшифровка текста с известным ключом.
"""

import os

# Ключ шифрования
key = {
    'Z': ' ',
    'P': 'в',
    'E': 'и',
    '!': 'р',
    'W': 'у',
    'F': 'с',
    'x': 'ы',
    'C': 'а',
    'U': 'п',
    '9': 'о',
    'n': 'т',
    'A': 'н',
    '$': 'ю',
    'S': 'я',
    't': 'ч',
    'I': 'е',
    'O': 'з',
    '>': 'э',
    'h': 'л',
    'K': 'к',
    'L': 'й',
    'V': 'м',
    'B': 'г',
    'M': 'б',
    'Q': 'ё',
    'Y': 'ъ',
    '8': 'щ',
    '-': 'ь',
    '=': 'д',
    'J': 'ж',
    'G': 'х',
    'H': 'ь',
    'R': 'ц',
    '3': 'ф',
    'd': 'ш',
}

# Читаем зашифрованный текст
with open('cod11.txt', 'r', encoding='utf-8') as f:
    encrypted = f.read()

# Расшифровываем
decrypted = ""
for c in encrypted:
    if c in key:
        decrypted += key[c]
    else:
        decrypted += c

# Выводим результат
print("=" * 40)
print("РАСШИФРОВАННЫЙ ТЕКСТ:")
print("=" * 40)
print(decrypted)
print("=" * 40)

# Создаём папку results
if not os.path.exists('results'):
    os.makedirs('results')

# Сохраняем в папку results
with open('results/decrypted.txt', 'w', encoding='utf-8') as f:
    f.write(decrypted)

# Сохраняем ключ
key_text = ""
for symbol, letter in sorted(key.items()):
    key_text += symbol + letter

with open('results/key2.txt', 'w', encoding='utf-8') as f:
    f.write(key_text)

print()
print("Сохранено в results/decrypted.txt и results/key2.txt")
