import sys
import argparse
from file_utils import (
    load_config, get_rsa_private_file, get_rsa_public_file,
    get_cast5_key_file, get_encrypted_cast5_key_file, get_key_files,
    get_cast5_default_key_len, get_cast5_min_key_len, get_cast5_max_key_len,
    get_cast5_key_step, get_rsa_key_size,
    save_bytes, load_bytes, file_exists, check_keys_exist, validate_key_length
)
from cast5_operations import generate_cast5_key, encrypt_cast5_file, decrypt_cast5_file
from rsa_operations import generate_rsa_keys, encrypt_with_rsa_public_key, decrypt_with_rsa_private_key

load_config()


def mode_gen(keylen: int) -> None:
    """Генерация ключей."""
    print(f"Генерация ключей CAST-5 ({keylen} бит):")
    cast5_key = generate_cast5_key(keylen)
    save_bytes(cast5_key, get_cast5_key_file())
    print(f"  -> {get_cast5_key_file()} ({len(cast5_key)} байт)")

    print(f"Генерация ключей RSA ({get_rsa_key_size()} бит):")
    rsa_priv, rsa_pub = generate_rsa_keys()
    save_bytes(rsa_priv, get_rsa_private_file())
    save_bytes(rsa_pub, get_rsa_public_file())
    print(f"  -> {get_rsa_private_file()}")
    print(f"  -> {get_rsa_public_file()}")

    print("Шифрование ключа CAST-5 открытым RSA:")
    encrypted = encrypt_with_rsa_public_key(cast5_key, rsa_pub)
    save_bytes(encrypted, get_encrypted_cast5_key_file())
    print(f"  -> {get_encrypted_cast5_key_file()}")


def mode_enc(in_file: str, out_file: str) -> None:
    """Шифрование файла."""
    if not file_exists(in_file):
        print(f"Ошибка: файл {in_file} не найден")
        sys.exit(1)

    all_exist, missing = check_keys_exist()
    if not all_exist:
        print(f"Ошибка: отсутствуют ключи: {missing}")
        print(f"Запустите: python main.py -gen --keylen {get_cast5_default_key_len()}")
        sys.exit(1)

    rsa_priv = load_bytes(get_rsa_private_file())
    enc_cast5 = load_bytes(get_encrypted_cast5_key_file())
    cast5_key = decrypt_with_rsa_private_key(enc_cast5, rsa_priv)

    encrypt_cast5_file(in_file, out_file, cast5_key)
    print(f"Зашифрован: {in_file} -> {out_file}")


def mode_dec(in_file: str, out_file: str) -> None:
    """Расшифрование файла."""
    if not file_exists(in_file):
        print(f"Ошибка: файл {in_file} не найден")
        sys.exit(1)

    all_exist, missing = check_keys_exist()
    if not all_exist:
        print(f"Ошибка: отсутствуют ключи: {missing}")
        print(f"Запустите: python main.py -gen --keylen {get_cast5_default_key_len()}")
        sys.exit(1)

    rsa_priv = load_bytes(get_rsa_private_file())
    enc_cast5 = load_bytes(get_encrypted_cast5_key_file())
    cast5_key = decrypt_with_rsa_private_key(enc_cast5, rsa_priv)

    decrypt_cast5_file(in_file, out_file, cast5_key)
    print(f"Расшифрован: {in_file} -> {out_file}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Гибридная криптосистема RSA + CAST-5")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generation', action='store_true', help='Генерация ключей')
    group.add_argument('-enc', '--encryption', action='store_true', help='Шифрование файла')
    group.add_argument('-dec', '--decryption', action='store_true', help='Расшифрование файла')

    default_len = get_cast5_default_key_len()
    min_len = get_cast5_min_key_len()
    max_len = get_cast5_max_key_len()
    step = get_cast5_key_step()

    parser.add_argument('--keylen', type=int, default=default_len,
                        help=f'Длина ключа CAST-5 ({min_len}-{max_len}, кратно {step})')
    parser.add_argument('--input', '-i', type=str, help='Входной файл')
    parser.add_argument('--output', '-o', type=str, help='Выходной файл')

    args = parser.parse_args()

    # Определяем режим через match-case
    match (args.generation, args.encryption, args.decryption):
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