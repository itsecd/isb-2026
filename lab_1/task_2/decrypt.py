#!/usr/bin/env python3
"""
Расшифровка текста с известным ключом.
"""

import os


KEY_FILE = 'key.txt'

def read_key(key_file: str) -> dict[str, str]:
    """Читает файл с ключом и создаёт словарь подстановки.

    Формат ключа: пары символов (символ шифра + расшифровка) без разделителей.
    Пример: '!р$ю' → {'!': 'р', '$': 'ю'}.

    Args:
        key_file (str): Путь к файлу с ключом.

    Returns:
        dict[str, str]: Словарь расшифровки (шифр → оригинал).

    Raises:
        FileNotFoundError: Если файл с ключом не найден.
    """
    with open(key_file, 'r', encoding='utf-8') as f:
        key = f.read().strip()

    substitution = {}
    for i in range(0, len(key) - 1, 2):
        cipher = key[i]
        plain = key[i + 1]
        substitution[cipher] = plain
    return substitution

key=read_key(KEY_FILE)

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



print()
print("Сохранено в results/decrypted.txt ")
