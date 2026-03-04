"""
Модуль для дешифрования текста с использованием подстановочного шифра
и анализа частотности символов через командную строку.

Этот модуль читает зашифрованный текст из файла, применяет к нему
подстановку символов согласно ключу из внешнего JSON-файла, сохраняет
расшифрованный текст и выполняет частотный анализ символов исходного текста.
"""

import argparse
import sys
import json
import os


def load_substitution_key(key_file_path: str = "substitution_key.json") -> dict:
    """
    Загружает ключ подстановки из JSON-файла.

    Args:
        key_file_path: Путь к файлу с ключом подстановки.

    Returns:
        Словарь с ключом подстановки {зашифрованный_символ: расшифрованный_символ}.

    Raises:
        FileNotFoundError: Если файл с ключом не найден.
        JSONDecodeError: Если файл содержит некорректный JSON.
    """
    try:
        with open(key_file_path, "r", encoding="utf-8") as file:
            key = json.load(file)
        print(f"Ключ подстановки загружен из файла: {key_file_path}")
        return key
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл с ключом подстановки '{key_file_path}' не найден.")
    except json.JSONDecodeError as error:
        raise json.JSONDecodeError(f"Ошибка в формате JSON файла '{key_file_path}': {error}", error.doc, error.pos)


def parse_command_line_arguments() -> argparse.Namespace:
    """
    Парсит аргументы командной строки.

    Returns:
        Объект Namespace с атрибутами, соответствующими аргументам командной строки.
    """
    parser = argparse.ArgumentParser(
        description="Дешифрование текста с подстановкой символов"
    )

    parser.add_argument(
        "-i", "--input",
        default="cod10.txt",
        help="Путь к файлу с зашифрованным текстом (по умолчанию: cod10.txt)"
    )

    parser.add_argument(
        "-o", "--output",
        default="decrypted.txt",
        help="Путь для сохранения расшифрованного текста (по умолчанию: decrypted.txt)"
    )

    parser.add_argument(
        "-f", "--freq",
        default="frequency.txt",
        help="Путь для сохранения частотного анализа (по умолчанию: frequency.txt)"
    )

    parser.add_argument(
        "-k", "--key",
        default="substitution_key.json",
        help="Путь к файлу с ключом подстановки (по умолчанию: substitution_key.json)"
    )

    return parser.parse_args()


def apply_substitution(encrypted_text: str, substitution_key: dict) -> str:
    """
    Применяет подстановку символов к зашифрованному тексту согласно ключу.

    Args:
        encrypted_text: Зашифрованный текст для дешифрования.
        substitution_key: Словарь с ключом подстановки.

    Returns:
        Расшифрованный текст.
    """
    decrypted_text = encrypted_text

    for encrypted_char, decrypted_char in substitution_key.items():
        decrypted_text = decrypted_text.replace(encrypted_char, decrypted_char)

    return decrypted_text


def analyze_frequency(text: str, frequency_file_path: str) -> None:
    """
    Выполняет частотный анализ символов в тексте.

    Args:
        text: Текст для частотного анализа.
        frequency_file_path: Путь для сохранения файла с частотами.

    Returns:
        None
    """
    unique_characters = set(text)

    frequency_dict = {character: 0 for character in unique_characters}

    for current_char in text:
        frequency_dict[current_char] += 1

    text_length = len(text)
    for character, count in frequency_dict.items():
        frequency_dict[character] = count / text_length

    sorted_frequencies = {
        character: frequency
        for character, frequency in sorted(
            frequency_dict.items(),
            key=lambda item: item[1],
            reverse=True
        )
    }

    try:
        with open(frequency_file_path, "w", encoding="utf-8") as file:
            for character, frequency in sorted_frequencies.items():
                file.write(f"{character} {frequency:.6f}\n")
        print(f"Файл частотного анализа сохранён: {frequency_file_path}")
    except IOError as error:
        print(f"Ошибка при записи файла частотного анализа: {error}")


def read_text_file(file_path: str) -> str:
    """
    Читает содержимое текстового файла.

    Args:
        file_path: Путь к файлу для чтения.

    Returns:
        Содержимое файла в виде строки.

    Raises:
        FileNotFoundError: Если указанный файл не существует.
        IOError: Если возникла ошибка при чтении файла.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл '{file_path}' не найден.")
    except IOError as error:
        raise IOError(f"Ошибка при чтении файла '{file_path}': {error}")


def write_text_file(content: str, file_path: str) -> None:
    """
    Записывает содержимое в текстовый файл.

    Args:
        content: Текст для записи.
        file_path: Путь для сохранения файла.

    Returns:
        None

    Raises:
        IOError: Если возникла ошибка при записи файла.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"Файл сохранён: {file_path}")
    except IOError as error:
        raise IOError(f"Ошибка при записи файла '{file_path}': {error}")


def main() -> None:
    """
    Основная функция программы.

    Returns:
        None
    """
    print("=" * 50)
    print("ДЕШИФРОВАНИЕ ТЕКСТА С ПОДСТАНОВКОЙ СИМВОЛОВ")
    print("=" * 50)

    try:
        command_args = parse_command_line_arguments()

        substitution_key = load_substitution_key(command_args.key)
        print(f"Загружено символов в ключе: {len(substitution_key)}")

        print(f"\nЧтение зашифрованного текста из файла: {command_args.input}")
        encrypted_text = read_text_file(command_args.input)
        print(f"Прочитано символов: {len(encrypted_text)}")

        print("Применение подстановки символов...")
        decrypted_text = apply_substitution(encrypted_text, substitution_key)

        print("\nРАСШИФРОВАННЫЙ ТЕКСТ:")
        print("-" * 50)
        print(decrypted_text)
        print("-" * 50)

        print(f"\nСохранение расшифрованного текста в файл: {command_args.output}")
        write_text_file(decrypted_text, command_args.output)

        print("Выполнение частотного анализа...")
        analyze_frequency(encrypted_text, command_args.freq)

        print("\nОбработка завершена успешно!")

    except (FileNotFoundError, json.JSONDecodeError) as error:
        print(f"\nОшибка: {error}")
        sys.exit(1)

    except IOError as error:
        print(f"\nОшибка ввода/вывода: {error}")
        sys.exit(1)

    except Exception as error:
        print(f"\nНепредвиденная ошибка: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()