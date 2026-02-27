"""
Программа для расшифровки текста с подсчетом статистики символов
"""

import json
from collections import Counter

def read_file(filename):
    """Читает файл"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print("Файл не найден")
        return None
    except:
        print("Ошибка при чтении файла")
        return None

def write_file(filename, text):
    """Записывает файл"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
        print("Готово! Результат в файле", filename)
    except:
        print("Ошибка при записи файла")

def count_symbols(text):
    """Подсчитывает статистику символов в тексте"""
    counter = Counter(text)
    total = len(text)
    
    stats = []
    for char, count in counter.most_common():
        freq = count / total
        if char == ' ':
            display = 'ПРОБЕЛ'
        elif char == '\n':
            display = 'ПЕРЕВОД СТРОКИ'
        else:
            display = char
        stats.append((display, count, freq))
    
    return stats, total

def save_stats(stats, total, filename):
    """Сохраняет статистику в файл"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("СТАТИСТИКА СИМВОЛОВ В ТЕКСТЕ\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Всего символов: {total}\n")
        f.write(f"Уникальных символов: {len(stats)}\n\n")
        f.write("Символ | Кол-во | Частота\n")
        f.write("-" * 30 + "\n")
        
        for char, count, freq in stats:
            f.write(f"{char:8} | {count:6} | {freq:.4f}\n")

def decrypt_text(text, key):
    """Расшифровывает текст"""
    result = ""
    unknown = set()
    
    for c in text:
        if c in key:
            result += key[c]
        else:
            result += c
            if c not in ' \n\r\t':
                unknown.add(c)
    
    if unknown:
        print("\nСимволы не найденные в ключе:", unknown)
    
    return result

def print_stats(stats, total, n=15):
    """Выводит статистику на экран"""
    print(f"\nВсего символов: {total}")
    print(f"Уникальных символов: {len(stats)}")
    print("\nТоп-{} самых частых символов:".format(n))
    print("-" * 40)
    print("  №  | Символ | Кол-во | Частота")
    print("-" * 40)
    
    for i, (char, count, freq) in enumerate(stats[:n]):
        print(f"  {i+1:2d} | {char:7} | {count:6} | {freq:.4f}")

def main():
    print("=" * 50)
    print("РАСШИФРОВКА ТЕКСТА")
    print("=" * 50)
    
    # Ввод названий файлов
    text_file = input("Файл с зашифрованным текстом: ").strip()
    key_file = input("Файл с ключом: ").strip()
    out_file = input("Файл для результата: ").strip()
    
    if not all([text_file, key_file, out_file]):
        print("Ошибка: нужно заполнить все поля")
        return
    
    # Читаем зашифрованный текст
    print("\nЧитаем файл с текстом...")
    text = read_file(text_file)
    if text is None:
        return
    
    # Считаем статистику исходного текста
    stats, total = count_symbols(text)
    print_stats(stats, total)
    
    # Сохраняем статистику
    save_stats(stats, total, "stats_original.txt")
    print("\nСтатистика сохранена в stats_original.txt")
    
    # Читаем ключ
    print("\nЧитаем файл с ключом...")
    key_data = read_file(key_file)
    if key_data is None:
        return
    
    # Загружаем ключ
    try:
        key = json.loads(key_data)
        print(f"Ключ загружен, {len(key)} соответствий")
    except:
        print("Ошибка: неверный формат ключа")
        return
    
    # Расшифровываем
    print("\nРасшифровываем...")
    result = decrypt_text(text, key)
    
    # Считаем статистику расшифрованного текста
    result_stats, result_total = count_symbols(result)
    
    # Сохраняем результат
    write_file(out_file, result)
    
    # Сохраняем статистику результата
    save_stats(result_stats, result_total, "stats_decrypted.txt")
    print("Статистика результата в stats_decrypted.txt")
    
    # Показываем результат
    print("\n" + "=" * 50)
    print("РЕЗУЛЬТАТ (первые 300 символов):")
    print("=" * 50)
    print(result[:300])
    
    print("\nГотово! Файлы созданы:")
    print(f"  - {out_file} (расшифрованный текст)")
    print("  - stats_original.txt (статистика исходного текста)")
    print("  - stats_decrypted.txt (статистика результата)")

if __name__ == "__main__":
    main()