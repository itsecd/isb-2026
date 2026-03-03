import argparse
import os

import caesar


def parse_arguments():
    """Парсинг аргументов командной строки"""

    parser = argparse.ArgumentParser(description="Шифр Цезаря")

    parser.add_argument(
        "-i", "--input", default="data/original.txt", help="Файл с текстом"
    )

    parser.add_argument(
        "-k", "--key", default="data/key.txt", help="Файл для сохранения ключа"
    )

    parser.add_argument(
        "-o",
        "--output",
        default="data/encrypted.txt",
        help="Файл для зашифрованного текста",
    )

    return parser.parse_args()


def read_file(filepath):
    """Чтение файла"""

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{filepath}' not found")


def write_file(content, filepath):
    """Запись в файл"""

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Создан: {filepath}")


def main() -> None:
    """Основная функция программы"""

    args = parse_arguments()

    try:
        original_text = read_file(args.input)
        print(f"\nИсходный текст: {args.input}")

        key_content = read_file(args.key)
        try:
            shift = int(key_content.strip())
            print(f"Ключ из файла: {shift:+d}")
        except ValueError:
            raise ValueError(f"Файл {args.key} должен содержать число")

        encrypted_text = caesar.encrypt(original_text, shift)

        write_file(encrypted_text, args.output)

        decrypted_text = caesar.decrypt(encrypted_text, shift)
        if original_text.upper() == decrypted_text.upper():
            print("\nПроверка пройдена: расшифровка работает корректно")
        else:
            print("\nОшибка: расшифровка не совпадает с исходным текстом")

    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
