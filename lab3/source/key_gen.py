import os
import json
import argparse
from typing import Dict, Any

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes


def load_config(path: str) -> Dict[str, Any]:
    """
    Загружает JSON-конфигурацию.

    :param path: путь к JSON файлу
    :return: словарь с конфигурацией
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_cast5_key(size_bytes: int) -> bytes:
    """
    Генерирует ключ для CAST5.

    :param size_bytes: размер ключа в байтах (5–16)
    :return: случайный ключ
    :raises ValueError: если размер вне диапазона
    """
    if not (5 <= size_bytes <= 16):
        raise ValueError("CAST5 key must be 5–16 bytes")
    return os.urandom(size_bytes)


def generate_rsa_keys() -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """
    Генерирует пару RSA ключей.

    :return: (private_key, public_key)
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    return private_key, private_key.public_key()


def save_private_key(private_key: rsa.RSAPrivateKey, path: str) -> None:
    """
    Сохраняет приватный ключ в PEM.

    :param private_key: приватный RSA ключ
    :param path: путь для сохранения
    """
    with open(path, "wb") as f:
        f.write(private_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption()
        ))


def save_public_key(public_key: rsa.RSAPublicKey, path: str) -> None:
    """
    Сохраняет публичный ключ в PEM.

    :param public_key: публичный RSA ключ
    :param path: путь для сохранения
    """
    with open(path, "wb") as f:
        f.write(public_key.public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo
        ))


def encrypt_symmetric_key(
    public_key: rsa.RSAPublicKey,
    symmetric_key: bytes
) -> bytes:
    """
    Шифрует симметричный ключ с помощью RSA-OAEP.

    :param public_key: публичный RSA ключ
    :param symmetric_key: симметричный ключ
    :return: зашифрованный ключ
    """
    return public_key.encrypt(
        symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )


def save_bytes(data: bytes, path: str) -> None:
    """
    Сохраняет байты в файл.

    :param data: данные
    :param path: путь
    """
    with open(path, "wb") as f:
        f.write(data)


def run(config: Dict[str, Any]) -> None:
    """
    Выполняет генерацию ключей гибридной системы.

    :param config: конфигурация из JSON
    """
    print("[*] Генерация ключей")

    sym_key = generate_cast5_key(config["key_size"])
    private_key, public_key = generate_rsa_keys()

    save_private_key(private_key, config["secret_key"])
    save_public_key(public_key, config["public_key"])

    encrypted_sym_key = encrypt_symmetric_key(public_key, sym_key)
    save_bytes(encrypted_sym_key, config["symmetric_key"])

    print("[+] Готово")


def parse_args() -> argparse.Namespace:
    """
    Парсит аргументы CLI.

    :return: namespace с аргументами
    """
    parser = argparse.ArgumentParser(description="Hybrid crypto key generator")
    parser.add_argument(
        "--config",
        required=True,
        help="Путь к JSON конфигу"
    )
    return parser.parse_args()


def main() -> None:
    """
    Точка входа CLI.
    """
    args = parse_args()
    config = load_config(args.config)
    run(config)


if __name__ == "__main__":
    main()