"""Задание 2: дешифровка текста частотным анализом"""

from collections import Counter
import os

def load_file_names(filename):
    """Загружает имена выходных файлов из конфигурационного файла."""
    names = {}
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    names[key.strip()] = value.strip()
    except FileNotFoundError:
        names = {
            'DECRYPTED_RESULT_FILE': '02_decrypted.txt',
            'KEY_FOUND_FILE': '02_key_found.txt',
            'FREQUENCY_FILE': '02_frequency_analysis.txt'
        }
    return names

def read_file(filename):
    """Читает содержимое файла."""
    try:
        if not os.path.exists(filename):
            return None
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return None

def save_file(filename, content):
    """Сохраняет содержимое в файл."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'{filename} сохранен')
    except:
        pass

def frequency_analysis(text):
    """Выполняет частотный анализ текста."""
    freq = Counter(text)
    total = sum(freq.values())
    sorted_freq = freq.most_common()
    freq_with_index = []
    for char, count in sorted_freq:
        index = count / total
        freq_with_index.append((char, count, index))
    return freq_with_index, total

def save_frequency_report(text, filename):
    """Сохраняет отчет о частотном анализе в файл."""
    freq_with_index, total = frequency_analysis(text)
    lines = []
    lines.append(f'Частотный анализ:')
    lines.append(f'Всего символов: {total}')
    lines.append(f'Уникальных символов: {len(Counter(text))}')
    lines.append('')
    lines.append('Символ | Кол-во | Индекс частоты')
    for char, count, index in freq_with_index:
        if char == ' ':
            display = 'пробел'
        elif char == '\n':
            display = 'перевод'
        else:
            display = char
        lines.append(f'{display:6} | {count:6} | {index:.6f}')
    save_file(filename, '\n'.join(lines))
    return freq_with_index

def load_key(key_file):
    """Загружает ключ дешифровки из файла."""
    key = {}
    try:
        with open(key_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            line = line.rstrip('\n')
            if not line or line.startswith('#'):
                continue
            if line.startswith(' '):
                if len(line) >= 3 and line[1] == ' ':
                    enc = ' '
                    dec = line[2:].strip()
                    if dec == 'пробел':
                        key[enc] = ' '
                    elif dec == 'перевод':
                        key[enc] = '\n'
                    else:
                        key[enc] = dec
                    continue
            parts = line.split()
            if len(parts) >= 2:
                enc = parts[0]
                dec = ' '.join(parts[1:])
                if enc == '\\n':
                    enc = '\n'
                if dec == 'пробел':
                    key[enc] = ' '
                elif dec == 'перевод':
                    key[enc] = '\n'
                else:
                    key[enc] = dec
        return key
    except:
        return {}

def save_key(key, filename):
    """Сохраняет найденный ключ дешифровки в файл."""
    lines = ['ключ шифрования']
    for enc in sorted(key.keys()):
        dec = key[enc]
        if enc == ' ':
            lines.append(f"' ' -> {dec if dec != ' ' else 'пробел'}")
        elif enc == '\n':
            lines.append(f"'\\n' -> {dec if dec != '\n' else 'перевод'}")
        else:
            if dec == ' ':
                lines.append(f"'{enc}' -> пробел")
            elif dec == '\n':
                lines.append(f"'{enc}' -> перевод")
            else:
                lines.append(f"'{enc}' -> {dec}")
    save_file(filename, '\n'.join(lines))

def decrypt(text, key):
    """Дешифрует текст с использованием ключа."""
    result = []
    for char in text:
        if char in key:
            result.append(key[char])
        else:
            result.append(char)
    return ''.join(result)

def main():
    """Основная функция программы."""
    names = load_file_names('file_names.txt')
    encrypted = read_file('02_encrypted.txt')
    if encrypted is None:
        print('Файл 02_encrypted.txt не найден')
        return
    
    freq_file = names.get('FREQUENCY_FILE', '02_frequency_analysis.txt')
    save_frequency_report(encrypted, freq_file)
    
    key = load_key('decryption_key.txt')
    if key:
        decrypted = decrypt(encrypted, key)
        result_file = names.get('DECRYPTED_RESULT_FILE', '02_decrypted.txt')
        save_file(result_file, decrypted)
        key_file = names.get('KEY_FOUND_FILE', '02_key_found.txt')
        save_key(key, key_file)
    else:
        print('Ключ не загружен. Создайте decryption_key.txt')

if __name__ == '__main__':
    main()
