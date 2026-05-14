import sys
import argparse
from file_utils import save_bytes, load_bytes, file_exists, get_file_size
from cast5_operations import generate_key, encrypt_file, decrypt_file
from rsa_operations import generate_keys, encrypt_with_public_key, decrypt_with_private_key

# Имена файлов для хранения ключей
RSA_PRIVATE = "rsa_private.pem"           # Закрытый ключ RSA
RSA_PUBLIC = "rsa_public.pem"             # Открытый ключ RSA
CAST5_KEY = "cast5_key.bin"               # Симметричный ключ CAST-5
ENCRYPTED_CAST5_KEY = "encrypted_cast5_key.bin"  # CAST-5 ключ, зашифрованный RSA


def check_keys() -> bool:
    """
    Проверяет наличие всех необходимых файлов ключей.

    Returns:
        bool: True если все ключи существуют, False в противном случае.
    """
    required = [RSA_PRIVATE, RSA_PUBLIC, CAST5_KEY, ENCRYPTED_CAST5_KEY]
    missing = [f for f in required if not file_exists(f)]

    if missing:
        print("Ошибка: отсутствуют файлы ключей:", ", ".join(missing))
        print("Запустите: python main.py -gen --keylen 128")
        return False
    return True


def load_keys() -> tuple:
    """
    Загружает все ключи из файлов.

    Returns:
        tuple: (rsa_private, rsa_public, cast5_key, encrypted_cast5_key) в виде байтов.

    Raises:
        FileNotFoundError: Если какой-либо из файлов ключей не найден.
    """
    return (
        load_bytes(RSA_PRIVATE),
        load_bytes(RSA_PUBLIC),
        load_bytes(CAST5_KEY),
        load_bytes(ENCRYPTED_CAST5_KEY)
    )


def mode_gen(keylen: int) -> None:
    """
    Режим генерации ключей.

    Генерирует:
        1. Ключ CAST-5 заданной длины
        2. Пару RSA-ключей (2048 бит)
        3. Зашифрованный открытым RSA ключ CAST-5

    Args:
        keylen (int): Длина ключа CAST-5 в битах (40-128, кратно 8).

    Returns:
        None
    """
    print(f"Генерация ключей CAST-5 ({keylen} бит):")
    cast5_key = generate_key(keylen)
    save_bytes(cast5_key, CAST5_KEY)
    print(f"  -> {CAST5_KEY} ({len(cast5_key)} байт)")

    print("Генерация ключей RSA (2048 бит):")
    rsa_priv, rsa_pub = generate_keys()
    save_bytes(rsa_priv, RSA_PRIVATE)
    save_bytes(rsa_pub, RSA_PUBLIC)
    print(f"  -> {RSA_PRIVATE}")
    print(f"  -> {RSA_PUBLIC}")

    print("Шифрование ключа CAST-5 открытым RSA:")
    encrypted = encrypt_with_public_key(cast5_key, rsa_pub)
    save_bytes(encrypted, ENCRYPTED_CAST5_KEY)
    print(f"  -> {ENCRYPTED_CAST5_KEY}")


def mode_enc(in_file: str, out_file: str) -> None:
    """
    Режим шифрования файла.

    Процесс:
        1. Проверяет наличие входного файла
        2. Проверяет наличие всех ключей
        3. Расшифровывает ключ CAST-5 через RSA
        4. Шифрует файл алгоритмом CAST-5

    Args:
        in_file (str): Путь к исходному файлу для шифрования.
        out_file (str): Путь для сохранения зашифрованного файла.

    Returns:
        None
    """
    if not file_exists(in_file):
        print(f"Ошибка: файл {in_file} не найден")
        sys.exit(1)

    if not check_keys():
        sys.exit(1)

    rsa_priv, _, _, enc_cast5 = load_keys()
    cast5_key = decrypt_with_private_key(enc_cast5, rsa_priv)

    encrypt_file(in_file, out_file, cast5_key)
    print(f"Зашифрован: {in_file} -> {out_file}")


def mode_dec(in_file: str, out_file: str) -> None:
    """
    Режим расшифрования файла.

    Процесс:
        1. Проверяет наличие входного файла
        2. Проверяет наличие всех ключей
        3. Расшифровывает ключ CAST-5 через RSA
        4. Расшифровывает файл алгоритмом CAST-5

    Args:
        in_file (str): Путь к зашифрованному файлу.
        out_file (str): Путь для сохранения расшифрованного файла.

    Returns:
        None
    """
    if not file_exists(in_file):
        print(f"Ошибка: файл {in_file} не найден")
        sys.exit(1)

    if not check_keys():
        sys.exit(1)

    rsa_priv, _, _, enc_cast5 = load_keys()
    cast5_key = decrypt_with_private_key(enc_cast5, rsa_priv)

    decrypt_file(in_file, out_file, cast5_key)
    print(f"Расшифрован: {in_file} -> {out_file}")


def main() -> None:
    """
    Главная функция, обрабатывающая аргументы командной строки.

    Поддерживает три режима работы:
        -gen   : генерация ключей (с опцией --keylen)
        -enc   : шифрование файла (с опциями --input и --output)
        -dec   : расшифрование файла (с опциями --input и --output)

    Returns:
        None
    """
    parser = argparse.ArgumentParser(
        description="Гибридная криптосистема RSA + CAST-5"
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generation', action='store_true',
                       help='Генерация ключей')
    group.add_argument('-enc', '--encryption', action='store_true',
                       help='Шифрование файла')
    group.add_argument('-dec', '--decryption', action='store_true',
                       help='Расшифрование файла')

    parser.add_argument('--keylen', type=int, default=128,
                        help='Длина ключа CAST-5 (40-128, кратно 8)')
    parser.add_argument('--input', '-i', type=str,
                        help='Входной файл')
    parser.add_argument('--output', '-o', type=str,
                        help='Выходной файл')

    args = parser.parse_args()

    # Режим генерации ключей
    if args.generation:
        if args.keylen < 40 or args.keylen > 128 or args.keylen % 8 != 0:
            print("Ошибка: длина ключа должна быть 40-128, кратно 8")
            sys.exit(1)
        mode_gen(args.keylen)

    # Режим шифрования
    elif args.encryption:
        if not args.input or not args.output:
            print("Ошибка: укажите --input и --output")
            sys.exit(1)
        mode_enc(args.input, args.output)

    # Режим расшифрования
    elif args.decryption:
        if not args.input or not args.output:
            print("Ошибка: укажите --input и --output")
            sys.exit(1)
        mode_dec(args.input, args.output)


if __name__ == "__main__":
    main()