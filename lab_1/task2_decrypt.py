"""
Модуль для расшифровки текста шифром простой подстановки.
Лабораторная работа №1, Вариант 21

Полный ключ подстановки
"""

import os
from collections import Counter


RESULTS_DIR = 'results'


SUBSTITUTION_KEY = {
    'М': ' ',
    ' ': 'ы',
    'Е': 'о',
    'У': 'и',
    '4': 'а',
    '>': 'е',
    'Д': 'н',
    'И': 'с',
    'Й': 'т',
    'О': 'в',
    't': 'р',
    'Р': 'д',
    '1': 'л',
    'r': 'п',
    'Х': 'к',
    'Л': 'я',
    '2': 'м',
    '8': 'з',
    'А': 'ь',
    'Ч': 'у',
    'Щ': 'х',
    '<': 'ч',
    'К': 'ю',
    'Ф': 'й',
    'Ъ': 'ц',
    'П': 'г',
    'Ш': 'ф',
    '7': 'ж',
    'Ь': 'щ',
    '5': 'б',
    'Ы': 'ш',
    'Э': 'э',
    'Я': 'я',
    'З': 'з',
    'В': 'в',
    'Н': 'н',
    'Т': 'т',
    'С': 'с',
    'Г': 'г',
    'Б': 'б',
    'Ж': 'ж',
    'Ё': 'ё',
    'Ю': 'ю',
    'Ц': 'ц',
}


def ensure_results_dir():
    """Создает папку для результатов."""
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)


def decrypt_text(key: dict, text: str) -> str:
    """Расшифровывает текст, используя ключ подстановки."""
    return "".join(key.get(char, char) for char in text)


def write_file(path: str, text: str) -> None:
    """Записывает текст в файл."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def open_file(path: str) -> str:
    """Считывает содержимое файла."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def get_freq(text: str) -> dict:
    """Вычисляет частоту встречаемости каждого символа."""
    if not text:
        return {}
    
    len_t = len(text)
    char_counts = Counter(text)
    char_freq = {char: count / len_t for char, count in char_counts.items()}
    freq_char = dict(
        sorted(char_freq.items(), key=lambda item: item[1], reverse=True)
    )
    
    return freq_char


def format_frequency_table(freq_dict: dict, key: dict) -> str:
    """Форматирует таблицу частот."""
    output = "ТАБЛИЦА ЧАСТОТ СИМВОЛОВ\n"
    output += "=" * 60 + "\n"
    output += f"{'Символ':<15} {'Частота':<15} {'Расшифровка':<15}\n"
    output += "-" * 60 + "\n"
    
    for char, freq in freq_dict.items():
        display_char = repr(char) if char in ['\n', '\t', ' '] else char
        decrypted = key.get(char, '?')
        decrypted_display = repr(decrypted) if decrypted == ' ' else decrypted
        output += f"{display_char:<15} {freq*100:<15.2f}% {decrypted_display:<15}\n"
    
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
        enc_display = repr(encrypted) if encrypted in ['\n', '\t', ' '] else encrypted
        orig_display = repr(original) if original in ['\n', '\t', ' '] else original
        output += f"{enc_display:<20} {orig_display:<20}\n"
    
    output += "=" * 50 + "\n"
    
    write_file(path, output)


def main() -> None:
    """Основная функция."""
    ensure_results_dir()
    
    print("=" * 70)
    print("ЗАДАНИЕ 2: Расшифровка текста шифром простой подстановки")
    print("Лабораторная работа №1, Вариант 21")
    print("=" * 70)
    
    # Чтение зашифрованного текста
    try:
        encrypted_text = open_file("cod21.txt")
    except FileNotFoundError:
        print(f"\n ОШИБКА: Файл cod21.txt не найден!")
        return
    
    print(f"\n1. ЗАШИФРОВАННЫЙ ТЕКСТ:")
    print("-" * 70)
    print(encrypted_text[:500] + "..." if len(encrypted_text) > 500 else encrypted_text)
    print(f"\nДлина текста: {len(encrypted_text)} символов")
    
    # Частотный анализ
    print("\n2. ЧАСТОТНЫЙ АНАЛИЗ:")
    print("-" * 70)
    freq_dict = get_freq(encrypted_text)
    
    print(f"\n{'Символ':<15} {'Частота':<15} {'Расшифровка':<15}")
    print("-" * 70)
    for char, freq in list(freq_dict.items())[:20]:
        display_char = repr(char) if char in ['\n', '\t', ' '] else char
        decrypted = SUBSTITUTION_KEY.get(char, '?')
        print(f"{display_char:<15} {freq*100:<15.2f}% {decrypted:<15}")
    print("-" * 70)
    
    # Расшифровка
    print("\n3. РАСШИФРОВКА:")
    print("=" * 70)
    decrypted = decrypt_text(SUBSTITUTION_KEY, encrypted_text)
    print(decrypted)
    print("=" * 70)
    
    # Таблица частот
    freq_table = format_frequency_table(freq_dict, SUBSTITUTION_KEY)
    
    # Сохранение результатов
    write_file(f"{RESULTS_DIR}/task2_encrypted.txt", encrypted_text)
    write_file(f"{RESULTS_DIR}/task2_decrypted.txt", decrypted)
    write_file(f"{RESULTS_DIR}/task2_frequency.txt", freq_table)
    save_key_to_file(SUBSTITUTION_KEY, f"{RESULTS_DIR}/task2_key.txt")
    
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