#!/usr/bin/env python3

import argparse


def arg_parse() -> argparse.Namespace:
    """Парсинг аргументов командной строки для шифрования/дешифрования."""
    parser = argparse.ArgumentParser(
        prog="vigenere",
        description="Encrypt or decrypt text using a cipher",
    )
    parser.add_argument("filename", help="Input file")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("-e", "--encrypt", action="store_true", help="Encrypt input file")
    mode.add_argument("-d", "--decrypt", action="store_true", help="Decrypt input file")
    parser.add_argument("-k", "--key", required=True, help="Encryption key")
    parser.add_argument("-o", "--output", required=True, help="Output file")
    return parser.parse_args()


def read_file(filename: str) -> str:
    """Чтение содержимого файла и возврат как строки."""
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def write_file(filename: str, data: str) -> None:
    """Запись строки data в файл filename."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(data)


def encrypt_vigenere(plaintext: str, key: str) -> str:
    """Шифрование текста шифром Виженера."""
    plaintext = plaintext.upper()
    key = key.upper()
    ciphertext = ""
    key_index = 0

    for char in plaintext:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord("A")
            encrypted_char = chr((ord(char) - ord("A") + shift) % 26 + ord("A"))
            ciphertext += encrypted_char
            key_index += 1
        else:
            ciphertext += char
    return ciphertext


def decrypt_vigenere(ciphertext: str, key: str) -> str:
    """Дешифрование текста шифром Виженера."""
    ciphertext = ciphertext.upper()
    key = key.upper()
    plaintext = ""
    key_index = 0

    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord("A")
            decrypted_char = chr((ord(char) - ord("A") - shift + 26) % 26 + ord("A"))
            plaintext += decrypted_char
            key_index += 1
        else:
            plaintext += char
    return plaintext


def main() -> None:
    """Основная функция программы."""
    args = arg_parse()
    key = args.key
    data = read_file(args.filename)
    result = ""
    if args.encrypt:
        result = encrypt_vigenere(data, key)
    elif args.decrypt:
        result = decrypt_vigenere(data, key)
    write_file(args.output, result)


if __name__ == "__main__":
    main()