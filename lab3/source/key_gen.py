import json
from typing import Any, Dict

from CAST5 import generate_key
from RSA import encrypt, generate_keys, save_private_key, save_public_key


def load_config(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_bytes(data: bytes, path: str) -> None:
    with open(path, "wb") as f:
        f.write(data)


def run(config: Dict[str, Any]) -> None:
    print("[*] Генерация ключей")

    sym_key = generate_key(config["key_size"])
    private_key, public_key = generate_keys()

    save_private_key(private_key, config["secret_key"])
    save_public_key(public_key, config["public_key"])

    encrypted_sym_key = encrypt(sym_key, public_key)
    save_bytes(encrypted_sym_key, config["symmetric_key"])

    print("[+] Готово")