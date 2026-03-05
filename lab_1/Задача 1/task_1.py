import argparse
from constants_task_1 import (ORIGINAL_TEXT_PATH, KEY_PATH, ENCRYPT_TEXT_PATH,
                              DECRYPT_TEXT_PATH, RU_LOWER, EN_LOWER)
import sys

def caesar_cipher(text, shift, mode='encrypt'):
    """
    Шифр Цезаря для русского и английского алфавитов
    :param text: Исходный текст, который необходимо зашифровать или дешифровать
    :param shift: Ключ, определяющий величину сдвига символов в алфавите
    :param mode: Режим работы: 'encrypt' для шифрования,'decrypt' для дешифрования
    :return: Строка с примененным сдвигом
    """
    if mode == 'decrypt':
        shift = -shift

    ru_upper = RU_LOWER.upper()
    en_upper = EN_LOWER.upper()

    result = []

    for char in text:
        if char in RU_LOWER:
            index = (RU_LOWER.find(char) + shift) % len(RU_LOWER)
            result.append(RU_LOWER[index])
        elif char in ru_upper:
            index = (ru_upper.find(char) + shift) % len(ru_upper)
            result.append(ru_upper[index])
        elif char in EN_LOWER:
            index = (EN_LOWER.find(char) + shift) % len(EN_LOWER)
            result.append(EN_LOWER[index])
        elif char in en_upper:
            index = (en_upper.find(char) + shift) % len(en_upper)
            result.append(en_upper[index])
        else:
            result.append(char)

    return "".join(result)

def parse_args() -> argparse.Namespace:
    """
    Разбор аргументов командной строки
    :return: аргументы командной строки
    """

    p = argparse.ArgumentParser()

    p.add_argument("-o",
                   "--original_text_path",
                   default=ORIGINAL_TEXT_PATH,
                   help="Путь к оригинальному тексту")

    p.add_argument("-k",
                   "--key_value",
                   required=True,
                   help="Ключ для шифра Цезаря")

    p.add_argument("-kp",
                   "--key_path",
                   default=KEY_PATH,
                   help="Путь для сохранения значения ключа")

    p.add_argument("-e",
                   "--encrypt_text_path",
                   default=ENCRYPT_TEXT_PATH,
                   help="Путь для сохранения зашифрованного текста")

    p.add_argument("-d",
                   "--decrypt_text_path",
                   default=DECRYPT_TEXT_PATH,
                   help="Путь для сохранения дешифрованного текста")

    return p.parse_args()

def main():
    args = parse_args()

    try:
        with open(args.original_text_path, "r") as f:
            original_text = f.read()
    except FileNotFoundError:
        print(f"File path {args.original_text_path} was not found")
        sys.exit(1)

    encrypted_text = caesar_cipher(original_text, int(args.key_value), mode='encrypt')

    try:
        with open(args.encrypt_text_path, 'w', encoding='utf-8') as f:
            f.write(encrypted_text)
    except IOError:
        print(f"Error writing to a file {args.encrypt_text_path} ")
        sys.exit(1)

    try:
        with open(args.key_path, 'w', encoding='utf-8') as f:
            f.write(str(args.key_value))
    except IOError:
        print(f"Error writing to a file {args.key_path} ")
        sys.exit(1)

    decrypted_text = caesar_cipher(encrypted_text, int(args.key_value), mode='decrypt')

    if original_text == decrypted_text:
        print("Исходный текст успешно зашифрован и дешифрован")

    else:
        print("Дешифрованный текст не совпадает с исходным текстом")
        try:
            with open(args.decrypt_text_path, 'w', encoding='utf-8') as f:
                f.write(decrypted_text)
        except IOError:
            print(f"Error writing to a file {args.decrypt_text_path} ")
            sys.exit(1)

if __name__ == "__main__":
    main()