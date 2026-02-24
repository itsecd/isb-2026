#!/usr/bin/env python3
"""
Частотный анализ для расшифровки текстов.
Простая версия для новичков.
"""

import os
from collections import Counter

# Частоты букв (по убыванию): пробел, О, И, Е, А, Н, Т, С...
FREQ = '_ОИЕАНТСРВМЛДЯКПЗЫЬУЧЖГХФЙЮБЦШЩЭЪ'

# Читаем зашифрованный текст
text = open('cod11.txt', 'r', encoding='utf-8').read()

# Удаляем символы новой строки и пробелы из текста для анализа
clean_text = text.replace('\n', '').replace(' ', '')

# Считаем частоты только по символам шифра
counts = Counter(clean_text).most_common()
total = len(clean_text)

print("=" * 40)
print("ЧАСТОТНЫЙ АНАЛИЗ")
print("=" * 40)
print("Символ     Кол-во   %       Предл.")
print("-" * 40)

for i, (char, count) in enumerate(counts):
    percent = count / total * 100
    suggestion = FREQ[i] if i < len(FREQ) else '?'
    if char == ' ':
        display = '(пробел)'
    elif char == '\n':
        display = '(newline)'
    else:
        display = char
    print(f"{display:<10} {count:<8} {percent:<8.2f} {suggestion}")

print("-" * 40)

# Создаём ключ шифрования
key = {}
for i, (char, _) in enumerate(counts):
    if i < len(FREQ):
        key[char] = FREQ[i]

# Расшифровываем текст (используем исходный text с пробелами и \n)
decrypted = ""
for c in text:
    if c in key:
        decrypted += key[c]
    else:
        decrypted += c

print()
print("=" * 40)
print("АВТОМАТИЧЕСКАЯ РАСШИФРОВКА:")
print("=" * 40)
print(decrypted)
print("=" * 40)


