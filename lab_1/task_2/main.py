"""
Модуль для дешифрования текста с использованием подстановочного шифра
и анализа частотности символов через командную строку.

Этот модуль читает зашифрованный текст из файла, применяет к нему
подстановку символов согласно заданному ключу, сохраняет расшифрованный
текст и выполняет частотный анализ символов исходного текста.
"""

import argparse
import sys

# Ключ подстановки символов (формат: {зашифрованный_символ: расшифрованный_символ})
SUBSTITUTION_KEY = {"Y": " ", "Ё": "о", "К":"е", "Я":"и", "s": "л", "Й":"т",
                "U":"н", "Д":"к", "i":"ь", "ю":"р", "7":"п", "Q":"с",
                "И":"в", "R":"а", "г":"б", "@":"з", "Ж":"я", "О":"ш",
                "Т":"ж", "F":"э", "J":"й", "G":"ч", "Р":"ю", "1":"ы",
                "у":"ъ", "%":"д", "3":"м", "=":"г", "Z":"ц", "Х":"х", "N":"ф", "П":"щ", "<":"у"
}


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

    return parser.parse_args()


def apply_substitution(encrypted_text: str) -> str:
    """
    Применяет подстановку символов к зашифрованному тексту согласно ключу.

    Args:
        encrypted_text: Зашифрованный текст для дешифрования.

    Returns:
        Расшифрованный текст.
    """
    decrypted_text = encrypted_text

    for encrypted_char, decrypted_char in SUBSTITUTION_KEY.items():
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

        print(f"\nЧтение зашифрованного текста из файла: {command_args.input}")
        encrypted_text = read_text_file(command_args.input)
        print(f"Прочитано символов: {len(encrypted_text)}")

        print("Применение подстановки символов...")
        decrypted_text = apply_substitution(encrypted_text)

        print("\nРАСШИФРОВАННЫЙ ТЕКСТ:")
        print("-" * 50)
        print(decrypted_text)
        print("-" * 50)

        print(f"\nСохранение расшифрованного текста в файл: {command_args.output}")
        write_text_file(decrypted_text, command_args.output)

        print("Выполнение частотного анализа...")
        analyze_frequency(encrypted_text, command_args.freq)

        print("\nОбработка завершена успешно!")

    except FileNotFoundError as error:
        print(f"\nОшибка: {error}")
        print("Убедитесь, что файл существует и путь указан правильно.")
        sys.exit(1)

    except IOError as error:
        print(f"\nОшибка ввода/вывода: {error}")
        sys.exit(1)

    except Exception as error:
        print(f"\nНепредвиденная ошибка: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()