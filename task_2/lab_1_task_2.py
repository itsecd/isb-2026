import argparse
import json


def decrypt_text(encrypted_text, decryption_key):
    "Заменяет символы в зашифрованном тексте согласно ключу дешифровки"
    result = ""
    for char in encrypted_text:
        if char in decryption_key:
            result += decryption_key[char]
        else:
            result += char
    return result


def count_frequencies(text):
    "Подсчитывает количество вхождений каждого символа в тексте и сортирует по возрастанию"
    frequencies = {}
    for ch in text:
        frequencies[ch] = frequencies.get(ch, 0) + 1

    items = list(frequencies.items())

    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i][1] > items[j][1]:
                items[i], items[j] = items[j], items[i]

    return items


def frequen(text, items):
    "Преобразует абсолютные частоты символов в относительные"
    n = len(text)
    fren = {}
    for ch, freq in items:
        fren[ch] = freq / n
    return fren


def parse_arguments():
    "Считывает и обрабатывает аргументы командной строки"
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", nargs="?", help="Путь к файлу для обработки")
    parser.add_argument("output_file", help="Путь к файлу для записи результата")
    parser.add_argument("key", help="Путь к файлу с ключом шифрования")
    parser.add_argument("frequencies_file", help="файл с частотами")
    return parser.parse_args()


def read_file(file_path):
    "Читает содержимое текстового файла с обработкой ошибок"
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
    "Читает JSON файл с ключом дешифровки"
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print(f"Ошибка при чтении JSON ключа: {e}")
        return None


def write_file(file_path, content):
    "Записывает текст в файл"
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
    except Exception as e:
        print(f"Ошибка при записи файла: {e}")


def write_frequencies(file_path, frequencies_dict):
    "Записывает словарь с частотами символов в файл"
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            for char, freq in frequencies_dict.items():
                line = repr(char) + ": " + str(freq) + "\n"
                file.write(line)
    except Exception as e:
        print(f"Ошибка при записи частот в файл {file_path}: {e}")


if __name__ == "__main__":
    args = parse_arguments()
    encrypted_text = read_file(args.input_file)
    decryption_key = read_json_key(args.key)
    frequencies_list = count_frequencies(encrypted_text)
    frequencies_dict = frequen(encrypted_text, frequencies_list)
    print("\nЧастоты символов в шифровке:")
    for char, freq in frequencies_dict.items():
        print(f"'{char}': {freq}")
    decrypted = decrypt_text(encrypted_text, decryption_key)
    print(f"\nРасшифрованный текст: {decrypted}")
    write_frequencies(args.frequencies_file, frequencies_dict)
    write_file(args.output_file, decrypted)
