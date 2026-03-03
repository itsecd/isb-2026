import json
import os
import argparse
from collections import Counter

import constants


def parse_arguments():
    """Парсинг аргументов командной строки"""

    parser = argparse.ArgumentParser(description="Частотная дешифровка")

    parser.add_argument(
        "-i", "--input", default="data/cod19.txt", help="Файл с зашифрованным текстом"
    )

    parser.add_argument(
        "-k1", "--key1", default="key_1.json", help="Файл для первого ключа"
    )

    parser.add_argument(
        "-k2", "--key2", default="key_2.json", help="Файл для второго ключа"
    )

    parser.add_argument(
        "-o1",
        "--output1",
        default="data/decrypted_1.txt",
        help="Файл для первой расшифровки",
    )

    parser.add_argument(
        "-o2",
        "--output2",
        default="data/decrypted_2.txt",
        help="Файл для финальной расшифровки",
    )

    parser.add_argument(
        "-ef",
        "--encrypted-freq",
        default="freq_encrypted.json",
        help="Файл с частотами шифротекста",
    )

    return parser.parse_args()


def read_file(filepath, is_json=False):
    """Чтение файла (текстового или JSON)"""

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f) if is_json else f.read()
    except FileNotFoundError:
        if is_json:
            return None
        raise FileNotFoundError(f"Файл '{filepath}' не найден")
    except json.JSONDecodeError:
        raise ValueError(f"Файл '{filepath}' содержит некорректный JSON")


def write_file(data, filepath, is_json=False):
    """Запись файла (текстового или JSON)"""

    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        if is_json:
            json.dump(data, f, ensure_ascii=False, indent=4)
        else:
            f.write(data)

    print(f"Создан: {filepath}")


def calculate_frequencies(text):
    """Подсчёт частот символов в тексте"""

    total = len(text)
    if total == 0:
        return {}

    counter = Counter(text)
    frequencies = {char: count / total for char, count in counter.items()}
    return dict(sorted(frequencies.items(), key=lambda x: x[1], reverse=True))


def create_key(encrypted_freq, sample_freq):
    """Создание первого ключа путём сопоставления частот"""

    encrypted_sorted = list(encrypted_freq.keys())
    sample_sorted = list(sample_freq.keys())

    key = {}
    for i in range(min(len(encrypted_sorted), len(sample_sorted))):
        key[encrypted_sorted[i]] = sample_sorted[i]

    for char in encrypted_sorted:
        if char not in key:
            key[char] = char

    return key


def apply_key(text, key):
    """Применение ключа к тексту"""

    result = []
    for char in text:
        result.append(key.get(char, char))
    return "".join(result)


def main():
    """Основная функция программы"""

    args = parse_arguments()

    try:
        encrypted_text = read_file(args.input)
        print(f"Загружен текст: {args.input}")

        sample_freq = constants.REFERENCE_FREQUENCIES
        encrypted_freq = calculate_frequencies(encrypted_text)
        write_file(encrypted_freq, args.encrypted_freq, is_json=True)

        first_key = read_file(args.key1, is_json=True)
        if first_key is None:
            print("Создание первого ключа...")
            first_key = create_key(encrypted_freq, sample_freq)
            write_file(first_key, args.key1, is_json=True)

        if not os.path.exists(args.output1):
            decrypted_1 = apply_key(encrypted_text, first_key)
            write_file(decrypted_1, args.output1, is_json=False)
            print(f"Первая расшифровка: {args.output1}")

        second_key = read_file(args.key2, is_json=True)
        if second_key:
            decrypted_2 = apply_key(encrypted_text, second_key)
            write_file(decrypted_2, args.output2, is_json=False)
            print(f"Финальная расшифровка: {args.output2}")
        else:
            print(f"Второй ключ {args.key2} не найден")
            print(f"Отредактируйте {args.key1} и сохраните как {args.key2}")

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
