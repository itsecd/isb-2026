"""
Модуль для работы с шифром Цезаря через командную строку.

Этот модуль предоставляет интерфейс командной строки для шифрования текстовых
файлов с использованием шифра Цезаря. Он читает исходный текст из файла,
применяет сдвиг (ключ) из другого файла и сохраняет зашифрованный результат.
"""

import argparse
import os
import sys

import caesar_cipher


def parse_command_line_arguments() -> argparse.Namespace:
    """
    Парсит аргументы командной строки.

    Returns:
        Объект Namespace с атрибутами, соответствующими аргументам командной строки.
    """
    parser = argparse.ArgumentParser(
        description="Шифрование текста с помощью шифра Цезаря"
    )

    parser.add_argument(
        "-i", "--input",
        default="original.txt",
        help="Путь к файлу с исходным текстом (по умолчанию: original.txt)"
    )

    parser.add_argument(
        "-k", "--key",
        default="key.txt",
        help="Путь к файлу с ключом шифрования (целое число) (по умолчанию: key.txt)"
    )

    parser.add_argument(
        "-o", "--output",
        default="encrypted.txt",
        help="Путь для сохранения зашифрованного текста (по умолчанию: encrypted.txt)"
    )

    return parser.parse_args()


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
        directory_path = os.path.dirname(file_path)
        if directory_path:
            os.makedirs(directory_path, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

    except IOError as error:
        raise IOError(f"Ошибка при записи файла '{file_path}': {error}")


def extract_shift_key_from_file(key_file_path: str) -> int:
    """
    Извлекает числовой ключ сдвига из файла.

    Args:
        key_file_path: Путь к файлу с ключом.

    Returns:
        Целое число - величина сдвига.

    Raises:
        ValueError: Если файл не содержит корректного целого числа.
        FileNotFoundError: Если файл с ключом не найден.
    """
    key_content = read_text_file(key_file_path).strip()

    try:
        return int(key_content)
    except ValueError:
        raise ValueError(
            f"Файл '{key_file_path}' должен содержать целое число. "
            f"Найдено: '{key_content}'"
        )


def verify_decryption(
    original_text: str,
    encrypted_text: str,
    shift_key: int
) -> bool:
    """
    Проверяет корректность шифрования.

    Args:
        original_text: Исходный текст.
        encrypted_text: Зашифрованный текст.
        shift_key: Ключ сдвига, использованный при шифровании.

    Returns:
        True если дешифровка совпадает с оригиналом, иначе False.
    """
    decrypted_text = caesar_cipher.decrypt(encrypted_text, shift_key)
    return original_text.upper() == decrypted_text.upper()


def main() -> None:
    """
    Основная функция программы.

    Returns:
        None
    """
    try:
        command_args = parse_command_line_arguments()

        original_text = read_text_file(command_args.input)

        shift_value = extract_shift_key_from_file(command_args.key)

        encrypted_text = caesar_cipher.encrypt(original_text, shift_value)

        write_text_file(encrypted_text, command_args.output)

        if verify_decryption(original_text, encrypted_text, shift_value):
            print("Проверка пройдена: расшифровка работает корректно")
        else:
            print("Ошибка: расшифровка не совпадает с исходным текстом")

    except FileNotFoundError as error:
        print(f"Ошибка: {error}")
        sys.exit(1)

    except ValueError as error:
        print(f"Ошибка формата данных: {error}")
        sys.exit(1)

    except IOError as error:
        print(f"Ошибка ввода/вывода: {error}")
        sys.exit(1)

    except Exception as error:
        print(f"Непредвиденная ошибка: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()