"""Задание 2: дешифровка текста частотным анализом"""

import config
from collections import Counter

def save_file(filename, content):
    """Сохраняет текст в файл"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f' {filename} сохранен')
    except Exception as e:
        print(f' Ошибка сохранения {filename}: {e}')

def frequency_analysis(text):
    """Анализирует частоту символов в тексте"""
    freq = Counter(text)
    total = sum(freq.values())
    sorted_freq = freq.most_common()
    return freq, sorted_freq, total

def save_frequency_report(text, filename):
    """Сохраняет отчет о частотном анализе"""
    freq, sorted_freq, total = frequency_analysis(text)
    
    report = 'ЧАСТОТНЫЙ АНАЛИЗ ЗАШИФРОВАННОГО ТЕКСТА\n'
    report += f'Всего символов: {total}\n'
    report += f'Уникальных символов: {len(freq)}\n\n'
    report += '15 самых частых символов:\n'
    report += '-'*50 + '\n'
    report += ' № | Символ | Частота |   %   \n'
    report += '-'*50 + '\n'
    
    for i, (char, count) in enumerate(sorted_freq[:15], 1):
        percent = (count / total) * 100
        if char == ' ':
            display = 'ПРОБЕЛ'
        elif char == '\n':
            display = 'ПЕРЕВОД'
        else:
            display = f"'{char}'"
        report += f'{i:2} | {display:6} | {count:7} | {percent:6.2f}\n'
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f' Отчет по частотам сохранен')
    return sorted_freq[:10]

def decrypt_with_key(text):
    """Дешифрует текст используя ключ из config"""
    result = ''
    for char in text:
        result += config.DECRYPTION_KEY.get(char, char)
    return result

def save_key(filename):
    """Сохраняет ключ из config в файл"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('НАЙДЕННЫЙ КЛЮЧ ШИФРОВАНИЯ\n')
            f.write('='*50 + '\n\n')
            for enc in sorted(config.DECRYPTION_KEY.keys()):
                if enc == ' ':
                    f.write(f'ПРОБЕЛ -> {config.DECRYPTION_KEY[enc]}\n')
                elif enc == '\n':
                    f.write(f'ПЕРЕВОД СТРОКИ -> {config.DECRYPTION_KEY[enc]}\n')
                else:
                    f.write(f"'{enc}' -> {config.DECRYPTION_KEY[enc]}\n")
        print(f' Ключ сохранен')
    except Exception as e:
        print(f' Ошибка сохранения ключа: {e}')

def main():
    """Основная функция"""
    
    encrypted = config.ENCRYPTED_TEXT
    print(f' Зашифрованный текст, {len(encrypted)} символов')
    
    top = save_frequency_report(encrypted, config.FREQUENCY_FILE)
    
    print('\n10 самых частых символов:')
    for i, (char, count) in enumerate(top, 1):
        if char == ' ':
            print(f'{i}. ПРОБЕЛ: {count} раз')
        elif char == '\n':
            print(f'{i}. ПЕРЕВОД: {count} раз')
        else:
            print(f'{i}. "{char}": {count} раз')
    
    decrypted = decrypt_with_key(encrypted)
    
    print('Результат (первые 300 символов):')
    print(decrypted[:300] + '...')
    
    save_file(config.DECRYPTED_RESULT_FILE, decrypted)
    save_key(config.KEY_FOUND_FILE)
    
    print(f'Файлы: {config.ENCRYPTED_VARIANT_FILE}, {config.DECRYPTED_RESULT_FILE}, {config.KEY_FOUND_FILE}, {config.FREQUENCY_FILE}')

if __name__ == '__main__':
    main()