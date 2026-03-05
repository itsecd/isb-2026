import os
import sys
from typing import Dict, List, Optional


class CipherError(Exception):
    """Ошибка шифрования."""
    pass


class KeyFileError(CipherError):
    """Ошибка в файле ключа."""
    pass


class FileProcessingError(CipherError):
    """Ошибка обработки файлов."""
    pass


def load_key_from_txt(key_file: str) -> Dict[str, str]:
    """
    Загружает ключ шифрования из текстового файла.

    Args:
        key_file: Путь к файлу с ключом.

    Returns:
        Словарь с парами исходный_символ -> заменяющий_символ.

    Raises:
        KeyFileError: Если файл ключа не найден или имеет неверный формат.
    """
    key_map = {}

    try:
        with open(key_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError as e:
        raise KeyFileError(f"Файл ключа '{key_file}' не найден") from e
    except IOError as e:
        raise KeyFileError(f"Ошибка чтения файла ключа: {e}") from e

    for line_num, line in enumerate(lines, start=1):
        line = line.strip()

        if not line or line.startswith('#'):
            continue

        if line[1]!= '=':
            print(f"Предупреждение: строка {line_num} пропущена (нет символа '='): {line}")
            continue

        original = line[0]
        replacement = line[2]

        if not original:
            print(f"Предупреждение: строка {line_num} - пустой исходный символ: {line}")
            continue

        if not replacement:
            print(f"Предупреждение: строка {line_num} - пустой заменяющий символ: {line}")
            continue

        key_map[original] = replacement

    if not key_map:
        raise KeyFileError("Файл ключа не содержит валидных пар символов")

    return key_map


def validate_key(key_map: Dict[str, str]) -> bool:
    """
    Проверяет ключ на корректность.

    Args:
        key_map: Словарь с парами замены.

    Returns:
        True если ключ корректен (всегда True, только выводит предупреждения).
    """
    replacements = list(key_map.values())
    if len(replacements) != len(set(replacements)):
        print(
            "Предупреждение: в ключе есть повторяющиеся символы замены!\n"
            "Это может привести к неоднозначности при дешифровании."
        )

    return True


def encrypt_text(text: str, key_map: Dict[str, str]) -> str:
    """
    Шифрует текст, заменяя символы согласно ключу.

    Args:
        text: Исходный текст для шифрования.
        key_map: Словарь с парами замены.

    Returns:
        Зашифрованный текст.
    """
    result_chars = []

    for char in text:
        if char in key_map:
            result_chars.append(key_map[char])
        else:
            result_chars.append(char)

    return ''.join(result_chars)


def decrypt_text(text: str, key_map: Dict[str, str]) -> str:
    """
    Дешифрует текст, используя обратную замену.

    Args:
        text: Зашифрованный текст.
        key_map: Словарь с парами замены.

    Returns:
        Расшифрованный текст.
    """
    reverse_map = {v: k for k, v in key_map.items()}

    result_chars = []
    for char in text:
        if char in reverse_map:
            result_chars.append(reverse_map[char])
        else:
            result_chars.append(char)

    return ''.join(result_chars)


def process_file(
    input_file: str,
    output_file: str,
    key_map: Dict[str, str],
    mode: str = 'encrypt'
) -> None:
    """
    Обрабатывает файл целиком.

    Args:
        input_file: Путь к входному файлу.
        output_file: Путь к выходному файлу.
        key_map: Словарь с парами замены.
        mode: Режим работы ('encrypt' или 'decrypt').

    Raises:
        FileProcessingError: При ошибках чтения/записи файлов.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
    except (FileNotFoundError, IOError) as e:
        raise FileProcessingError(
            f"Ошибка чтения входного файла '{input_file}': {e}"
        ) from e

    print(f"\nЗагружен текст из файла: {len(text)} символов")
    print(f"Первые 100 символов:\n{text[:100]}")

    if mode == 'encrypt':
        processed_text = encrypt_text(text, key_map)
        action = "Шифрование"
    else:
        processed_text = decrypt_text(text, key_map)
        action = "Дешифрование"

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(processed_text)
    except IOError as e:
        raise FileProcessingError(
            f"Ошибка записи в выходной файл '{output_file}': {e}"
        ) from e

    print(f"\n{action} завершено успешно!")
    print(f"Результат сохранен в файл: {output_file}")
    print(f"Сохранено символов: {len(processed_text)}")
    print(f"Первые 100 символов результата:\n{processed_text[:100]}")


def get_user_choice() -> str:
    """
    Получает выбор пользователя из меню.

    Returns:
        Выбранный пункт меню.
    """
    while True:
        print("\nМеню:")
        print("1. Зашифровать файл")
        print("2. Расшифровать файл")
        print("3. Выход")

        choice = input("\nВыберите действие (1-4): ").strip()

        if choice in ('1', '2', '3'):
            return choice

        print("Неверный выбор. Пожалуйста, выберите 1-3.")


def get_file_paths(mode: str) -> tuple:
    """
    Получает пути к файлам от пользователя.

    Args:
        mode: Режим работы ('encrypt' или 'decrypt').

    Returns:
        Кортеж (input_file, key_file, output_file).
    """
    action = "шифрования" if mode == 'encrypt' else "дешифрования"
    print(f"\n--- Режим {action} ---")

    input_file = input("Введите путь к входному TXT файлу с текстом: ").strip()
    key_file = input("Введите путь к TXT файлу с ключом: ").strip()
    output_file = input("Введите путь для выходного TXT файла: ").strip()

    if not input_file.lower().endswith('.txt'):
        print("Предупреждение: входной файл должен быть в формате TXT")

    if not key_file.lower().endswith('.txt'):
        print("Предупреждение: файл ключа должен быть в формате TXT")

    if not output_file.lower().endswith('.txt'):
        output_file += '.txt'
        print(f"Выходному файлу добавлено расширение .txt: {output_file}")

    return input_file, key_file, output_file


def display_key_info(key_map: Dict[str, str]) -> None:
    """
    Отображает информацию о загруженном ключе.

    Args:
        key_map: Словарь с парами замены.
    """
    print(f"\nЗагружено {len(key_map)} замен:")
    for i, (orig, repl) in enumerate(list(key_map.items())[:5]):
        print(f"  '{orig}' -> '{repl}'")

    if len(key_map) > 5:
        print(f"  ... и еще {len(key_map) - 5} замен")


def main() -> None:
    """Основная функция программы."""
    print("=" * 50)
    print("     ШИФР ПРОСТОЙ ЗАМЕНЫ")
    print("=" * 50)

    while True:
        try:
            choice = get_user_choice()

            if choice in ('1', '2'):
                mode = 'encrypt' if choice == '1' else 'decrypt'
                input_file, key_file, output_file = get_file_paths(mode)

                if not os.path.exists(input_file):
                    print(f"Ошибка: входной файл '{input_file}' не найден")
                    continue

                if not os.path.exists(key_file):
                    print(f"Ошибка: файл ключа '{key_file}' не найден")
                    continue

                print("\nЗагрузка ключа...")
                key_map = load_key_from_txt(key_file)
                display_key_info(key_map)

                validate_key(key_map)

                process_file(input_file, output_file, key_map, mode)

            elif choice == '3':
                print("\nДо свидания!")
                break

        except KeyFileError as e:
            print(f"Ошибка в файле ключа: {e}")
        except FileProcessingError as e:
            print(f"Ошибка обработки файла: {e}")
        except KeyboardInterrupt:
            print("\n\nПрограмма прервана пользователем.")
            break
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")
            print("Пожалуйста, сообщите об этой ошибке разработчику.")


if __name__ == "__main__":
    main()