"""
Модуль для шифрования и дешифрования текста шифром Виженера.

Использует кириллический алфавит и ключ из внешнего файла.
Конфигурация путей к файлам импортируется из модуля const.
"""

from typing import List

from const import ALPHABET, INPUT_FILE, KEY_FILE, OUTPUT_FILE


def load_key(filepath: str) -> str:
    """
    Загрузить ключ шифрования из текстового файла.

    Аргументы:
        filepath (str): Путь к файлу, содержащему ключ.

    Возвращает:
        str: Ключевая строка без ведущих/замыкающих пробелов и переносов.

    Raises:
        FileNotFoundError: Если файл с ключом не найден.
        UnicodeDecodeError: Если файл не может быть прочитан в кодировке UTF-8.
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read().strip()


def clean_key(key: str, alphabet: str) -> str:
    """
    Очистить ключ от символов, отсутствующих в алфавите.

    Аргументы:
        key (str): Исходная ключевая строка.
        alphabet (str): Строка допустимых символов алфавита.

    Возвращает:
        str: Ключ, содержащий только допустимые символы в верхнем регистре.

    Raises:
        ValueError: Если после очистки ключ становится пустым.
    """
    cleaned: str = "".join(
        [char.upper() for char in key if char.upper() in alphabet]
    )

    if not cleaned:
        raise ValueError("Ключ не содержит допустимых символов!")

    return cleaned


def vigenere(text: str, key: str, alphabet: str) -> str:
    """
    Шифрует текст с использованием шифра Виженера.

    Функция проходит по каждому символу текста. Если символ присутствует
    в алфавите, он сдвигается на величину, соответствующую символу ключа.
    Символы, отсутствующие в алфавите, копируются в результат без изменений
    и не сдвигают индекс ключа.

    Аргументы:
        text (str): Исходный текст для шифрования.
        key (str): Ключ шифрования (строка).
        alphabet (str): Строка алфавита для сдвига.

    Возвращает:
        str: Зашифрованный текст.

    Raises:
        ValueError: Если ключ не содержит ни одного допустимого символа.
    """
    result: List[str] = []
    key_index: int = 0

    # Переименовано в valid_key, чтобы не конфликтовало с именем функции clean_key
    valid_key: str = "".join(
        [char.upper() for char in key if char.upper() in alphabet]
    )

    if not valid_key:
        raise ValueError("Ключ не содержит допустимых символов!")

    for char in text:
        if char in alphabet:
            shift: int = alphabet.index(valid_key[key_index % len(valid_key)])
            idx: int = alphabet.index(char)
            new_idx: int = (idx + shift) % len(alphabet)
            result.append(alphabet[new_idx])
            key_index += 1
        else:
            result.append(char)

    return "".join(result)


def vigenere_decrypt(text: str, key: str, alphabet: str) -> str:
    """
    Дешифрует текст, зашифрованный шифром Виженера.

    Выполняет обратную операцию шифрованию: сдвигает символы в обратную сторону
    на величину, соответствующую символу ключа.

    Аргументы:
        text (str): Зашифрованный текст.
        key (str): Ключ дешифрования (должен совпадать с ключом шифрования).
        alphabet (str): Строка алфавита для сдвига.

    Возвращает:
        str: Расшифрованный исходный текст.
    """
    result: List[str] = []
    key_index: int = 0

    valid_key: str = "".join(
        [char.upper() for char in key if char.upper() in alphabet]
    )

    for char in text:
        if char in alphabet:
            shift: int = alphabet.index(valid_key[key_index % len(valid_key)])
            idx: int = alphabet.index(char)
            new_idx: int = (idx - shift) % len(alphabet)
            result.append(alphabet[new_idx])
            key_index += 1
        else:
            result.append(char)

    return "".join(result)


def main() -> None:
    """
    Основная функция выполнения скрипта.

    Считывает исходный текст из файла, шифрует его ключом из файла,
    проверяет целостность дешифрования и записывает результат.
    """
    try:
        key: str = load_key(KEY_FILE)

        with open(INPUT_FILE, 'r', encoding='utf-8') as input_file:
            source_text: str = input_file.read()

        encrypted_text: str = vigenere(source_text, key, ALPHABET)

        decrypted_check: str = vigenere_decrypt(encrypted_text, key, ALPHABET)

        if source_text.upper() != decrypted_check.upper():
            print("ОШИБКА: Расшифровка не совпадает с оригиналом!")
            return

        with open(OUTPUT_FILE, 'w', encoding='utf-8') as output_file:
            output_file.write(encrypted_text)

        print("Успешно выполнено!")

    except FileNotFoundError as e:
        print(f"Ошибка: Файл не найден — {e}")
    except ValueError as e:
        print(f"Ошибка ключа: {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")


if __name__ == "__main__":
    main()