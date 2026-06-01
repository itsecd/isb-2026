import argparse

from cast5_ops import (
    generate_cast5_key,
    encrypt_file_cast5,
    decrypt_file_cast5
)
from rsa_ops import (
    generate_rsa_keys,
    save_private_key,
    save_public_key,
    load_private_key,
    encrypt_symmetric_key,
    decrypt_symmetric_key
)
from exceptions import FileProcessingError, CryptoSystemError
from file_utils import load_json, read_bytes, write_bytes

DEFAULT_SETTINGS_PATH = "settings.json"


def load_settings(path: str = DEFAULT_SETTINGS_PATH) -> dict:
    """
    Загружает настройки из JSON-файла.

    :param path: Путь к settings.json.
    :return: Словарь настроек.
    :raises FileProcessingError: При ошибке загрузки.
    """
    try:
        return load_json(path)
    except Exception as error:
        raise FileProcessingError(f"Ошибка загрузки настроек: {error}") from error


def generate_keys(settings: dict) -> None:
    """
    Генерирует:
    - CAST5 ключ;
    - RSA ключи;
    - шифрует симметричный ключ.

    :param settings: Настройки системы.
    :raises CryptoSystemError: При ошибке генерации.
    """
    try:
        print("[+] Генерация ключа CAST5...")
        symmetric_key = generate_cast5_key(
            settings["cast5_key_size"],
            settings["cast5_min_key_size"],
            settings["cast5_max_key_size"],
            settings["cast5_key_step"]
        )

        print("[+] Генерация RSA ключей...")
        private_key, public_key = generate_rsa_keys(
            settings["rsa_public_exponent"],
            settings["rsa_key_size"]
        )

        print("[+] Сохранение RSA ключей...")
        save_private_key(private_key, settings["private_key"])
        save_public_key(public_key, settings["public_key"])

        print("[+] Шифрование симметричного ключа RSA...")
        encrypted_sym_key = encrypt_symmetric_key(symmetric_key, public_key)
        write_bytes(settings["encrypted_symmetric_key"], encrypted_sym_key)

        print("[+] Ключи успешно созданы")
    except Exception as error:
        raise CryptoSystemError(f"Ошибка генерации ключей: {error}") from error


def _get_symmetric_key_from_encrypted(settings: dict) -> bytes:
    """
    Получает симметричный ключ.

    :param settings: Настройки системы.
    :return: Расшифрованный ключ CAST5.
    """
    private_key = load_private_key(settings["private_key"])
    encrypted_key = read_bytes(settings["encrypted_symmetric_key"])
    return decrypt_symmetric_key(encrypted_key, private_key)


def encrypt_data(settings: dict) -> None:
    """
    Шифрует файл.

    :param settings: Настройки системы.
    :raises CryptoSystemError: При ошибке шифрования.
    """
    try:
        print("[+] Загрузка RSA private key...")
        symmetric_key = _get_symmetric_key_from_encrypted(settings)

        print("[+] Шифрование файла CAST5...")
        encrypt_file_cast5(
            settings["initial_file"],
            settings["encrypted_file"],
            symmetric_key,
            settings["cast5_block_size"],
            settings["cast5_iv_size"]
        )

        print("[+] Файл успешно зашифрован")
    except Exception as error:
        raise CryptoSystemError(f"Ошибка шифрования: {error}") from error


def decrypt_data(settings: dict) -> None:
    """
    Расшифровывает файл.

    :param settings: Настройки системы.
    :raises CryptoSystemError: При ошибке дешифрования.
    """
    try:
        print("[+] Загрузка RSA private key...")
        symmetric_key = _get_symmetric_key_from_encrypted(settings)

        print("[+] Дешифрование файла CAST5...")
        decrypt_file_cast5(
            settings["encrypted_file"],
            settings["decrypted_file"],
            symmetric_key,
            settings["cast5_block_size"],
            settings["cast5_iv_size"]
        )

        print("[+] Файл успешно расшифрован")
    except Exception as error:
        raise CryptoSystemError(f"Ошибка дешифрования: {error}") from error


def main() -> None:
    """Точка входа программы."""
    try:
        parser = argparse.ArgumentParser()
        group = parser.add_mutually_exclusive_group(required=True)

        group.add_argument(
            "-gen", "--generation",
            action="store_true",
            help="Генерация ключей"
        )
        group.add_argument(
            "-enc", "--encryption",
            action="store_true",
            help="Шифрование"
        )
        group.add_argument(
            "-dec", "--decryption",
            action="store_true",
            help="Дешифрование"
        )
        parser.add_argument(
            "-s", "--settings",
            default=DEFAULT_SETTINGS_PATH,
            help="Путь к settings.json"
        )

        args = parser.parse_args()
        settings = load_settings(args.settings)

        match (args.generation, args.encryption, args.decryption):
            case (True, False, False):
                generate_keys(settings)
            case (False, True, False):
                encrypt_data(settings)
            case (False, False, True):
                decrypt_data(settings)
            case _:
                raise ValueError("Некорректный режим работы")

    except Exception as error:
        print(f"[!] Ошибка: {error}")


if __name__ == "__main__":
    main()
