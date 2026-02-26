"""Задание 1: шифрование текста квадратом Полибия"""

import os

def load_polybius_key(filename):
    """Загружает квадрат Полибия из файла"""
    polybius = {}
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                code, letter = parts
                if letter == 'пробел':
                    polybius[' '] = code
                else:
                    polybius[letter] = code
    return polybius

def load_file_names(filename):
    """Загружает имена файлов из файла"""
    names = {}
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=')
                names[key] = value
    return names

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
        print(f'Ошибка чтения {name}')
        exit()

def encrypt(text, polybius):
    """Заменяет буквы на пары цифр по квадрату Полибия"""
    res = ''
    for c in text.upper():
        res += polybius.get(c, c)
    return res

def decrypt(text, reverse_polybius):
    """Преобразует пары цифр обратно в буквы"""
    res = ''
    i = 0
    while i < len(text):
        if i+1 < len(text) and text[i].isdigit() and text[i+1].isdigit():
            code = text[i:i+2]
            res += reverse_polybius.get(code, code)
            i += 2
        else:
            res += text[i]
            i += 1
    return res

names = load_file_names('file_names.txt')
POLYBIUS = load_polybius_key('polybius_key.txt')
REVERSE = {v: k for k, v in POLYBIUS.items()}

INPUT_FILE = names['INPUT_FILE']
ENCRYPTED_FILE = names['ENCRYPTED_FILE']
DECRYPTED_FILE = names['DECRYPTED_FILE']
KEY_FILE = names['KEY_FILE']

def save_key_display(polybius, filename):
    """Сохраняет ключ в файл"""
    key_text = ''
    for letter, code in polybius.items():
        key_text += f'{code} {letter}\n'
    save_file(filename, key_text)

def main():
    """Основная функция"""
    text = read_file(INPUT_FILE)
    print(f'Исходный текст: {len(text)} символов')

    enc = encrypt(text, POLYBIUS)
    print(f'Зашифровано: {len(enc)} символов')

    dec = decrypt(enc, REVERSE)
    print(f'Расшифровано: {len(dec)} символов')

    if dec == text.upper():
        print('Всё ок')
    else:
        print('Ошибка')

    save_file(ENCRYPTED_FILE, enc)
    save_file(DECRYPTED_FILE, dec)
    save_key_display(POLYBIUS, KEY_FILE)

if __name__ == '__main__':
    main()
