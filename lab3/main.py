#!/usr/bin/env python3
"""
Лабораторная работа №3 «Построение гибридной криптосистемы».

Симметричный алгоритм: SEED (128 бит).
Асимметричный алгоритм: RSA (2048 бит).
Режим симметричного шифрования: CBC с дополнением ANSI X.923.
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
    шифрования, предоставляя три режима работы:
    - генерация ключей;
    - шифрование файла;
    - дешифрование файла.

    Атрибуты:
        _config (ConfigManager): Менеджер конфигурации.
    """

    def __init__(self, config_path: str = "settings.json") -> None:
        """
        Инициализирует криптосистему с указанной конфигурацией.

        Аргументы:
            config_path: Путь к JSON-файлу с настройками.

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

        Читает приватный RSA-ключ и зашифрованный симметричный ключ,
        затем расшифровывает симметричный ключ с помощью RSA.

        Возвращает:
            bytes: Расшифрованный ключ SEED (16 байт).

        Исключения:
            CryptoSystemError: При ошибках загрузки или расшифрования.
        """
        print("Загрузка ключей")
        try:
            private_pem = FileHandler.read_bytes(self._config.get('private_key'))
            encrypted_key = FileHandler.read_bytes(self._config.get('symmetric_key'))
            rsa_keys = RSAKeyManager.load_from_private_pem(private_pem)
            sym_key = rsa_keys.decrypt_key(encrypted_key)
            return sym_key
        except CryptoSystemError:
            raise
        except Exception as exc:
            raise CryptoSystemError(f"Ошибка загрузки симметричного ключа: {exc}")

    def generate_keys(self) -> None:
        """
        Режим генерации ключей гибридной системы.

        Создаёт:
        - ключ SEED (128 бит);
        - пару RSA-ключей (2048 бит);
        - зашифрованный RSA симметричный ключ.

        Все ключи сохраняются по путям из конфигурации.
        """
        print("Режим генерации ключей")

        try:
            sym_key = SEEDCipher.generate_key()
            print(f"Ключ SEED создан ({len(sym_key)} байт)")

            rsa_keys = RSAKeyManager()

            print("Сохранение RSA-ключей")
            FileHandler.write_bytes(
                self._config.get('public_key'),
                rsa_keys.serialize_public()
            )
            FileHandler.write_bytes(
                self._config.get('private_key'),
                rsa_keys.serialize_private()
            )

            enc_sym_key = rsa_keys.encrypt_key(sym_key)
            FileHandler.write_bytes(
                self._config.get('symmetric_key'),
                enc_sym_key
            )

            print("Все ключи успешно сгенерированы и сохранены")
            print(f"  Публичный ключ RSA:         {self._config.get('public_key')}")
            print(f"  Приватный ключ RSA:         {self._config.get('private_key')}")
            print(f"  Зашифрованный ключ SEED:    {self._config.get('symmetric_key')}")

        except CryptoSystemError:
            raise
        except Exception as exc:
            raise CryptoSystemError(f"Ошибка при генерации ключей: {exc}")

    def encrypt_file(self) -> None:
        """
        Режим шифрования текстового файла.

        Читает исходный файл, шифрует его алгоритмом SEED в режиме CBC,
        сохраняет IV и шифротекст в выходной файл.
        """
        print("Режим шифрования файла")

        try:
            sym_key = self._load_symmetric_key()

            cipher = SEEDCipher(sym_key)
            iv = cipher.set_iv()
            print(f"IV сгенерирован ({len(iv)} байт)")

            text = FileHandler.read_text(self._config.get('initial_file'))
            data = text.encode('utf-8')
            print(f"Размер исходных данных: {len(data)} байт")

            ciphertext = cipher.encrypt(data)
            print(f"Размер зашифрованных данных: {len(ciphertext)} байт")

            FileHandler.write_bytes(
                self._config.get('encrypted_file'),
                iv + ciphertext
            )

            print(f"Файл успешно зашифрован: {self._config.get('encrypted_file')}")

        except CryptoSystemError:
            raise
        except Exception as exc:
            raise CryptoSystemError(f"Ошибка при шифровании: {exc}")

    def decrypt_file(self) -> None:
        """
        Режим дешифрования зашифрованного файла.

        Читает зашифрованный файл, извлекает IV, расшифровывает данные
        алгоритмом SEED и сохраняет результат в текстовый файл.
        """
        print("Режим дешифрования файла")

        try:
            sym_key = self._load_symmetric_key()

            cipher = SEEDCipher(sym_key)

            encrypted_data = FileHandler.read_bytes(
                self._config.get('encrypted_file')
            )

            iv = encrypted_data[:SEEDCipher.IV_SIZE]
            ciphertext = encrypted_data[SEEDCipher.IV_SIZE:]
            print(
                f"IV извлечён ({len(iv)} байт), "
                f"шифротекст ({len(ciphertext)} байт)"
            )

            plaintext = cipher.decrypt(ciphertext, iv)

            text = plaintext.decode('utf-8')
            FileHandler.write_text(
                self._config.get('decrypted_file'),
                text
            )

            print(f"Файл успешно расшифрован:"
                  f" {self._config.get('decrypted_file')}")

        except CryptoSystemError:
            raise
        except Exception as exc:
            raise CryptoSystemError(f"Ошибка при дешифровании: {exc}")


def create_parser() -> argparse.ArgumentParser:
    """
    Создаёт парсер аргументов командной строки.

    Возвращает:
        argparse.ArgumentParser: Настроенный парсер с тремя
        взаимоисключающими режимами работы.
    """
    parser = argparse.ArgumentParser(
        description='Гибридная криптосистема (SEED + RSA)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python main.py --generate            Генерация ключей
  python main.py --encrypt             Шифрование файла
  python main.py --decrypt             Дешифрование файла
  python main.py --generate -c my.json Использование своего конфига
        """
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-gen', '--generate',
        action='store_true',
        help='Запустить режим генерации ключей'
    )
    group.add_argument(
        '-enc', '--encrypt',
        action='store_true',
        help='Запустить режим шифрования файла'
    )
    group.add_argument(
        '-dec', '--decrypt',
        action='store_true',
        help='Запустить режим дешифрования файла'
    )

    parser.add_argument(
        '-c', '--config',
        default='settings.json',
        help='Путь к файлу конфигурации (по умолчанию: settings.json)'
    )

    return parser


def main() -> None:
    """
    Главная точка входа в программу.

    Парсит аргументы командной строки и запускает
    соответствующий режим работы криптосистемы.
    """
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