# task2_final_decrypt.py - Дешифровка варианта 25 с ручным ключом
import json
from collections import Counter

DECRYPT_KEY = {
    'Х': ' ',
    'Е': 'О',
    'Ы': 'Е',
    'Д': 'Н',
    'Ч': 'А',
    't': 'Р',
    '1': 'Л',
    '2': 'М',
    '7': 'Ь',
    'И': 'С',
    'Я': 'З',
    'Щ': 'В',
    '>': 'Ы',
    'К': 'У',
    'Ф': 'Я',
    'w': 'Д',
    'Ъ': 'Г',
    'Ь': 'Ж',
    'Л': 'Ф',
    'М': 'Х',
    'r': 'П',
    'У': 'Ю',
    '4': 'Ц',
    'О': 'Ш',
    '5': 'Ч',
    'П': 'Щ',
    '8': 'Э',
    'Й': 'Т',
    'Б': 'К',
    '-': '-',
    ' ': 'И',
}

def decrypt_text(text, key):
    """Дешифрует текст используя ключ"""
    result = []
    for char in text:
        if char in key:
            result.append(key[char])
        else:
            result.append(char)  # Оставляем как есть если нет в ключе
    return ''.join(result)

def analyze_frequency(text):
    """Анализирует частоту символов"""
    freq = Counter(text)
    total = len(text)
    return {char: count/total for char, count in freq.most_common()}

def main():
    # Читаем зашифрованный текст
    with open('cod25.txt', 'r', encoding='utf-8') as f:
        encrypted = f.read()
    total = len(encrypted)
    print(f"Зашифрованный текст: {len(encrypted)} символов\n")
    
    # Анализируем частоты
    freq = analyze_frequency(encrypted)
    
    # Сохраняем таблицу частот
    with open('frequency_table_task2.txt', 'w', encoding='utf-8') as f:
        f.write("ТАБЛИЦА ЧАСТОТ СИМВОЛОВ ЗАШИФРОВАННОГО ТЕКСТА\n")
        f.write("=" * 70 + "\n")
        f.write(f"{'Символ':<12} {'Частота':<15} {'Процент':<12}\n")
        f.write("-" * 70 + "\n")
        for char, count in freq.items():
            f.write(f"'{char}'          {count:<15.6f} {count*100:<12.2f}%\n")
        f.write("-" * 70 + "\n")
        f.write(f"Всего уникальных символов: {len(freq)}\n")
        f.write(f"Всего символов в тексте: {total}\n")
    
    # Дешифруем
    decrypted = decrypt_text(encrypted, DECRYPT_KEY)
    
    # Сохраняем результаты
    with open('decrypted_task2.txt', 'w', encoding='utf-8') as f:
        f.write(decrypted)
    print("✓ Дешифрованный текст сохранен в decrypted_task2.txt")
    
    with open('found_key_task2.json', 'w', encoding='utf-8') as f:
        json.dump(DECRYPT_KEY, f, ensure_ascii=False, indent=2, sort_keys=True)
    print("✓ Ключ дешифровки сохранен в found_key_task2.json")
    
    print("✓ Таблица частот сохранена в frequency_table_task2.txt")
    
    print("\n" + "=" * 70)
    print("ДЕШИФРОВАННЫЙ ТЕКСТ:")
    print("=" * 70)
    print(decrypted)
    print("=" * 70)

if __name__ == "__main__":
    main()