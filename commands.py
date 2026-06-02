import os
import sys
import utilities
import RSA
import SM4
from utils import ensure_directory_exists, show_hex_dump, show_text


def load_config(settings_path: str) -> dict:
    """
    Загружает конфигурацию из JSON-файла.

    Args:
        settings_path (str): путь к JSON-файлу.

    Returns:
        dict: словарь с конфигурацией.
    """
    config = utilities.read_json(settings_path)
    if not config:
        print("[!] Не удалось загрузить конфигурацию.", file=sys.stderr)
        sys.exit(1)
    return config


def generate_rsa_keys(config: dict) -> None:
    """
    Генерирует RSA-ключи и сохраняет их в файлы, указанные в config.

    Args:
        config (dict): словарь конфигурации с ключами 'public_key' и 'secret_key'.
    """
    pub = config.get("public_key")
    priv = config.get("secret_key")
    if not pub or not priv:
        print("[!] В конфигурации отсутствуют пути для ключей.", file=sys.stderr)
        sys.exit(1)

    try:
        ensure_directory_exists(pub)
        ensure_directory_exists(priv)
        private_key, public_key = RSA.generate()
        utilities.serialize_private_key(priv, private_key)
        utilities.serialize_public_key(pub, public_key)
        print(f"[+] RSA-ключи сгенерированы:\n    Публичный: {pub}\n    Приватный: {priv}")
    except Exception as e:
        print(f"[!] Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


def encrypt_text(config: dict, input_file: str = None) -> None:
    """
    Шифрует исходный текст с помощью SM4, а ключ SM4 – с помощью RSA.

    Args:
        config (dict): словарь конфигурации с путями к файлам.
        input_file (str, optional): путь к входному файлу. Если None, берётся
                                    значение config['initial_file'].
    """
    src = input_file or config.get("initial_file")
    if not src or not os.path.exists(src):
        print(f"[!] Исходный файл '{src}' не найден.", file=sys.stderr)
        sys.exit(1)

    pub_path = config.get("public_key")
    if not os.path.exists(pub_path):
        print("[!] Публичный RSA-ключ не найден. Сначала выполните 'generate-rsa'.", file=sys.stderr)
        sys.exit(1)

    try:
        public_key = utilities.deserialize_public_key(pub_path)
        if public_key is None:
            raise ValueError("Не удалось загрузить публичный ключ")

        plaintext = utilities.read_txt_file(src)
        if not plaintext:
            raise ValueError("Исходный файл пуст")

        sm4_key = SM4.generate_sm4_key()
        iv, ciphertext = SM4.sm4_encrypt(sm4_key, plaintext)
        encrypted_data = iv + ciphertext

        enc_file = config["encrypted_file"]
        ensure_directory_exists(enc_file)
        utilities.write_txt_file(encrypted_data, enc_file)

        encrypted_sm4_key = RSA.encryption(sm4_key, public_key)
        sym_file = config["symmetric_key"]
        ensure_directory_exists(sym_file)
        utilities.write_txt_file(encrypted_sm4_key, sym_file)

        print(f"[+] Шифрование выполнено успешно.\n    Зашифрованный текст: {enc_file}\n"
              f"    Зашифрованный SM4-ключ: {sym_file}")
    except Exception as e:
        print(f"[!] Ошибка шифрования: {e}", file=sys.stderr)
        sys.exit(1)


def decrypt_text(config: dict) -> None:
    """
    Расшифровывает файл, используя приватный RSA-ключ и SM4.

    Args:
        config (dict): словарь конфигурации с путями к зашифрованным файлам и ключам.
    """
    enc_file = config.get("encrypted_file")
    sym_file = config.get("symmetric_key")
    if not enc_file or not sym_file:
        print("[!] В конфигурации отсутствуют пути к зашифрованным файлам.", file=sys.stderr)
        sys.exit(1)

    if not (os.path.exists(enc_file) and os.path.exists(sym_file)):
        print("[!] Зашифрованные файлы не найдены. Сначала выполните 'encrypt'.", file=sys.stderr)
        sys.exit(1)

    priv_path = config.get("secret_key")
    if not os.path.exists(priv_path):
        print("[!] Приватный RSA-ключ не найден.", file=sys.stderr)
        sys.exit(1)

    try:
        private_key = utilities.deserialize_private_key(priv_path)
        if private_key is None:
            raise ValueError("Не удалось загрузить приватный ключ")

        enc_sm4_key = utilities.read_txt_file(sym_file)
        sm4_key = RSA.decryption(enc_sm4_key, private_key)

        encrypted_data = utilities.read_txt_file(enc_file)
        if len(encrypted_data) < SM4.BLOCK_SIZE:
            raise ValueError("Зашифрованный файл слишком мал (отсутствует IV)")

        iv = encrypted_data[:SM4.BLOCK_SIZE]
        ciphertext = encrypted_data[SM4.BLOCK_SIZE:]
        decrypted_text = SM4.sm4_decrypt(sm4_key, ciphertext, iv)

        dec_file = config["decrypted_file"]
        ensure_directory_exists(dec_file)
        utilities.write_txt_file(decrypted_text, dec_file)
        print(f"[+] Расшифровка выполнена успешно.\n    Результат: {dec_file}")
    except Exception as e:
        print(f"[!] Ошибка расшифровки: {e}", file=sys.stderr)
        sys.exit(1)


def show_encrypted(config: dict) -> None:
    """
    Выводит содержимое зашифрованного файла в виде hex-дампа.

    Args:
        config (dict): словарь конфигурации с ключом 'encrypted_file'.
    """
    path = config.get("encrypted_file")
    if not path or not os.path.exists(path):
        print("[!] Зашифрованный файл не найден.", file=sys.stderr)
        sys.exit(1)
    data = utilities.read_txt_file(path)
    print(f"Размер: {len(data)} байт")
    print(show_hex_dump(data))


def show_decrypted(config: dict) -> None:
    """
    Выводит содержимое расшифрованного текстового файла.

    Args:
        config (dict): словарь конфигурации с ключом 'decrypted_file'.
    """
    path = config.get("decrypted_file")
    if not path or not os.path.exists(path):
        print("[!] Расшифрованный файл не найден. Сначала выполните 'decrypt'.", file=sys.stderr)
        sys.exit(1)
    data = utilities.read_txt_file(path)
    print(show_text(data))


def show_keys(config: dict) -> None:
    """
    Выводит содержимое файлов ключей (RSA и зашифрованного SM4-ключа).

    Args:
        config (dict): словарь конфигурации с ключами 'public_key', 'secret_key', 'symmetric_key'.
    """
    items = [
        ("Публичный RSA-ключ", config.get("public_key")),
        ("Приватный RSA-ключ", config.get("secret_key")),
        ("Зашифрованный SM4-ключ", config.get("symmetric_key"))
    ]
    for name, path in items:
        if not path:
            continue
        print(f"\n{name}: {path}")
        if not os.path.exists(path):
            print("   (файл не существует)")
            continue
        if "SM4" in name:
            data = utilities.read_txt_file(path)
            print(f"   Длина: {len(data)} байт")
            print(f"   Hex: {show_hex_dump(data)}")
        else:
            with open(path, 'r', encoding='utf-8') as f:
                print(f.read().rstrip())