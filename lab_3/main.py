import argparse
import json
import os
from pathlib import Path

from cryptography.hazmat.primitives import hashes, padding as sym_padding, serialization
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding, rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from cryptography.hazmat.primitives.ciphers import Cipher, modes

try:
    from cryptography.hazmat.decrepit.ciphers.algorithms import TripleDES
except ImportError: 
    from cryptography.hazmat.primitives.ciphers.algorithms import TripleDES


ALLOWED_3DES_KEY_BITS = {64, 128, 192}
BLOCK_BITS = 64
IV_SIZE = 8


def read_config(path: str | None) -> dict:
    if not path:
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def pick(args, config: dict, name: str, required: bool = True, default=None):
    value = getattr(args, name, None)
    if value is None:
        value = config.get(name, default)
    if required and value is None:
        raise ValueError(f'Не указан параметр: {name}')
    return value


def ensure_parent(path: str) -> None:
    parent = Path(path).expanduser().resolve().parent
    parent.mkdir(parents=True, exist_ok=True)


def generate_3des_key(key_bits: int) -> bytes:
    if key_bits not in ALLOWED_3DES_KEY_BITS:
        raise ValueError('Для 3DES допустимы только 64, 128 или 192 бит')
    return os.urandom(key_bits // 8)


def load_private_key(path: str):
    with open(path, 'rb') as f:
        return load_pem_private_key(f.read(), password=None)


def load_public_key(path: str):
    with open(path, 'rb') as f:
        return load_pem_public_key(f.read())


def rsa_encrypt(public_key, data: bytes) -> bytes:
    return public_key.encrypt(
        data,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def rsa_decrypt(private_key, data: bytes) -> bytes:
    return private_key.decrypt(
        data,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def decrypt_symmetric_key(private_key_path: str, encrypted_key_path: str) -> bytes:
    private_key = load_private_key(private_key_path)
    with open(encrypted_key_path, 'rb') as f:
        encrypted_key = f.read()
    return rsa_decrypt(private_key, encrypted_key)


def encrypt_3des(plaintext: bytes, key: bytes) -> bytes:
    iv = os.urandom(IV_SIZE)
    padder = sym_padding.PKCS7(BLOCK_BITS).padder()
    padded = padder.update(plaintext) + padder.finalize()
    cipher = Cipher(TripleDES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded) + encryptor.finalize()
    return iv + ciphertext


def decrypt_3des(encrypted: bytes, key: bytes) -> bytes:
    if len(encrypted) < IV_SIZE:
        raise ValueError('Файл слишком короткий: отсутствует IV')
    iv, ciphertext = encrypted[:IV_SIZE], encrypted[IV_SIZE:]
    cipher = Cipher(TripleDES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = sym_padding.PKCS7(BLOCK_BITS).unpadder()
    return unpadder.update(padded) + unpadder.finalize()


def generation(args, config: dict) -> None:
    encrypted_symmetric_key = pick(args, config, 'encrypted_symmetric_key')
    public_key_path = pick(args, config, 'public_key')
    private_key_path = pick(args, config, 'private_key')
    key_bits = int(pick(args, config, 'key_bits', required=False, default=192))

    print('[1/5] Генерация симметричного ключа 3DES...')
    symmetric_key = generate_3des_key(key_bits)

    print('[2/5] Генерация RSA-ключей...')
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    print('[3/5] Сериализация RSA-ключей...')
    ensure_parent(public_key_path)
    ensure_parent(private_key_path)
    with open(public_key_path, 'wb') as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ))
    with open(private_key_path, 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))

    print('[4/5] Шифрование симметричного ключа открытым RSA-ключом...')
    encrypted_key = rsa_encrypt(public_key, symmetric_key)

    print('[5/5] Сохранение зашифрованного симметричного ключа...')
    ensure_parent(encrypted_symmetric_key)
    with open(encrypted_symmetric_key, 'wb') as f:
        f.write(encrypted_key)

    print('Готово: ключи гибридной системы сгенерированы.')


def encryption(args, config: dict) -> None:
    input_file = pick(args, config, 'input_file')
    private_key_path = pick(args, config, 'private_key')
    encrypted_symmetric_key = pick(args, config, 'encrypted_symmetric_key')
    output_file = pick(args, config, 'output_file')

    print('[1/3] Расшифровка симметричного ключа...')
    symmetric_key = decrypt_symmetric_key(private_key_path, encrypted_symmetric_key)

    print('[2/3] Чтение и шифрование файла алгоритмом 3DES/CBC...')
    with open(input_file, 'rb') as f:
        plaintext = f.read()
    encrypted = encrypt_3des(plaintext, symmetric_key)

    print('[3/3] Сохранение зашифрованного файла...')
    ensure_parent(output_file)
    with open(output_file, 'wb') as f:
        f.write(encrypted)

    print('Готово: файл зашифрован.')


def decryption(args, config: dict) -> None:
    input_file = pick(args, config, 'input_file')
    private_key_path = pick(args, config, 'private_key')
    encrypted_symmetric_key = pick(args, config, 'encrypted_symmetric_key')
    output_file = pick(args, config, 'output_file')

    print('[1/3] Расшифровка симметричного ключа...')
    symmetric_key = decrypt_symmetric_key(private_key_path, encrypted_symmetric_key)

    print('[2/3] Чтение и дешифрование файла алгоритмом 3DES/CBC...')
    with open(input_file, 'rb') as f:
        encrypted = f.read()
    plaintext = decrypt_3des(encrypted, symmetric_key)

    print('[3/3] Сохранение расшифрованного файла...')
    ensure_parent(output_file)
    with open(output_file, 'wb') as f:
        f.write(plaintext)

    print('Готово: файл расшифрован.')


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Лабораторная №3: гибридная криптосистема RSA + 3DES')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generation', action='store_true', help='Режим генерации ключей')
    group.add_argument('-enc', '--encryption', action='store_true', help='Режим шифрования файла')
    group.add_argument('-dec', '--decryption', action='store_true', help='Режим дешифрования файла')

    parser.add_argument('-c', '--config', help='Путь к JSON-файлу настроек')
    parser.add_argument('--key-bits', type=int, choices=[64, 128, 192], help='Длина ключа 3DES: 64, 128 или 192 бит')
    parser.add_argument('--input-file', help='Входной файл для шифрования/дешифрования')
    parser.add_argument('--output-file', help='Выходной файл')
    parser.add_argument('--encrypted-symmetric-key', help='Файл с зашифрованным симметричным ключом')
    parser.add_argument('--public-key', help='Файл открытого RSA-ключа')
    parser.add_argument('--private-key', help='Файл закрытого RSA-ключа')
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    config = read_config(args.config)

    try:
        if args.generation:
            generation(args, config)
        elif args.encryption:
            encryption(args, config)
        else:
            decryption(args, config)
    except Exception as exc:
        print(f'Ошибка: {exc}')
        raise SystemExit(1)


if __name__ == '__main__':
    main()
