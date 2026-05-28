import sys
import argparse
from constants import (
    RSA_PRIVATE_FILE, RSA_PUBLIC_FILE, CAST5_KEY_FILE, ENCRYPTED_CAST5_KEY_FILE,
    KEY_FILES, CAST5_DEFAULT_KEY_LEN, CAST5_MIN_KEY_LEN, CAST5_MAX_KEY_LEN,
    CAST5_KEY_STEP
)
from file_utils import save_bytes, load_bytes, file_exists, check_keys_exist, validate_key_length
from cast5_operations import generate_cast5_key, encrypt_cast5_file, decrypt_cast5_file
from rsa_operations import generate_rsa_keys, encrypt_with_rsa_public_key, decrypt_with_rsa_private_key


def mode_gen(keylen: int) -> None:
    """Генерация ключей."""
    print(f"Генерация ключей CAST-5 ({keylen} бит):")
    cast5_key = generate_cast5_key(keylen)
    save_bytes(cast5_key, CAST5_KEY_FILE)
    print(f"  -> {CAST5_KEY_FILE} ({len(cast5_key)} байт)")

    print("Генерация ключей RSA (2048 бит):")
    rsa_priv, rsa_pub = generate_rsa_keys()
    save_bytes(rsa_priv, RSA_PRIVATE_FILE)
    save_bytes(rsa_pub, RSA_PUBLIC_FILE)
    print(f"  -> {RSA_PRIVATE_FILE}")
    print(f"  -> {RSA_PUBLIC_FILE}")

    print("Шифрование ключа CAST-5 открытым RSA:")
    encrypted = encrypt_with_rsa_public_key(cast5_key, rsa_pub)
    save_bytes(encrypted, ENCRYPTED_CAST5_KEY_FILE)
    print(f"  -> {ENCRYPTED_CAST5_KEY_FILE}")


def mode_enc(in_file: str, out_file: str) -> None:
    """Шифрование файла."""
    if not file_exists(in_file):
        print(f"Ошибка: файл {in_file} не найден")
        sys.exit(1)

    all_exist, missing = check_keys_exist(KEY_FILES)
    if not all_exist:
        print(f"Ошибка: отсутствуют ключи: {missing}")
        print(f"Запустите: python main.py -gen --keylen {CAST5_DEFAULT_KEY_LEN}")
        sys.exit(1)

    rsa_priv = load_bytes(RSA_PRIVATE_FILE)
    enc_cast5 = load_bytes(ENCRYPTED_CAST5_KEY_FILE)
    cast5_key = decrypt_with_rsa_private_key(enc_cast5, rsa_priv)

    encrypt_cast5_file(in_file, out_file, cast5_key)
    print(f"Зашифрован: {in_file} -> {out_file}")


def mode_dec(in_file: str, out_file: str) -> None:
    """Расшифрование файла."""
    if not file_exists(in_file):
        print(f"Ошибка: файл {in_file} не найден")
        sys.exit(1)

    all_exist, missing = check_keys_exist(KEY_FILES)
    if not all_exist:
        print(f"Ошибка: отсутствуют ключи: {missing}")
        print(f"Запустите: python main.py -gen --keylen {CAST5_DEFAULT_KEY_LEN}")
        sys.exit(1)

    rsa_priv = load_bytes(RSA_PRIVATE_FILE)
    enc_cast5 = load_bytes(ENCRYPTED_CAST5_KEY_FILE)
    cast5_key = decrypt_with_rsa_private_key(enc_cast5, rsa_priv)

    decrypt_cast5_file(in_file, out_file, cast5_key)
    print(f"Расшифрован: {in_file} -> {out_file}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Гибридная криптосистема RSA + CAST-5")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generation', action='store_true', help='Генерация ключей')
    group.add_argument('-enc', '--encryption', action='store_true', help='Шифрование файла')
    group.add_argument('-dec', '--decryption', action='store_true', help='Расшифрование файла')

    parser.add_argument('--keylen', type=int, default=CAST5_DEFAULT_KEY_LEN,
                        help=f'Длина ключа CAST-5 ({CAST5_MIN_KEY_LEN}-{CAST5_MAX_KEY_LEN}, кратно {CAST5_KEY_STEP})')
    parser.add_argument('--input', '-i', type=str, help='Входной файл')
    parser.add_argument('--output', '-o', type=str, help='Выходной файл')

    args = parser.parse_args()

    match (
        args.generation,
        args.encryption,
        args.decryption
    ):
        case (True, False, False):
            mode = "gen"
        case (False, True, False):
            mode = "enc"
        case (False, False, True):
            mode = "dec"
        case _:
            mode = None

    match mode:
        case "gen":
            try:
                validate_key_length(args.keylen)
            except ValueError as e:
                print(f"Ошибка: {e}")
                sys.exit(1)
            mode_gen(args.keylen)

        case "enc":
            if not args.input or not args.output:
                print("Ошибка: укажите --input и --output")
                sys.exit(1)
            mode_enc(args.input, args.output)

        case "dec":
            if not args.input or not args.output:
                print("Ошибка: укажите --input и --output")
                sys.exit(1)
            mode_dec(args.input, args.output)

        case _:
            print("Ошибка: не выбран режим работы")
            sys.exit(1)


if __name__ == "__main__":
    main()