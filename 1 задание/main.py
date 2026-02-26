
from typing import List

ALPHABET = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ "


def vigenere(text: str, key: str) -> str:
    """
    Шифрует текст с использованием шифра Виженера.

    Функция проходит по каждому символу текста. Если символ присутствует
    в алфавите, он сдвигается на величину, соответствующую символу ключа.
    Символы, отсутствующие в алфавите, копируются в результат без изменений
    и не сдвигают индекс ключа.

    Args:
        text (str): Исходный текст для шифрования.
        key (str): Ключ шифрования (строка).

    Returns:
        str: Зашифрованный текст.

    Raises:
        ValueError: Если ключ не содержит ни одного допустимого символа.
    """
    result: List[str] = []
    key_index: int = 0


    clean_key: str = "".join([char.upper() for char in key if char.upper() in ALPHABET])

    if not clean_key:
        raise ValueError("Ключ не содержит допустимых символов!")

    for char in text:
        if char in ALPHABET:
            shift: int = ALPHABET.index(clean_key[key_index % len(clean_key)])
            idx: int = ALPHABET.index(char)
            new_idx: int = (idx + shift) % len(ALPHABET)
            result.append(ALPHABET[new_idx])
            key_index += 1
        else:

            result.append(char)

    return "".join(result)


def vigenere_decrypt(text: str, key: str) -> str:
    """
    Дешифрует текст, зашифрованный шифром Виженера.

    Выполняет обратную операцию шифрованию: сдвигает символы в обратную сторону
    на величину, соответствующую символу ключа.

    Args:
        text (str): Зашифрованный текст.
        key (str): Ключ дешифрования (должен совпадать с ключом шифрования).

    Returns:
        str: Расшифрованный исходный текст.
    """
    result: List[str] = []
    key_index: int = 0

    clean_key: str = "".join([char.upper() for char in key if char.upper() in ALPHABET])

    for char in text:
        if char in ALPHABET:
            shift: int = ALPHABET.index(clean_key[key_index % len(clean_key)])
            idx: int = ALPHABET.index(char)
            new_idx: int = (idx - shift) % len(ALPHABET)
            result.append(ALPHABET[new_idx])
            key_index += 1
        else:
            result.append(char)

    return "".join(result)


def main() -> None:
    """
    Основная функция выполнения скрипта.

    Считывает исходный текст из файла 'source.txt', очищает его,
    шифрует ключом 'ДАНИЛКОЛБАСЕНКО', проверяет целостность дешифрования
    и записывает результаты в файлы 'crypt.txt' и 'key_task1.txt'.
    """
    input_filename: str = "source.txt"
    output_filename: str = "crypt.txt"
    key_filename: str = "key_task1.txt"
    key: str = "ДАНИЛКОЛБАСЕНКО"

    try:
        with open(input_filename, "r", encoding="utf-8") as f:
            source_text: str = f.read()

        clean_text: str = "".join(
            [char.upper() for char in source_text if char.upper() in ALPHABET]
        )

        encrypted_text: str = vigenere(clean_text, key)
        decrypted_check: str = vigenere_decrypt(encrypted_text, key)


        if clean_text != decrypted_check:
            print("ОШИБКА: Расшифровка не совпадает с оригиналом!")
            return

        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(encrypted_text)

        with open(key_filename, "w", encoding="utf-8") as f:
            f.write(key)

        print(f"Успешно выполнено!")
        print(f"Первые 100 символов расшифрованного текста:\n{decrypted_check[:100]}")

    except FileNotFoundError:
        print(f"Ошибка: Файл '{input_filename}' не найден.")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")


if __name__ == "__main__":
    main()