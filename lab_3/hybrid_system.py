"""Сценарии работы гибридной криптосистемы RSA + 3DES."""

from file_utils import read_bytes, write_bytes
from rsa_utils import (
    decrypt_key,
    encrypt_key,
    generate_private_key,
    load_private_key,
    serialize_private_key,
    serialize_public_key,
)
from triple_des import generate_key, decrypt as decrypt_3des, encrypt as encrypt_3des


def generate_keys(
    encrypted_symmetric_key_path: str,
    public_key_path: str,
    private_key_path: str,
    key_bits: int,
) -> None:
    """Генерирует и сохраняет все ключи гибридной системы.

    Аргументы:
        encrypted_symmetric_key_path: Путь для сохранения RSA-зашифрованного ключа 3DES.
        public_key_path: Путь для сохранения открытого RSA-ключа.
        private_key_path: Путь для сохранения закрытого RSA-ключа.
        key_bits: Длина ключа 3DES в битах.
    """
    symmetric_key = generate_key(key_bits)
    private_key = generate_private_key()
    public_key = private_key.public_key()

    write_bytes(public_key_path, serialize_public_key(public_key))
    write_bytes(private_key_path, serialize_private_key(private_key))
    write_bytes(encrypted_symmetric_key_path, encrypt_key(symmetric_key, public_key))


def unwrap_symmetric_key(private_key_path: str, encrypted_symmetric_key_path: str) -> bytes:
    """Загружает и расшифровывает сохраненный ключ 3DES закрытым RSA-ключом."""
    private_key = load_private_key(read_bytes(private_key_path))
    encrypted_symmetric_key = read_bytes(encrypted_symmetric_key_path)
    return decrypt_key(encrypted_symmetric_key, private_key)


def encrypt_file(
    input_file_path: str,
    private_key_path: str,
    encrypted_symmetric_key_path: str,
    output_file_path: str,
) -> None:
    """Шифрует файл с помощью ранее сгенерированных ключей гибридной системы.

    По требованиям лабораторной этот сценарий расшифровывает сериализованный
    симметричный ключ закрытым RSA-ключом, а затем шифрует данные алгоритмом 3DES.
    """
    symmetric_key = unwrap_symmetric_key(private_key_path, encrypted_symmetric_key_path)
    plaintext = read_bytes(input_file_path)
    write_bytes(output_file_path, encrypt_3des(plaintext, symmetric_key))


def decrypt_file(
    input_file_path: str,
    private_key_path: str,
    encrypted_symmetric_key_path: str,
    output_file_path: str,
) -> None:
    """Расшифровывает файл с помощью ранее сгенерированных ключей гибридной системы."""
    symmetric_key = unwrap_symmetric_key(private_key_path, encrypted_symmetric_key_path)
    encrypted_payload = read_bytes(input_file_path)
    write_bytes(output_file_path, decrypt_3des(encrypted_payload, symmetric_key))
