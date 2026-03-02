import re
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from constants import ALPHABET, ENCODING

def preprocess(text):
    """Удаляет всё, кроме русских букв и пробела, переводит в верхний регистр."""
    cleaned = re.sub(r'[^А-Яа-я ]', '', text)
    return cleaned.upper()

def create_maps(key):
    """Создаёт словари для шифрования и дешифрования."""
    if len(key) != len(ALPHABET):
        raise ValueError(f"Ключ должен содержать ровно {len(ALPHABET)} символов.")
    enc_map = dict(zip(ALPHABET, key))
    dec_map = dict(zip(key, ALPHABET))
    return enc_map, dec_map

def substitute(text, mapping):
    """
    Универсальная функция замены символов.
    Применяет к тексту словарь mapping: если символ есть в словаре,
    заменяет его соответствующим значением, иначе оставляет без изменений.
    """
    return ''.join(mapping.get(ch, ch) for ch in text)

def main():
    print("=" * 50)
    print("   Шифрование / дешифрование моноалфавитной заменой")
    print("=" * 50)

    mode = input("Режим (encrypt / decrypt): ").strip().lower()
    if mode not in ('encrypt', 'decrypt'):
        print("Ошибка: выберите encrypt или decrypt.")
        return

    key = input(f"Введите ключ (ровно {len(ALPHABET)} символов, последний — пробел):\n")
    if len(key) != len(ALPHABET):
        print(f"Ошибка: длина ключа {len(key)}, требуется {len(ALPHABET)}.")
        return

    try:
        enc_map, dec_map = create_maps(key)
    except ValueError as e:
        print(e)
        return

    input_file = input("Имя входного файла: ").strip()
    output_file = input("Имя выходного файла: ").strip()

    try:
        with open(input_file, 'r', encoding=ENCODING) as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Файл '{input_file}' не найден.")
        return
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return

    if mode == 'encrypt':
        prep = input("Очистить текст от знаков препинания и привести к верхнему регистру? (y/n): ").strip().lower()
        if prep == 'y':
            text = preprocess(text)
            print("Текст очищен.")
        mapping = enc_map
    else:
        mapping = dec_map

    result = substitute(text, mapping)

    try:
        with open(output_file, 'w', encoding=ENCODING) as f:
            f.write(result)
        print(f"Готово! Результат записан в '{output_file}'.")
    except Exception as e:
        print(f"Ошибка при записи файла: {e}")

if __name__ == '__main__':
    main()
