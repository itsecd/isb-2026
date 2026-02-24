import sys
import json
from collections import Counter

def read_file(file_path):
    """Читает содержимое файла с обработкой ошибок."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Ошибка: файл '{file_path}' не найден.")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при чтении файла '{file_path}': {e}")
        sys.exit(1)

def read_key(file_path):
    """Читает JSON-файл с ключом дешифровки."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
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
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"Ошибка при записи в файл '{file_path}': {e}")
        sys.exit(1)

def write_frequencies(file_path, freq_dict):
    """
    Записывает словарь частот в файл построчно в формате:
    символ: частота
    Для непечатных символов используется repr.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            for ch, freq in freq_dict.items():                
                f.write(f"{repr(ch)}: {freq:.6f}\n")
    except Exception as e:
        print(f"Ошибка при записи частот в файл '{file_path}': {e}")
        sys.exit(1)

def main():
    if len(sys.argv) != 5:
        print("Использование: python decrypt.py <cipher_file> <key_file> <output_decrypted> <output_freq>")
        print("Пример: python decrypt.py cipher.txt key.json decrypted.txt freq.txt")
        sys.exit(1)

    cipher_file = sys.argv[1]
    key_file = sys.argv[2]
    out_decrypted = sys.argv[3]
    out_freq = sys.argv[4]

    cipher_text = read_file(cipher_file)
    key_map = read_key(key_file)

    freq = count_frequencies(cipher_text)
    print("Относительные частоты символов в шифротексте:")
    for ch, f in sorted(freq.items(), key=lambda x: x[1], reverse=True):
        print(f"{repr(ch)}: {f:.6f}")

    decrypted = decrypt(cipher_text, key_map)

    write_file(out_decrypted, decrypted)
    write_frequencies(out_freq, freq)

    print(f"\nРезультаты сохранены:\n- Расшифрованный текст: {out_decrypted}\n- Частоты: {out_freq}")

if __name__ == "__main__":
    main()
