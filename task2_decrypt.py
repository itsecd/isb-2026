"""
Задание 2: Дешифровка текста из 17 варианта с помощью частотного анализа

Изменения:
- Добавлены докстринги
- Добавлены недостающие файлы (frequencies.txt, found_key.txt)
- Текст шифра вынесен в отдельный файл
- Убраны эмодзи
- Исправлен вывод таблицы частот
"""

from utils import RUS_ALPHABET, REFERENCE_SORTED, write_file, read_file
from utils import calculate_frequencies, print_frequencies

def get_unique_symbols(text: str) -> list:
    """
    Возвращает множество уникальных символов в тексте.
    
    Args:
        text: Входной текст
        
    Returns:
        Отсортированный список уникальных символов
    """
    return sorted(set(text))

def apply_substitution(text: str, substitution: dict) -> str:
    """
    Применяет подстановку к тексту.
    
    Args:
        text: Исходный текст
        substitution: Словарь замен {символ: буква}
        
    Returns:
        Текст с примененными заменами
    """
    result = []
    for char in text:
        if char in substitution:
            result.append(substitution[char])
        else:
            result.append(char)
    return ''.join(result)

def save_frequencies(freq_dict: dict, filename: str) -> None:
    """
    Сохраняет таблицу частот в файл.
    
    Args:
        freq_dict: Словарь частот
        filename: Путь для сохранения
    """
    lines = ["ЧАСТОТЫ СИМВОЛОВ В ЗАШИФРОВАННОМ ТЕКСТЕ:"]
    for char, freq in sorted(freq_dict.items(), key=lambda x: x[1], reverse=True):
        char_display = 'ПРОБЕЛ' if char == ' ' else char
        lines.append(f"{char_display}: {freq:.6f}")
    write_file(filename, '\n'.join(lines))

def save_key(key: dict, filename: str) -> None:
    """
    Сохраняет найденный ключ в файл.
    
    Args:
        key: Словарь замен
        filename: Путь для сохранения
    """
    lines = ["НАЙДЕННЫЙ КЛЮЧ ШИФРОВАНИЯ:",
             "Символ шифра -> Буква русского алфавита",
             "-" * 40]
    
    for cipher_char, plain_char in sorted(key.items()):
        cipher_display = 'ПРОБЕЛ' if cipher_char == ' ' else cipher_char
        plain_display = 'ПРОБЕЛ' if plain_char == ' ' else plain_char
        lines.append(f"{cipher_display:6} -> {plain_display}")
    
    write_file(filename, '\n'.join(lines))

def initial_substitution(freq_sorted: list) -> dict:
    """
    Создает начальную подстановку на основе частот.
    
    Args:
        freq_sorted: Список символов по убыванию частоты
        
    Returns:
        Словарь начальных замен
    """
    substitution = {}
    for i, cipher_char in enumerate(freq_sorted):
        if i < len(REFERENCE_SORTED):
            substitution[cipher_char] = REFERENCE_SORTED[i]
        else:
            substitution[cipher_char] = '?'
    return substitution

def main():
    """Основная функция программы."""
    print("=" * 60)
    print("ЗАДАНИЕ 2: ДЕШИФРОВКА ТЕКСТА (ВАРИАНТ 17)")
    print("=" * 60)
    
    # Читаем зашифрованный текст из файла
    cipher_text = read_file("data/task2/original.txt")
    if cipher_text is None:
        print("\nОшибка: файл data/task2/original.txt не найден!")
        return
    
    print(f"\nДлина зашифрованного текста: {len(cipher_text)} символов")
    
    # Показываем уникальные символы
    symbols = get_unique_symbols(cipher_text)
    print(f"Уникальные символы в тексте ({len(symbols)} шт.):")
    print(' '.join(symbols[:20]) + "...")
    
    # Считаем и сохраняем частоты
    freq_dict, sorted_chars = calculate_frequencies(cipher_text)
    print_frequencies(freq_dict, "Частоты символов в зашифрованном тексте")
    save_frequencies(freq_dict, "data/task2/frequencies.txt")
    print(f"Таблица частот сохранена в data/task2/frequencies.txt")
    
    # Создаем начальную подстановку
    substitution = initial_substitution(sorted_chars)
    
    print("\n" + "=" * 60)
    print("ИНСТРУКЦИЯ:")
    print("=" * 60)
    print("1. Смотрите на текст и угадывайте слова")
    print("2. Вводите замены в формате: символ=буква")
    print("   Например: 7=О")
    print("3. После каждой замены текст обновится")
    print("4. Для завершения введите: готово")
    print("=" * 60)
    
    while True:
        print("\n" + "=" * 60)
        print("ТЕКУЩИЙ ТЕКСТ:")
        print("=" * 60)
        print(apply_substitution(cipher_text, substitution))
        print("=" * 60)
        
        if substitution:
            print("\nТЕКУЩИЕ ЗАМЕНЫ:")
            for k, v in list(substitution.items())[:10]:
                print(f"  {k} -> {v if v != ' ' else 'ПРОБЕЛ'}")
        
        cmd = input("\nВведите замену (или 'готово'): ").strip()
        
        if cmd.lower() == 'готово':
            break
        
        if '=' in cmd:
            parts = cmd.split('=')
            if len(parts) == 2:
                cipher_char, plain_char = parts
                cipher_char = cipher_char.strip()
                plain_char = plain_char.strip().upper()
                
                if plain_char in RUS_ALPHABET:
                    substitution[cipher_char] = plain_char
                    print(f"Замена {cipher_char} -> {plain_char} добавлена")
                else:
                    print("Ошибка: буква должна быть из русского алфавита")
            else:
                print("Ошибка: используйте формат символ=буква")
        else:
            print("Ошибка: используйте формат символ=буква")
    
    # Сохраняем результаты
    decrypted = apply_substitution(cipher_text, substitution)
    write_file("data/task2/decrypted.txt", decrypted)
    save_key(substitution, "data/task2/found_key.txt")
    
    print("\n" + "=" * 60)
    print("ГОТОВО!")
    print("=" * 60)
    print("Результаты сохранены в:")
    print("  - data/task2/frequencies.txt")
    print("  - data/task2/decrypted.txt")
    print("  - data/task2/found_key.txt")

if __name__ == "__main__":
    main()