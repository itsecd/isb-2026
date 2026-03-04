from constants import *


def encrypt(text: str, alphabet: str, key: str) -> str:
    """
    Шифрует текст с использованием моноалфавитной подстановки.

    :param text: исходный текст
    :param alphabet: исходный алфавит
    :param key: ключ подстановки
    :return: зашифрованный текст
    """
    result = ""
    for char in text:
        if char in alphabet:
            index = alphabet.index(char)
            result += key[index]
        else:
            result += char
    return result


def decrypt(text: str, alphabet: str, key: str) -> str:
    """
    Дешифрует текст с использованием моноалфавитной подстановки.

    :param text: зашифрованный текст
    :param alphabet: исходный алфавит
    :param key: ключ подстановки
    :return: расшифрованный текст
    """
    result = ""
    for char in text:
        if char in key:
            index = key.index(char)
            result += alphabet[index]
        else:
            result += char
    return result


def main() -> None:
    """
    Основная функция программы.
    """
    try:
        with open(TASK1_INPUT, "r", encoding="utf-8") as f:
            text = f.read()

        encrypted_text = encrypt(text, ALPHABET, FIXED_KEY)

        with open(TASK1_ENC_OUTPUT, "w", encoding="utf-8") as f:
            f.write(encrypted_text)

        decrypted_text = decrypt(encrypted_text, ALPHABET, FIXED_KEY)

        with open(TASK1_DEC_OUTPUT, "w", encoding="utf-8") as f:
            f.write(decrypted_text)

        with open(TASK1_KEY_OUTPUT, "w", encoding="utf-8") as f:
            f.write(FIXED_KEY)

        if text == decrypted_text:
            print("Дешифрование выполнено корректно.")
        else:
            print("Ошибка при дешифровании.")

    except FileNotFoundError as e:
        print(f"Файл не найден: {e}")
    except IOError as e:
        print(f"Ошибка работы с файлом: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()