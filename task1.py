"""Задание 1: шифрование текста квадратом Полибия"""

import config
import os

REVERSE = {v: k for k, v in config.POLYBIUS_SQUARE.items()}

def save_file(name, text):
    """Сохраняет текст в файл"""
    try:
        with open(name, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f'{name} сохранен')
    except:
        print(f'Ошибка сохранения {name}')

def read_file(name):
    """Читает текст из файла"""
    try:
        if not os.path.exists(name):
            print(f'Файл {name} не найден')
            exit()
        with open(name, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        print(f' Ошибка чтения {name}')
        exit()

def encrypt(text):
    """Заменяет буквы на пары цифр по квадрату Полибия"""
    res = ''
    for c in text.upper():
        res += config.POLYBIUS_SQUARE.get(c, c)
    return res

def decrypt(text):
    """Преобразует пары цифр обратно в буквы"""
    res = ''
    i = 0
    while i < len(text):
        if i+1 < len(text) and text[i].isdigit() and text[i+1].isdigit():
            code = text[i:i+2]
            res += REVERSE.get(code, code)
            i += 2
        else:
            res += text[i]
            i += 1
    return res


text = read_file(config.INPUT_FILE)
print(f'Исходный текст: {len(text)} символов')

enc = encrypt(text)
print(f'Зашифровано: {len(enc)} символов')

dec = decrypt(enc)
print(f'Расшифровано: {len(dec)} символов')

if dec == text.upper():
    print('Всё ок')
else:
    print(' Ошибка')

save_file(config.ENCRYPTED_FILE, enc)
save_file(config.DECRYPTED_FILE, dec)

save_file(config.KEY_FILE, config.KEY_DISPLAY)
