"""
Модуль для расшифровки текста шифром простой подстановки.
Лабораторная работа №1, Вариант 21
"""

import os
from frequency_analyzer import FrequencyAnalyzer


RESULTS_DIR = 'results'


def load_key_from_file(key_file: str = 'key2.txt') -> dict:
    """Загружает ключ подстановки из файла."""
    key = {}
    
    try:
        with open(key_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for line in lines:
            line = line.strip()
            if not line or line.startswith('=') or line.startswith('КЛЮЧ'):
                continue
            
            if '→' in line:
                parts = line.split('→')
                if len(parts) == 2:
                    encrypted = parts[0].strip()
                    original = parts[1].strip()
                    
                    # Обрабатываем пробелы правильно
                    if encrypted == '':
                        encrypted = ' '
                    if original == '':
                        original = ' '
                    
                    if len(encrypted) == 1:
                        key[encrypted] = original
                    
    except FileNotFoundError:
        print(f" Файл {key_file} не найден!")
        return {}
    
    return key


def ensure_results_dir():
    """Создает папку для результатов."""
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)


def decrypt_text(key: dict, text: str) -> str:
    """Расшифровывает текст, используя ключ подстановки."""
    result = []
    for char in text:
        if char in key:
            result.append(key[char])
        else:
            result.append(char)
    return "".join(result)


def write_file(path: str, text: str) -> None:
    """Записывает текст в файл."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def open_file(path: str) -> str:
    """Считывает содержимое файла."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def format_frequency_table(freq_dict: dict, key: dict) -> str:
    """Форматирует таблицу частот."""
    output = "ТАБЛИЦА ЧАСТОТ СИМВОЛОВ\n"
    output += "=" * 60 + "\n"
    output += f"{'Символ':<15} {'Частота':<15} {'Расшифровка':<15}\n"
    output += "-" * 60 + "\n"
    
    for char, freq in freq_dict.items():
        if char == ' ':
            display_char = '(пробел)'
        elif char == '\n':
            display_char = '(newline)'
        else:
            display_char = char
        decrypted = key.get(char, '?')
        output += f"{display_char:<15} {freq*100:<15.2f}% {decrypted:<15}\n"
    
    output += "=" * 60 + "\n"
    return output


def save_key_to_file(key: dict, path: str) -> None:
    """Сохраняет ключ подстановки в файл."""
    output = "КЛЮЧ ПОДСТАНОВКИ (моноалфавитная замена)\n"
    output += "Лабораторная работа №1, Вариант 21\n"
    output += "=" * 50 + "\n\n"
    output += f"{'Зашифрованный':<20} {'Оригинал':<20}\n"
    output += "-" * 50 + "\n"
    
    for encrypted, original in sorted(key.items()):
        if encrypted == ' ':
            enc_display = '(пробел)'
        else:
            enc_display = encrypted
        output += f"{enc_display:<20} {original:<20}\n"
    
    output += "=" * 50 + "\n"
    
    write_file(path, output)


def main() -> None:
    """Основная функция."""
    ensure_results_dir()
    
    print("=" * 70)
    print("ЗАДАНИЕ 2: Расшифровка текста шифром простой подстановки")
    print("Лабораторная работа №1, Вариант 21")
    print("=" * 70)
    
    # Загрузка ключа из файла
    print("\n1. ЗАГРУЗКА КЛЮЧА ИЗ ФАЙЛА key2.txt:")
    print("-" * 70)
    key = load_key_from_file('key2.txt')
    print(f"Загружено {len(key)} соответствий")
    
    if not key:
        print(" Ошибка загрузки ключа!")
        return
    
    # Чтение зашифрованного текста
    try:
        encrypted_text = open_file("cod21.txt")
    except FileNotFoundError:
        print(f"\n ОШИБКА: Файл cod21.txt не найден!")
        return
    
    print(f"\n2. ЗАШИФРОВАННЫЙ ТЕКСТ:")
    print("-" * 70)
    print(encrypted_text[:500] + "..." if len(encrypted_text) > 500 else encrypted_text)
    print(f"\nДлина текста: {len(encrypted_text)} символов")
    
    # Частотный анализ
    print("\n3. ЧАСТОТНЫЙ АНАЛИЗ:")
    print("-" * 70)
    analyzer = FrequencyAnalyzer()
    freq_dict = analyzer.analyze(encrypted_text)
    
    print(f"\n{'Символ':<15} {'Частота':<15} {'Расшифровка':<15}")
    print("-" * 70)
    for char, freq in list(freq_dict.items())[:20]:
        if char == ' ':
            display_char = '(пробел)'
        else:
            display_char = char
        decrypted = key.get(char, '?')
        print(f"{display_char:<15} {freq:<15.2f}% {decrypted:<15}")
    print("-" * 70)
    
    # Расшифровка
    print("\n4. РАСШИФРОВКА:")
    print("=" * 70)
    decrypted = decrypt_text(key, encrypted_text)
    print(decrypted)
    print("=" * 70)
    
    # Таблица частот
    freq_table = format_frequency_table(freq_dict, key)
    
    # Сохранение результатов
    write_file(f"{RESULTS_DIR}/task2_encrypted.txt", encrypted_text)
    write_file(f"{RESULTS_DIR}/task2_decrypted.txt", decrypted)
    write_file(f"{RESULTS_DIR}/task2_frequency.txt", freq_table)
    save_key_to_file(key, f"{RESULTS_DIR}/task2_key.txt")
    
    print(f"\n Результаты сохранены в папку '{RESULTS_DIR}/'")
    print("\nФайлы:")
    print("  - task2_encrypted.txt")
    print("  - task2_decrypted.txt")
    print("  - task2_key.txt")
    print("  - task2_frequency.txt")
    
    print("\n" + "=" * 70)
    print("ЗАДАНИЕ 2 ВЫПОЛНЕНО")
    print("=" * 70)


if __name__ == "__main__":
    main()