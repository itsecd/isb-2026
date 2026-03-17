import argparse
import sys
from typing import Dict, Tuple

from values import KEY_STRING, ALPHABET


def create_cipher_map(key: str) -> Tuple[Dict[str, str], Dict[str, str]]:
    """
    Создаёт словари для шифрования (прямая подстановка) и дешифрования (обратная).
    """
    if len(key) != len(ALPHABET) or set(key) != set(ALPHABET):
        raise ValueError("Ключ должен быть перестановкой всех букв русского алфавита")
    enc_lower: Dict[str, str] = dict(zip(ALPHABET, key))
    encrypt_map: Dict[str, str] = {}
    decrypt_map: Dict[str, str] = {}

    for low, enc_low in enc_lower.items():
        upper = low.upper()
        enc_upper = enc_low.upper()

        encrypt_map[low] = enc_low
        encrypt_map[upper] = enc_upper

        decrypt_map[enc_low] = low
        decrypt_map[enc_upper] = upper

    return encrypt_map, decrypt_map


def transform_text(text: str, mapping: Dict[str, str]) -> str:
    """
    Преобразует текст, заменяя символы согласно словарю.
    """
    return ''.join(mapping.get(ch, ch) for ch in text)


def main() -> None:
    """Основная функция: читает файл, шифрует, дешифрует и проверяет результат."""
    parser = argparse.ArgumentParser(description="Шифрование и дешифрование текста моноалфавитной заменой.")
    parser.add_argument('input_file', help='Имя файла с исходным текстом.')
    parser.add_argument('--key', default=KEY_STRING, help='Строка-ключ. По умолчанию: обратный порядок.')
    parser.add_argument('output', help='Имя файла для сохранения зашифрованного текста.')

    args = parser.parse_args()

    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            plaintext: str = f.read()
    except FileNotFoundError:
        print(f"Ошибка: файл '{args.input_file}' не найден.")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        sys.exit(1)

    try:
        encrypt_map, decrypt_map = create_cipher_map(args.key)
    except ValueError as e:
        print(f"Ошибка в ключе: {e}")
        sys.exit(1)

    ciphertext = transform_text(plaintext, encrypt_map)

    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(ciphertext)
        print(f"Зашифрованный текст сохранён в файл '{args.output}'.")
    except Exception as e:
        print(f"Ошибка при записи в файл: {e}")
        sys.exit(1)
    print("\nЗашифрованный текст:")
    print(ciphertext)

    decrypted_text: str = transform_text(ciphertext, decrypt_map)
    print("\nДешифрованный текст:")
    print(decrypted_text)

    if plaintext == decrypted_text:
        print("\nДешифрование выполнено успешно, текст совпадает с исходным.")
    else:
        print("\nОшибка: дешифрованный текст отличается от исходного.")


if __name__ == "__main__":
    main()
