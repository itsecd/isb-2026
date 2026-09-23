from pathlib import Path


ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"


def read_file(file_name: str) -> str:
    """
    Читает содержимое текстового файла.

    :param file_name: имя файла.
    :return: содержимое файла.
    :raises FileNotFoundError: если файл не найден.
    """
    path = Path(file_name)

    with path.open("r", encoding="utf-8") as file:
        return file.read()


def write_file(file_name: str, text: str) -> None:
    """
    Записывает текст в файл.

    :param file_name: имя файла.
    :param text: текст для записи.
    """
    path = Path(file_name)

    with path.open("w", encoding="utf-8") as file:
        file.write(text)


def validate_key(key: str) -> None:
    """
    Проверяет корректность ключа простой подстановки.

    :param key: ключ шифрования.
    :raises ValueError: если ключ некорректен.
    """
    if len(key) != len(ALPHABET):
        raise ValueError(
            "Ключ должен содержать "
            f"{len(ALPHABET)} символов."
        )


def encrypt(text: str, key: str) -> str:
    """
    Шифрует текст методом простой подстановки.

    :param text: исходный текст.
    :param key: ключ шифрования.
    :return: зашифрованный текст.
    """
    validate_key(key)

    result = []

    for char in text:
        if char in ALPHABET:
            index = ALPHABET.index(char)
            result.append(key[index])
        elif char.lower() in ALPHABET:
            index = ALPHABET.index(char.lower())
            result.append(key[index].upper())
        else:
            result.append(char)

    return "".join(result)


def decrypt(text: str, key: str) -> str:
    """
    Расшифровывает текст методом простой подстановки.

    :param text: зашифрованный текст.
    :param key: ключ шифрования.
    :return: расшифрованный текст.
    """
    validate_key(key)

    result = []

    for char in text:
        if char in key:
            index = key.index(char)
            result.append(ALPHABET[index])
        elif char.lower() in key:
            index = key.index(char.lower())
            result.append(ALPHABET[index].upper())
        else:
            result.append(char)

    return "".join(result)


def normalize_key(key: str) -> str:
    """
    Удаляет пробелы и переводы строк из ключа.

    :param key: исходный ключ.
    :return: очищенный ключ.
    """
    return "".join(key.split()).lower()


def main() -> None:
    """
    Основная функция программы.

    Загружает исходный текст и ключ из файлов,
    выполняет шифрование и расшифровку,
    сохраняет результаты в файлы.
    """
    source_file = "source.txt"
    key_file = "key.txt"
    encrypted_file = "encrypted.txt"
    decrypted_file = "decrypted.txt"

    try:
        text = read_file(source_file)
        key = normalize_key(read_file(key_file))

        if len(text) < 500:
            raise ValueError(
                "Исходный текст должен содержать не менее "
                "500 символов."
            )

        encrypted_text = encrypt(text, key)
        decrypted_text = decrypt(encrypted_text, key)

        write_file(encrypted_file, encrypted_text)
        write_file(decrypted_file, decrypted_text)

        print("Шифрование выполнено.")
        print(f"Исходный текст: {len(text)} символов.")
        print(f"Результат сохранён в: {encrypted_file}")
        print(f"Расшифровка сохранена в: {decrypted_file}")

        if text == decrypted_text:
            print("Проверка: расшифрованный текст совпадает "
                  "с исходным.")
        else:
            print("Проверка: тексты НЕ совпадают.")

    except FileNotFoundError as exc:
        print(f"Ошибка: файл не найден: {exc.filename}")
    except ValueError as exc:
        print(f"Ошибка: {exc}")
    except OSError as exc:
        print(f"Ошибка работы с файлом: {exc}")


if __name__ == "__main__":
    main()