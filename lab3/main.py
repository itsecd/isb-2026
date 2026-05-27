#!/usr/bin/env python3
"""
Лабораторная работа №3 «Построение гибридной криптосистемы».

Симметричный алгоритм: SEED (128 бит).
Асимметричный алгоритм: RSA (2048 бит).
Режим симметричного шифрования: CBC с дополнением ANSI X.923.

Все параметры загружаются из settings.json.
Никакие значения не захардкожены в коде.
"""

import argparse
import sys

from config import ConfigManager
from file_utils import FileHandler
from seed_cipher import SEEDCipher
from rsa_manager import RSAKeyManager
from exceptions import CryptoSystemError


class HybridCryptoSystem:
    """
    Основной класс гибридной криптосистемы.

    Оркестрирует работу симметричного (SEED) и асимметричного (RSA)
    шифрования, предоставляя три режима работы.

    Атрибуты:
        _config (ConfigManager): Менеджер конфигурации.
    """

    def __init__(self, config_path: str = None) -> None:
        """
        Инициализирует криптосистему.

        Аргументы:
            config_path: Путь к JSON-файлу с настройками.
                         Если None, используется значение по умолчанию.

        Исключения:
            CryptoSystemError: При ошибках загрузки конфигурации.
        """
        print("Гибридная криптосистема (SEED + RSA)")
        try:
            self._config = ConfigManager(config_path)
            self._config.ensure_directories()
            print("Конфигурация загружена")
        except CryptoSystemError:
            raise
        except Exception as exc:
            raise CryptoSystemError(f"Ошибка инициализации: {exc}")

    def _load_symmetric_key(self) -> bytes:
        """
        Загружает и расшифровывает симметричный ключ SEED.

        Возвращает:
            bytes: Расшифрованный ключ SEED.

        Исключения:
            CryptoSystemError: При ошибках загрузки или расшифрования.
        """
        print("Загрузка ключей")
        try:
            private_pem = FileHandler.read_bytes(self._config.private_key)
            encrypted_key = FileHandler.read_bytes(self._config.symmetric_key)
            rsa_keys = RSAKeyManager.load_from_private_pem(private_pem)
            sym_key = rsa_keys.decrypt_key(encrypted_key)
            return sym_key
        except CryptoSystemError:
            raise
        except Exception as exc:
            raise CryptoSystemError(
                f"Ошибка загрузки симметричного ключа: {exc}")

    def generate_keys(self) -> None:
        """
        Режим генерации ключей гибридной системы.
        """
        print("Режим генерации ключей")

        try:
            sym_key = SEEDCipher.generate_key(self._config.seed_key_size)
            print(f"Ключ SEED создан ({len(sym_key)} байт)")

            rsa_keys = RSAKeyManager(
                key_size=self._config.rsa_key_size,
                public_exponent=self._config.rsa_public_exponent
            )

            print("Сохранение RSA-ключей")
            FileHandler.write_bytes(
                self._config.public_key, rsa_keys.serialize_public())
            FileHandler.write_bytes(
                self._config.private_key, rsa_keys.serialize_private())

            enc_sym_key = rsa_keys.encrypt_key(sym_key)
            FileHandler.write_bytes(self._config.symmetric_key, enc_sym_key)

            print("Все ключи успешно сгенерированы и сохранены")
            print(f"  Публичный ключ RSA:         {self._config.public_key}")
            print(f"  Приватный ключ RSA:         {self._config.private_key}")
            print(f"  Зашифрованный ключ SEED:    {
            self._config.symmetric_key}")

        except CryptoSystemError:
            raise
        except Exception as exc:
            raise CryptoSystemError(f"Ошибка при генерации ключей: {exc}")

    def encrypt_file(self) -> None:
        """
        Режим шифрования текстового файла.
        """
        print("Режим шифрования файла")

        try:
            sym_key = self._load_symmetric_key()

            cipher = SEEDCipher(
                key=sym_key,
                block_size=self._config.seed_block_size,
                iv_size=self._config.seed_iv_size
            )
            iv = cipher.set_iv()
            print(f"IV сгенерирован ({len(iv)} байт)")

            text = FileHandler.read_text(self._config.initial_file)
            data = text.encode(self._config.encoding)
            print(f"Размер исходных данных: {len(data)} байт")

            ciphertext = cipher.encrypt(data)
            print(f"Размер зашифрованных данных: {len(ciphertext)} байт")

            FileHandler.write_bytes(
                self._config.encrypted_file, iv + ciphertext)
            print(f"Файл успешно зашифрован: {self._config.encrypted_file}")

        except CryptoSystemError:
            raise
        except Exception as exc:
            raise CryptoSystemError(f"Ошибка при шифровании: {exc}")

    def decrypt_file(self) -> None:
        """
        Режим дешифрования зашифрованного файла.
        """
        print("Режим дешифрования файла")

        try:
            sym_key = self._load_symmetric_key()

            cipher = SEEDCipher(
                key=sym_key,
                block_size=self._config.seed_block_size,
                iv_size=self._config.seed_iv_size
            )

            encrypted_data = FileHandler.read_bytes(
                self._config.encrypted_file)

            iv = encrypted_data[:self._config.seed_iv_size]
            ciphertext = encrypted_data[self._config.seed_iv_size:]
            print(
                f"IV извлечён ({len(iv)} байт), "
                f"шифротекст ({len(ciphertext)} байт)"
            )

            plaintext = cipher.decrypt(ciphertext, iv)

            text = plaintext.decode(self._config.encoding)
            FileHandler.write_text(self._config.decrypted_file, text)
            print(f"Файл успешно расшифрован: {self._config.decrypted_file}")

        except CryptoSystemError:
            raise
        except Exception as exc:
            raise CryptoSystemError(f"Ошибка при дешифровании: {exc}")


def create_parser() -> argparse.ArgumentParser:
    """Создаёт парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description='Гибридная криптосистема (SEED + RSA)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python main.py --generate
  python main.py --encrypt
  python main.py --decrypt
  python main.py --generate -c my_settings.json
        """
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generate', action='store_true',
                       help='Запустить режим генерации ключей')
    group.add_argument('-enc', '--encrypt', action='store_true',
                       help='Запустить режим шифрования файла')
    group.add_argument('-dec', '--decrypt', action='store_true',
                       help='Запустить режим дешифрования файла')

    parser.add_argument('-c', '--config', default=None,
                        help='Путь к файлу конфигурации')

    return parser


def main() -> None:
    """Главная точка входа."""
    parser = create_parser()
    args = parser.parse_args()

    try:
        system = HybridCryptoSystem(args.config)

        match (args.generate, args.encrypt, args.decrypt):
            case (True, False, False):
                system.generate_keys()
            case (False, True, False):
                system.encrypt_file()
            case (False, False, True):
                system.decrypt_file()
            case _:
                print("Неизвестный режим работы")
                sys.exit(1)

    except CryptoSystemError as exc:
        print(f"Ошибка: {exc}")
        sys.exit(1)
    except Exception as exc:
        print(f"Критическая ошибка: {exc}")
        sys.exit(1)

    print("Работа завершена")


if __name__ == "__main__":
    main()