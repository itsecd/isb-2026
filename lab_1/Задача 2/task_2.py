import argparse
from constants_task_2 import (STANDARD_FREQUENCIES, ENCRYPTED_TEXT_PATH, KEY_PATH,
                       DECRYPTED_TEXT_PATH, ENCRYPTED_FREQUENCIES_PATH)
import sys


def parse_args() -> argparse.Namespace:
    """
    Разбор аргументов командной строки
    :return: аргументы командной строки
    """

    p = argparse.ArgumentParser()

    p.add_argument("-e",
                   "--encrypted_text_path",
                   default=ENCRYPTED_TEXT_PATH,
                   help="Путь к зашифрованному тексту")

    p.add_argument("-kp",
                   "--key_path",
                   default=KEY_PATH,
                   help="Путь для сохранения значения ключа")

    p.add_argument("-d",
                   "--decrypted_text_path",
                   default=DECRYPTED_TEXT_PATH,
                   help="Путь для сохранения дешифрованного текста")

    p.add_argument("-ef",
                   "--encrypted_frequencies_path",
                   default=ENCRYPTED_FREQUENCIES_PATH,
                   help="Путь для сохранения таблицы частотности")

    return p.parse_args()

def read_encrypted_text(filename: str) -> str:
    """
    Чтение зашифрованного текста из файла
    :param filename: имя файла
    :return: текст из файла
    """
    try:
        with open(filename, "r") as f:
            encrypted_text = f.read()
    except FileNotFoundError:
        print(f"File path {filename} was not found")
        sys.exit(1)

    return encrypted_text

def calculation_char_frequencies(text: str) -> dict[str, int]:
    """
    Вычисление частот символов в зашифрованном тексте
    :param text: зашифрованный текст
    :return: посчитанные частоты
    """
    char_frequencies = {}
    for char in text:
        if char != "\n":
            char_frequencies[char] = char_frequencies.get(char, 0) + 1

    for char in char_frequencies:
        char_frequencies[char] = round(char_frequencies[char]/ len(text), 6)

    char_frequencies = dict(sorted(char_frequencies.items(), key=lambda x: x[1], reverse=True))

    return char_frequencies

def write_frequencies_in_file(filename: str, char_frequencies: dict[str, int])-> None:
    """
    Запись посчитанных частот символов зашифрованного текста в файл
    :param filename: имя файла
    :param char_frequencies: посчитанные частоты
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Таблица частот для символов зашифрованного текста\n")
            for item in char_frequencies:
                f.write(f"\'{item}\': {char_frequencies[item]}\n")
    except FileNotFoundError:
        print(f"File path {filename} was not found")
        sys.exit(1)


def write_key_in_file(filename: str, key: dict[str, str])-> None:
    """
    Запись найденного ключа зашифрованного текста в файл
    :param filename: имя файла
    :param key: найденный ключ
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Найденный ключ шифрования текста\n")
            f.write(f"+------------+--------------+\n")
            f.write(f"|    Шифр    |    Дешифр    |\n")
            f.write(f"+------------+--------------+\n")
            for item in key:
                f.write(f"|    \'{item}\'     |     \'{key[item]}\'      |\n")
                f.write(f"+------------+--------------+\n")
    except FileNotFoundError:
        print(f"File path {filename} was not found")
        sys.exit(1)

def write_decrypted_text_in_file(filename: str, text: str)-> None:
    """
    Запись дешифрованного текста в файл
    :param filename: имя файла
    :param text: дешифрованный текст
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
    except FileNotFoundError:
        print(f"File path {filename} was not found")
        sys.exit(1)

def main():
    args = parse_args()

    encrypted_text = read_encrypted_text(args.encrypted_text_path)

    char_frequencies = calculation_char_frequencies(encrypted_text)

    write_frequencies_in_file(args.encrypted_frequencies_path, char_frequencies)

    key = dict(zip(char_frequencies.keys(), STANDARD_FREQUENCIES.keys()))

    key_keys = list(key.keys())
    char_frequencies_keys = list(char_frequencies.keys())
    while len(key) != len(char_frequencies):
        key[char_frequencies_keys[len(key_keys)]] = char_frequencies_keys[len(key_keys)]

    for char in key:
        if char != "Я":
            encrypted_text = encrypted_text.replace(char, key[char].lower())
        else:
            encrypted_text = encrypted_text.replace(char, "*")

    encrypted_text = encrypted_text.replace("*", " ")

    print("\n")
    print(encrypted_text)
    print("\n")

    while True:
        answer = input("Желаете продолжить замену символов?(Да/Нет): ")
        while answer.lower() != "да" and answer.lower() != "нет":
            answer = input("Желаете продолжить замену символов?(Да/Нет): ")

        if answer.lower() == "нет":
            break

        char_to_change = input("Введите символ из зашифрованного текста, который хотите заменить: ")
        char_for_change = input("Введите символ для замены: ")

        copy_encrypted_text = encrypted_text
        copy_key = key
        if char_to_change.upper() in key.values():
            for char in key:
                if key[char] == char_to_change.upper():
                    key[char] = char_for_change.lower()
            encrypted_text = encrypted_text.replace(f"{char_to_change}", f"{char_for_change.upper()}")

        print("\n")
        print(encrypted_text)
        print("\n")

        back = input("Хотите вернуться к предыдущей версии текста?(Да/Нет): ")
        while back.lower() != "да" and back.lower() != "нет":
            back = input("Хотите вернуться к предыдущей версии текста?(Да/Нет): ")

        if back.lower() == "да":
            encrypted_text = copy_encrypted_text
            key = copy_key
            print("\n")
            print(copy_encrypted_text)
            print("\n")

    write_key_in_file(args.key_path, key)
    write_decrypted_text_in_file(args.decrypted_text_path, encrypted_text)



if __name__ == "__main__":
    main()