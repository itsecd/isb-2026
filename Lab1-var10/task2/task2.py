import sys
import json
import os
from collections import Counter

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from constants import ENCODING

def read_file(file_path):
    """Читает содержимое файла, удаляя символы перевода строки."""
    try:
        with open(file_path, 'r', encoding=ENCODING) as f:
            content = f.read()
            return content.replace('\n', '').replace('\r', '')
    except FileNotFoundError:
        print(f"Ошибка: файл '{file_path}' не найден.")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при чтении файла '{file_path}': {e}")
        sys.exit(1)

def read_key(file_path):
    """Читает JSON-файл с ключом дешифровки."""
    try:
        with open(file_path, 'r', encoding=ENCODING) as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Ошибка: файл '{file_path}' не является корректным JSON.")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при чтении ключа: {e}")
        sys.exit(1)

def count_frequencies(text):
    """
    Возвращает словарь относительных частот символов в тексте.
    Ключи — символы, значения — частота (доля от общего числа символов).
    """
    total = len(text)
    if total == 0:
        return {}
    cnt = Counter(text)
    return {ch: count / total for ch, count in cnt.items()}

def decrypt(text, key_map):
    """
    Расшифровывает текст, заменяя символы по словарю key_map.
    Если символа нет в ключе, он остаётся без изменений.
    """
    return ''.join(key_map.get(ch, ch) for ch in text)

def write_file(file_path, content):
    """Записывает содержимое в файл."""
    try:
        with open(file_path, 'w', encoding=ENCODING) as f:
            f.write(content)
    except Exception as e:
        print(f"Ошибка при записи в файл '{file_path}': {e}")
        sys.exit(1)

def write_frequencies(file_path, freq_dict):
    """
    Записывает словарь частот в файл построчно в формате:
    символ: частота
    Сортировка по убыванию частоты.
    Для непечатных символов используется repr.
    """
    try:
        with open(file_path, 'w', encoding=ENCODING) as f:
           
            sorted_items = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)
            for ch, freq in sorted_items:
                f.write(f"{repr(ch)}: {freq:.6f}\n")
    except Exception as e:
        print(f"Ошибка при записи частот в файл '{file_path}': {e}")
        sys.exit(1)

def main():
    if len(sys.argv) != 5:
        print("Использование: python task2.py <cipher_file> <key_file> <output_decrypted> <output_freq>")
        print("Пример: python task2.py cipher.txt key.json decrypted.txt freq.txt")
        sys.exit(1)

    cipher_file = sys.argv[1]
    key_file = sys.argv[2]
    out_decrypted = sys.argv[3]
    out_freq = sys.argv[4]

    cipher_text = read_file(cipher_file)
    key_map = read_key(key_file)

    freq = count_frequencies(cipher_text)
    print("Относительные частоты символов в шифротексте (отсортированы по убыванию):")
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    for ch, f in sorted_freq:
        print(f"{repr(ch)}: {f:.6f}")

    decrypted = decrypt(cipher_text, key_map)

    write_file(out_decrypted, decrypted)
    write_frequencies(out_freq, freq)

    print(f"\nРезультаты сохранены:\n- Расшифрованный текст: {out_decrypted}\n- Частоты: {out_freq}")

if __name__ == '__main__':
    main()
