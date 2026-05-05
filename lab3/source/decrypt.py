import json
import argparse
from typing import Dict, Any

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey


def load_config(path: str) -> Dict[str, Any]:
    """
    Загружает JSON-конфигурацию.

    :param path: путь к JSON файлу
    :return: словарь конфигурации
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_private_key(path: str) -> RSAPrivateKey:
    """
    Загружает приватный RSA ключ из PEM файла.

    :param path: путь к файлу ключа
    :return: приватный ключ
    """
    with open(path, "rb") as f:
        return load_pem_private_key(f.read(), password=None)


def decrypt_sym_key(priv_path: str, sym_path: str) -> bytes:
    """
    Расшифровывает симметричный ключ с помощью RSA.

    :param priv_path: путь к приватному ключу
    :param sym_path: путь к зашифрованному симметричному ключу
    :return: симметричный ключ
    """
    private_key = load_private_key(priv_path)

    with open(sym_path, "rb") as f:
        encrypted_sym_key = f.read()

    return private_key.decrypt(
        encrypted_sym_key,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )


def decrypt_cast5(key: bytes, data: bytes) -> bytes:
    """
    Дешифрует данные с использованием CAST5 (CBC).

    :param key: симметричный ключ
    :param data: iv + ciphertext
    :return: исходные данные
    """
    iv: bytes = data[:8]
    ciphertext: bytes = data[8:]

    cipher = Cipher(algorithms.CAST5(key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = sym_padding.PKCS7(64).unpadder()
    return unpadder.update(padded_data) + unpadder.finalize()


def read_bytes(path: str) -> bytes:
    """
    Читает бинарные данные из файла.

    :param path: путь к файлу
    :return: содержимое файла
    """
    with open(path, "rb") as f:
        return f.read()


def write_bytes(path: str, data: bytes) -> None:
    """
    Записывает бинарные данные в файл.

    :param path: путь к файлу
    :param data: данные
    """
    with open(path, "wb") as f:
        f.write(data)


def run(config: Dict[str, Any]) -> None:
    """
    Выполняет дешифрование файла гибридной системой.

    :param config: конфигурация
    """
    print("[*] Дешифрование")

    sym_key = decrypt_sym_key(
        config["secret_key"],
        config["symmetric_key"]
    )

    encrypted_data = read_bytes(config["encrypted_file"])
    decrypted_data = decrypt_cast5(sym_key, encrypted_data)

    write_bytes(config["decrypted_file"], decrypted_data)

    print("[+] Готово")


def parse_args() -> argparse.Namespace:
    """
    Парсинг аргументов CLI.

    :return: namespace аргументов
    """
    parser = argparse.ArgumentParser(description="Hybrid crypto decryption")
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