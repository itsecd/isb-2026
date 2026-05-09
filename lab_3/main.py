#!/usr/bin/env python3

import argparse
from typing import Any, Dict

from AES import encrypt as aes_encrypt
from AES import decrypt as aes_decrypt

from RSA import decrypt as rsa_decrypt
from RSA import load_private_key

from utils import load_config, read_bytes, write_bytes
from key_gen import generate_keys_pipeline


def decrypt_symmetric_key(secret_key_path: str, enc_key_path: str) -> bytes:
    """
    Расшифровывает симметричный AES ключ с помощью RSA.
    """
    private_key = load_private_key(secret_key_path)
    encrypted_key = read_bytes(enc_key_path)
    return rsa_decrypt(encrypted_key, private_key)


def encrypt_file(config: Dict[str, Any]) -> None:
    """
    Шифрует файл с использованием гибридной схемы RSA + AES.
    """
    print("[*] Encryption started")

    sym_key = decrypt_symmetric_key(
        config["secret_key"],
        config["symmetric_key"],
    )

    data = read_bytes(config["initial_file"])
    encrypted_data = aes_encrypt(sym_key, data)

    write_bytes(config["encrypted_file"], encrypted_data)

    print("[+] Encryption finished")


def decrypt_file(config: Dict[str, Any]) -> None:
    """
    Расшифровывает файл с использованием гибридной схемы RSA + AES.
    """
    print("[*] Decryption started")

    sym_key = decrypt_symmetric_key(
        config["secret_key"],
        config["symmetric_key"],
    )

    encrypted_data = read_bytes(config["encrypted_file"])
    decrypted_data = aes_decrypt(sym_key, encrypted_data)

    write_bytes(config["decrypted_file"], decrypted_data)

    print("[+] Decryption finished")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Hybrid RSA + AES crypto system")
    parser.add_argument("--config", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(f"{args.config}")
    config = load_config(args.config)

    print("[*] 1. Key generation")
    generate_keys_pipeline(config)

    print("[*] 2. File encryption")
    encrypt_file(config)

    print("[*] 3. File decryption")
    decrypt_file(config)

    print("[+] Full pipeline completed")


if __name__ == "__main__":
    main()