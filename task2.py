"""Задание 2: дешифровка текста частотным анализом"""

from collections import Counter
import os

def load_file_names(filename):
    """Загружает имена файлов из файла"""
    names = {}
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=')
                names[key] = value
    return names

def load_decryption_key(filename):
    """Загружает ключ дешифровки из файла"""
    key = {}
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                enc, dec = parts
                if enc == 'пробел' or enc == ' ':
                    key[' '] = dec
                elif enc == 'перевод':
                    key['\n'] = dec
                else:
                    key[enc] = dec
    return key

def read_file(filename):
    """Читает текст из файла"""
    try:
        if not os.path.exists(filename):
            print(f'Файл {filename} не найден')
            exit()
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        print(f'Ошибка чтения {filename}')
        exit()

def save_file(filename, content):
    """Сохраняет текст в файл"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f' {filename} сохранен')
    except Exception as e:
        print(f' Ошибка сохранения {filename}: {e}')

def frequency_analysis(text):
    """Анализирует количество символов в тексте"""
    freq = Counter(text)
    total = sum(freq.values())
    sorted_freq = freq.most_common()
    return freq, sorted_freq, total

def save_frequency_report(text, filename):
    """Подсчитывает индекс частоты и сохраняет охраняет отчет о частотном анализе"""
    freq, sorted_freq, total = frequency_analysis(text)
    
    report = 'Частотный анализ зашифрованного текста\n'
    report += f'Всего символов: {total}\n'
    report += f'Уникальных символов: {len(freq)}\n\n'
    report += '15 самых частых символов:\n'
    report += ' № | Символ | Количество | Индекс частоты\n'
    
    for i, (char, count) in enumerate(sorted_freq[:15], 1):
        index = count / total  
        if char == ' ':
            display = 'Пробел'
        elif char == '\n':
            display = 'Перевод'
        else:
            display = f"'{char}'"
        report += f'{i:2} | {display:6} | {count:7} | {index:.6f}\n'
    
    save_file(filename, report)
    print(f' Отчет по частотам сохранен')
    return sorted_freq[:10]

def decrypt_with_key(text, key):
    """Дешифрует текст используя ключ"""
    result = ''
    for char in text:
        result += key.get(char, char)
    return result

def save_key(key, filename):
    """Сохраняет ключ в файл"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('НАЙДЕННЫЙ КЛЮЧ ШИФРОВАНИЯ\n')
            for enc in sorted(key.keys()):
                if enc == ' ':
                    f.write(f'Пробел -> {key[enc]}\n')
                elif enc == '\n':
                    f.write(f'Перевод строки -> {key[enc]}\n')
                else:
                    f.write(f"'{enc}' -> {key[enc]}\n")
        print(f' Ключ сохранен')
    except Exception as e:
        print(f' Ошибка сохранения ключа: {e}')

def main():
    """Основная функция"""
    
    names = load_file_names('file_names.txt')
    encrypted_text = read_file('encrypted_text.txt')
    decryption_key = load_decryption_key('decryption_key.txt')
    
    DECRYPTED_RESULT_FILE = names['DECRYPTED_RESULT_FILE']
    KEY_FOUND_FILE = names['KEY_FOUND_FILE']
    FREQUENCY_FILE = names['FREQUENCY_FILE']
    
    print(f' Зашифрованный текст, {len(encrypted_text)} символов')
    
    top = save_frequency_report(encrypted_text, FREQUENCY_FILE)
    
    print('\n10 самых частых символов:')
    total = len(encrypted_text)
    for i, (char, count) in enumerate(top, 1):
        index = count / total
        if char == ' ':
            print(f'{i}. Пробел: {count} раз, индекс = {index:.6f}')
        elif char == '\n':
            print(f'{i}. Перевод: {count} раз, индекс = {index:.6f}')
        else:
            print(f'{i}. "{char}": {count} раз, индекс = {index:.6f}')
    
    decrypted = decrypt_with_key(encrypted_text, decryption_key)
    
    print('\nРезультат (первые 300 символов):') 
    print(decrypted[:300] + '...')
    
    save_file(DECRYPTED_RESULT_FILE, decrypted)
    save_key(decryption_key, KEY_FOUND_FILE)
    


if __name__ == '__main__':
    main()
