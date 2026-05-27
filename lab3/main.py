import argparse
import sys

from crypto.file_utils import load_settings
from modes.generation import key_generation_mode
from modes.encryption import encryption_mode
from modes.decryption import decryption_mode


def main():
    """
    Главная функция приложения выполняет:
    - разбор аргументов командной строки
    - загрузку настроек
    - запуск выбранного режима работы

    Raises:
        SystemExit: При критической ошибке приложения.
    """

    parser = argparse.ArgumentParser(description="Гибридная криптосистема SM4 + RSA")
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-gen', '--generation', action='store_true', help='Режим генерации ключей')
    group.add_argument('-enc', '--encryption', action='store_true', help='Режим шифрования')
    group.add_argument('-dec', '--decryption', action='store_true', help='Режим дешифрования')
    parser.add_argument('-s', '--settings', required=True, help='Путь к settings.json')

    args = parser.parse_args()

    try:
        settings = load_settings(args.settings)

        mode_map = {'generation': args.generation, 'encryption': args.encryption, 'decryption': args.decryption}
        mode = next((key for key, value in mode_map.items() if value), None)

        match mode:
            case 'generation':
                key_generation_mode(settings)
            case 'encryption':
                encryption_mode(settings)
            case 'decryption':
                decryption_mode(settings)
            case _:
                print("[ERROR] Не выбран режим работы")
                sys.exit(1)

    except FileNotFoundError as err:
        print(f"[ERROR] Файл не найден: {err}")
        sys.exit(1)

    except ValueError as err:
        print(f"[ERROR] Ошибка данных: {err}")
        sys.exit(1)

    except OSError as err:
        print(f"[ERROR] Ошибка файловой системы: {err}")
        sys.exit(1)

    except Exception as err:
        print(f"[ERROR] Неизвестная ошибка: {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
