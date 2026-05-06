import argparse
import json
from typing import Any, Dict

from CAST5 import decrypt as cast5_decrypt
from CAST5 import encrypt as cast5_encrypt
from RSA import decrypt as rsa_decrypt
from RSA import load_private_key
from utils import load_config, read_bytes, write_bytes
from key_gen import generate_keys_pipeline


def decrypt_sym_key(secret_key_path: str, sym_key_path: str) -> bytes:
    private_key = load_private_key(secret_key_path)
    encrypted_key = read_bytes(sym_key_path)
    return rsa_decrypt(encrypted_key, private_key)


def encrypt_file(config: Dict[str, Any]) -> None:
    print("[*] Шифрование")

    sym_key = decrypt_sym_key(
        config["secret_key"],
        config["symmetric_key"],
    )

    data = read_bytes(config["initial_file"])
    encrypted = cast5_encrypt(sym_key, data)

    write_bytes(config["encrypted_file"], encrypted)

    print("[+] Готово")


def decrypt_file(config: Dict[str, Any]) -> None:
    print("[*] Дешифрование")

    sym_key = decrypt_sym_key(
        config["secret_key"],
        config["symmetric_key"],
    )

    encrypted = read_bytes(config["encrypted_file"])
    decrypted = cast5_decrypt(sym_key, encrypted)

    write_bytes(config["decrypted_file"], decrypted)

    print("[+] Готово")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Hybrid crypto system")
    parser.add_argument("--config", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)

    print("[*] 1. Генерация ключей")
    generate_keys_pipeline(config)

    print("[*] 2. Шифрование файла")
    encrypt_file(config)

    print("[*] 3. Дешифрование файла")
    decrypt_file(config)

    print("[+] Полный цикл выполнен")

if __name__ == "__main__":
    main()