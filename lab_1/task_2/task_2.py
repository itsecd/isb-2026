import json
import os
import argparse

import constants


def parse_args():
    """Обработка аргументов командной строки для дешифровки текста"""
    parser = argparse.ArgumentParser(
        description="Частотный анализ и дешифровка текста"
    )
    parser.add_argument(
        "-i",
        "--input",
        default="data/cod1.txt",
        help="Зашифрованный текст",
    )
    parser.add_argument(
        "-k",
        "--key",
        default="key.json",
        help="Файл ключа для дешифровки",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="data/decrypted.txt",
        help="Файл для результата",
    )
    parser.add_argument(
        "-ef",
        "--encrypted-freq",
        default="freq_encrypted.json",
        help="Файл частот",
    )
    return parser.parse_args()


def read_file(file_path, json_format=False):
    """Чтение файла"""
    if not os.path.exists(file_path):
        if json_format:
            return None
        raise FileNotFoundError(f"Файл '{file_path}' не найден")

    with open(file_path, "r", encoding="utf-8") as file:
        if json_format:
            return json.load(file)

        return file.read()
    

def write_file(content, file_path, json_format=False):
    """Запись текста или JSON в файл"""
    os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as file:
        if json_format:
            json.dump(content, file, ensure_ascii=False, indent=4)
        else:
            file.write(content)

    print(f"Создан файл: {file_path}")    


def analyze_frequencies(text):
    """Возвращает словарь частот символов, отсортированный по убыванию"""
    counts = {}

    for char in text:
        counts[char] = counts.get(char, 0) + 1

    total = len(text)
    freqs = {char: counts[char] / total for char in counts}

    return dict(
        sorted(freqs.items(), key=lambda item: item[1], reverse=True)
    )


def generate_key(encrypted_freq, reference_freq):
    """Создание ключа на основе частот"""
    key = {}
    encrypted_chars = list(encrypted_freq.keys())
    reference_chars = list(reference_freq.keys())

    for index, char in enumerate(encrypted_chars):
        if index < len(reference_chars):
            key[char] = reference_chars[index]
        else:
            key[char] = char

    return key


def apply_key(text, key):
    """Применяет ключ к тексту для получения расшифровки"""
    return "".join(key.get(char, char) for char in text)


def main():
    """Основная функция"""
    args = parse_args()

    try:
        text = read_file(args.input)
        print(f"Текстовый файл: {args.input}")

        freqs = analyze_frequencies(text)
        write_file(freqs, args.encrypted_freq, json_format=True)

        key = read_file(args.key, json_format=True)

        if key is None:
            print("Ключ не найден, генерируем новый")
            key = generate_key(freqs, constants.REFERENCE_FREQUENCIES)
            write_file(key, args.key, json_format=True)

        decrypted = apply_key(text, key)
        write_file(decrypted, args.output)

    except Exception as error:
        print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()