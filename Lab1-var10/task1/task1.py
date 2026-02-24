import re
import sys

ALPHABET = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ '

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

def encrypt(text, enc_map):
    """Заменяет каждый символ текста по словарю enc_map."""
    return ''.join(enc_map.get(ch, ch) for ch in text)

def decrypt(text, dec_map):
    """Заменяет каждый символ текста по словарю dec_map."""
    return ''.join(dec_map.get(ch, ch) for ch in text)

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
        with open(input_file, 'r', encoding='utf-8') as f:
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
        result = encrypt(text, enc_map)
    else:
        result = decrypt(text, dec_map)

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"Готово! Результат записан в '{output_file}'.")
    except Exception as e:
        print(f"Ошибка при записи файла: {e}")

if __name__ == '__main__':
    main()
