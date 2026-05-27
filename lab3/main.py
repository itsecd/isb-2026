import argparse
import json

from crypto_utils import (
    generate_cast5_key,
    generate_rsa_keys,
    save_private_key,
    save_public_key,
    encrypt_symmetric_key,
    load_private_key,
    decrypt_symmetric_key,
    encrypt_file_cast5,
    decrypt_file_cast5
)

from constants import DEFAULT_SETTINGS_PATH
from exceptions import (
    FileProcessingError,
    CryptoSystemError
)


def load_settings(path: str = DEFAULT_SETTINGS_PATH) -> dict:
    """
    Загружает настройки из JSON-файла.

    Args:
        path (str):
            Путь к settings.json.

    Returns:
        dict:
            Словарь настроек.

    Raises:
        FileProcessingError:
            Если файл настроек
            невозможно открыть.
    """

    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    except Exception as error:
        raise FileProcessingError(
            f"Ошибка загрузки настроек: {error}"
        ) from error


def generate_keys(settings: dict) -> None:
    """
    Генерирует симметричный ключ CAST5
    и пару RSA ключей.

    Args:
        settings (dict):
            Настройки системы.

    Raises:
        CryptoSystemError:
            При ошибке генерации ключей.
    """

    try:
        print("[+] Генерация ключа CAST5...")

        key_size = settings["cast5_key_size"]

        symmetric_key = generate_cast5_key(
            key_size
        )

        print("[+] Генерация RSA ключей...")

        private_key, public_key = (
            generate_rsa_keys()
        )

        print("[+] Сохранение RSA ключей...")

        save_private_key(
            private_key,
            settings["private_key"]
        )

        save_public_key(
            public_key,
            settings["public_key"]
        )

        print(
            "[+] Шифрование "
            "симметричного ключа RSA..."
        )

        encrypted_sym_key = (
            encrypt_symmetric_key(
                symmetric_key,
                public_key
            )
        )

        with open(
            settings[
                "encrypted_symmetric_key"
            ],
            "wb"
        ) as file:
            file.write(
                encrypted_sym_key
            )

        print(
            "[+] Ключи успешно созданы"
        )

    except Exception as error:
        raise CryptoSystemError(
            f"Ошибка генерации ключей: "
            f"{error}"
        ) from error


def encrypt_data(settings: dict) -> None:
    """
    Выполняет шифрование файла.

    Args:
        settings (dict):
            Настройки системы.

    Raises:
        CryptoSystemError:
            При ошибке шифрования.
    """

    try:
        print(
            "[+] Загрузка RSA "
            "private key..."
        )

        private_key = (
            load_private_key(
                settings["private_key"]
            )
        )

        print(
            "[+] Загрузка "
            "зашифрованного "
            "симметричного ключа..."
        )

        with open(
            settings[
                "encrypted_symmetric_key"
            ],
            "rb"
        ) as file:
            encrypted_key = (
                file.read()
            )

        print(
            "[+] Расшифрование "
            "симметричного ключа..."
        )

        symmetric_key = (
            decrypt_symmetric_key(
                encrypted_key,
                private_key
            )
        )

        print(
            "[+] Шифрование "
            "файла CAST5..."
        )

        encrypt_file_cast5(
            settings["initial_file"],
            settings["encrypted_file"],
            symmetric_key
        )

        print(
            "[+] Файл успешно "
            "зашифрован"
        )

    except Exception as error:
        raise CryptoSystemError(
            f"Ошибка шифрования: "
            f"{error}"
        ) from error


def decrypt_data(settings: dict) -> None:
    """
    Выполняет дешифрование файла.

    Args:
        settings (dict):
            Настройки системы.

    Raises:
        CryptoSystemError:
            При ошибке дешифрования.
    """

    try:
        print(
            "[+] Загрузка RSA "
            "private key..."
        )

        private_key = (
            load_private_key(
                settings["private_key"]
            )
        )

        print(
            "[+] Загрузка "
            "зашифрованного "
            "симметричного ключа..."
        )

        with open(
            settings[
                "encrypted_symmetric_key"
            ],
            "rb"
        ) as file:
            encrypted_key = (
                file.read()
            )

        print(
            "[+] Расшифрование "
            "симметричного ключа..."
        )

        symmetric_key = (
            decrypt_symmetric_key(
                encrypted_key,
                private_key
            )
        )

        print(
            "[+] Дешифрование "
            "файла CAST5..."
        )

        decrypt_file_cast5(
            settings["encrypted_file"],
            settings["decrypted_file"],
            symmetric_key
        )

        print(
            "[+] Файл успешно "
            "расшифрован"
        )

    except Exception as error:
        raise CryptoSystemError(
            f"Ошибка дешифрования: "
            f"{error}"
        ) from error


def main() -> None:
    """
    Главная функция программы.

    Выполняет обработку
    аргументов командной строки
    и запуск нужного режима.
    """

    try:
        parser = argparse.ArgumentParser()

        group = (
            parser
            .add_mutually_exclusive_group(
                required=True
            )
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
            default=(
                DEFAULT_SETTINGS_PATH
            ),
            help=(
                "Путь "
                "к settings.json"
            )
        )

        args = (
            parser.parse_args()
        )

        settings = (
            load_settings(
                args.settings
            )
        )

        match (
            args.generation,
            args.encryption,
            args.decryption
        ):
            case (
                True,
                False,
                False
            ):
                generate_keys(
                    settings
                )

            case (
                False,
                True,
                False
            ):
                encrypt_data(
                    settings
                )

            case (
                False,
                False,
                True
            ):
                decrypt_data(
                    settings
                )

            case _:
                raise ValueError(
                    "Некорректный "
                    "режим работы"
                )

    except Exception as error:
        print(
            f"[!] Ошибка: "
            f"{error}"
        )


if __name__ == "__main__":
    main()
