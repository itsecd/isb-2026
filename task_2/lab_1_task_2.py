import argparse
import json


def decrypt_text(encrypted_text, decryption_key):
    result = ""
    for char in encrypted_text:
        if char in decryption_key:
            result += decryption_key[char]
        else:
            result += char
    return result


def count_frequencies(text):
    frequencies = {}
    for ch in text:
        frequencies[ch] = frequencies.get(ch, 0) + 1

    items = list(frequencies.items())

    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i][1] > items[j][1]:
                items[i], items[j] = items[j], items[i]

    return items


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", nargs="?", help="Путь к файлу для обработки")
    parser.add_argument("output_file", help="Путь к файлу для записи результата")
    parser.add_argument("key", help="Путь к файлу с ключом шифрования")
    parser.add_argument("frequencies_file", help="файл с частотами")
    return parser.parse_args()


def read_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл '{file_path}' не найден")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None


def read_json_key(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print(f"Ошибка при чтении JSON ключа: {e}")
        return None


def write_file(file_path, content):
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
    except Exception as e:
        print(f"Ошибка при записи файла: {e}")


def write_frequencies(file_path, frequencies):
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            for char, count in frequencies:
                line = repr(char) + ": " + str(count) + "\n"
                file.write(line)
    except Exception as e:
        print("Ошибка при записи частот:", e)


if __name__ == "__main__":
    args = parse_arguments()
    encrypted_text = read_file(args.input_file)
    decryption_key = read_json_key(args.key)
    frequencies = count_frequencies(encrypted_text)
    print("\nЧастоты символов в шифровке:")
    for char, count in frequencies:
        print(f"'{char}': {count}")
    decrypted = decrypt_text(encrypted_text, decryption_key)
    print(f"\nРасшифрованный текст: {decrypted}")
    write_frequencies(args.frequencies_file, frequencies)
