import argparse
import json

from crypto_utils import *


def load_settings(path="settings.json"):

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_keys(settings):

    print("[+] Генерация ключа CAST5...")

    key_size = settings["cast5_key_size"]

    symmetric_key = generate_cast5_key(key_size)

    print("[+] Генерация RSA ключей...")

    private_key, public_key = generate_rsa_keys()

    print("[+] Сохранение RSA ключей...")

    save_private_key(
        private_key,
        settings["private_key"]
    )

    save_public_key(
        public_key,
        settings["public_key"]
    )

    print("[+] Шифрование симметричного ключа RSA...")

    encrypted_sym_key = encrypt_symmetric_key(
        symmetric_key,
        public_key
    )

    with open(settings["encrypted_symmetric_key"], "wb") as f:
        f.write(encrypted_sym_key)

    print("[+] Ключи успешно созданы")

def encrypt_data(settings):

    print("[+] Загрузка RSA private key...")

    private_key = load_private_key(
        settings["private_key"]
    )

    print("[+] Загрузка зашифрованного симметричного ключа...")

    with open(settings["encrypted_symmetric_key"], "rb") as f:
        encrypted_key = f.read()

    print("[+] Расшифрование симметричного ключа...")

    symmetric_key = decrypt_symmetric_key(
        encrypted_key,
        private_key
    )

    print("[+] Шифрование файла CAST5...")

    encrypt_file_cast5(
        settings["initial_file"],
        settings["encrypted_file"],
        symmetric_key
    )

    print("[+] Файл успешно зашифрован")

def decrypt_data(settings):

    print("[+] Загрузка RSA private key...")

    private_key = load_private_key(
        settings["private_key"]
    )

    print("[+] Загрузка зашифрованного симметричного ключа...")

    with open(settings["encrypted_symmetric_key"], "rb") as f:
        encrypted_key = f.read()

    print("[+] Расшифрование симметричного ключа...")

    symmetric_key = decrypt_symmetric_key(
        encrypted_key,
        private_key
    )

    print("[+] Дешифрование файла CAST5...")

    decrypt_file_cast5(
        settings["encrypted_file"],
        settings["decrypted_file"],
        symmetric_key
    )

    print("[+] Файл успешно расшифрован")

def main():

    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(
        required=True
    )

    group.add_argument(
        "-gen",
        "--generation",
        action="store_true",
        help="Генерация ключей"
    )

    group.add_argument(
        "-enc",
        "--encryption",
        action="store_true",
        help="Шифрование"
    )

    group.add_argument(
        "-dec",
        "--decryption",
        action="store_true",
        help="Дешифрование"
    )

    parser.add_argument(
        "-s",
        "--settings",
        default="settings.json",
        help="Путь к settings.json"
    )

    args = parser.parse_args()

    settings = load_settings(args.settings)

    if args.generation:
        generate_keys(settings)

    elif args.encryption:
        encrypt_data(settings)

    elif args.decryption:
        decrypt_data(settings)


if __name__ == "__main__":
    main()