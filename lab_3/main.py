import json
import argparse
from crypto_utils import (
    generate_idea_key,
    generate_rsa_keys,
    save_private_key,
    save_public_key,
    encrypt_key,
    decrypt_key,
    encrypt_data,
    decrypt_data,
    load_private_key,
)


def log(msg: str) -> None:
    """
    Выводит сообщение в консоль с пометкой LOG.

    :param msg: текст сообщения
    :return: None
    """
    print(f"[LOG] {msg}")


def load_config() -> dict:
    """
    Загружает настройки из файла settings.json.

    :return: словарь с конфигурацией
    :raises Exception: если файл не найден или повреждён
    """
    try:
        with open("settings.json") as f:
            return json.load(f)
    except Exception as e:
        raise Exception(f"Ошибка загрузки settings.json: {e}")


def get_symmetric_key() -> bytes:
    """
    Получает симметричный ключ от пользователя или генерирует его.

    :return: симметричный ключ (16 байт)
    :raises ValueError: если введён некорректный ключ или выбор
    """
    print("1 - Ввести ключ")
    print("2 - Сгенерировать")

    choice = input("Выбор: ").strip()

    if choice == "1":
        key = input("Введите ключ (16 символов): ").encode()

        if len(key) != 16:
            raise ValueError("Ключ должен быть 16 байт")

        return key

    elif choice == "2":
        return generate_idea_key()

    else:
        raise ValueError("Неверный выбор")


def generate(config: dict) -> None:
    """
    Выполняет генерацию ключей гибридной системы:
    - получает симметричный ключ
    - генерирует RSA ключи
    - шифрует симметричный ключ
    - сохраняет всё в файлы

    :param config: словарь настроек
    :return: None
    """
    try:
        log("Генерация ключей")

        sym_key = get_symmetric_key()
        private_key, public_key = generate_rsa_keys()

        save_private_key(private_key, config["private_key"])
        save_public_key(public_key, config["public_key"])

        enc_key = encrypt_key(public_key, sym_key)

        with open(config["symmetric_key"], "wb") as f:
            f.write(enc_key)

        log("Готово")

    except Exception as e:
        print(f"[ERROR] {e}")


def encrypt(config: dict) -> None:
    """
    Выполняет шифрование данных:
    - расшифровывает симметричный ключ
    - читает исходный файл
    - шифрует данные алгоритмом IDEA
    - сохраняет результат

    :param config: словарь настроек
    :return: None
    """
    try:
        log("Шифрование")

        private_key = load_private_key(config["private_key"])

        with open(config["symmetric_key"], "rb") as f:
            enc_key = f.read()

        sym_key = decrypt_key(private_key, enc_key)

        with open(config["initial_file"], "rb") as f:
            data = f.read()

        encrypted = encrypt_data(sym_key, data)

        with open(config["encrypted_file"], "wb") as f:
            f.write(encrypted)

        log("Готово")

    except FileNotFoundError as e:
        print(f"[ERROR] Файл не найден: {e}")
    except Exception as e:
        print(f"[ERROR] {e}")


def decrypt(config: dict) -> None:
    """
    Выполняет дешифрование данных:
    - расшифровывает симметричный ключ
    - читает зашифрованный файл
    - расшифровывает данные IDEA
    - сохраняет результат

    :param config: словарь настроек
    :return: None
    """
    try:
        log("Дешифрование")

        private_key = load_private_key(config["private_key"])

        with open(config["symmetric_key"], "rb") as f:
            enc_key = f.read()

        sym_key = decrypt_key(private_key, enc_key)

        with open(config["encrypted_file"], "rb") as f:
            data = f.read()

        decrypted = decrypt_data(sym_key, data)

        with open(config["decrypted_file"], "wb") as f:
            f.write(decrypted)

        log("Готово")

    except FileNotFoundError as e:
        print(f"[ERROR] Файл не найден: {e}")
    except Exception as e:
        print(f"[ERROR] {e}")


parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)

group.add_argument("--gen", action="store_true")
group.add_argument("--enc", action="store_true")
group.add_argument("--dec", action="store_true")

args = parser.parse_args()
config = load_config()

if args.gen:
    generate(config)
elif args.enc:
    encrypt(config)
elif args.dec:
    decrypt(config)
