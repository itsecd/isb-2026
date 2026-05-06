import json
import os
import argparse
from typing import Any, Dict

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes


def load_config(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_symmetric_key(key_size_bytes: int) -> bytes:
    return os.urandom(key_size_bytes)


def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    return private_key, private_key.public_key()


def save_bytes(path: str, data: bytes) -> None:
    with open(path, "wb") as f:
        f.write(data)


def save_private_key(private_key, path: str) -> None:
    with open(path, "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )


def save_public_key(public_key, path: str) -> None:
    with open(path, "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )


def encrypt_symmetric_key(sym_key: bytes, public_key) -> bytes:
    return public_key.encrypt(
        sym_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def run(config: Dict[str, Any]) -> None:
    print("[*] Генерация ключей")

    # симметричный ключ (ВАЖНО: у тебя key_size уже в БАЙТАХ)
    sym_key = generate_symmetric_key(config["key_size"])

    private_key, public_key = generate_rsa_keys()

    save_private_key(private_key, config["secret_key"])
    save_public_key(public_key, config["public_key"])

    encrypted_sym_key = encrypt_symmetric_key(sym_key, public_key)

    save_bytes(config["symmetric_key"], encrypted_sym_key)

    print("[+] Готово")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    config = load_config(args.config)
    run(config)


if __name__ == "__main__":
    main()