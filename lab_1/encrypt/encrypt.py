import sys

import constants


def encrypt(text: str) -> str:
    """
    Зашифровывает текст методом простой моноалфавитной замены.

    Args:
        text (str): Исходный открытый текст (в верхнем регистре).

    Returns:
        str: Зашифрованный текст.
    """
    return "".join(
        constants.CIPHER[constants.ALPHABET.index(char)]
        if char in constants.ALPHABET else char
        for char in text
    )


def decrypt(text: str) -> str:
    """
    Расшифровывает текст, зашифрованный методом моноалфавитной замены.

    Args:
        text (str): Зашифрованный текст.

    Returns:
        str: Расшифрованный открытый текст.
    """
    return "".join(
        constants.ALPHABET[constants.CIPHER.index(char)]
        if char in constants.CIPHER else char
        for char in text
    )


def main() -> None:
    """
    Основная функция: читает входной файл, шифрует его, сохраняет
    результаты и выводит расшифрованный текст для проверки.
    """
    try:
        with open(constants.INPUT_FILE, "r", encoding="utf-8") as f:
            text = f.read().upper()
    except FileNotFoundError:
        print(f"Критическая ошибка: Файл '{constants.INPUT_FILE}' не найден.")
        sys.exit(1)
    except OSError as e:
        print(f"Критическая ошибка: Ошибка чтения '{constants.INPUT_FILE}': {e}")
        sys.exit(1)

    encrypted_text = encrypt(text)

    try:
        with open(constants.ENCRYPTED_FILE, "w", encoding="utf-8") as f:
            f.write(encrypted_text)

        with open(constants.KEY_FILE, "w", encoding="utf-8") as f:
            f.write(f"OPEN:  {constants.ALPHABET}\n")
            f.write(f"CIPHER:{constants.CIPHER}\n")

        print(f"Текст сохранен в '{constants.ENCRYPTED_FILE}'.")
        print(f"Ключ сохранен в '{constants.KEY_FILE}'.")
    except OSError as e:
        print(f"Ошибка при записи файлов: {e}")
        sys.exit(1)

    print("\n--- Проверка дешифровки ---")
    decrypted_text = decrypt(encrypted_text)
    print(decrypted_text)
    print("-" * 27)


if __name__ == "__main__":
    main()