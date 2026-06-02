"""
Точка входа в приложение гибридной криптосистемы.

Парсит аргументы командной строки и запускает соответствующий режим работы:
- Генерация ключей
- Шифрование файлов
- Расшифровка файлов

Примеры использования:
    python -m src.main --generate --config config/path.json
    python -m src.main --encrypt --config config/path.json
    python -m src.main --decrypt --config config/path.json
"""

import argparse
import sys
from pathlib import Path

from . import io_utils
from . import modes


def parse_arguments():
    """
    Парсит аргументы командной строки.
    
    Returns:
        argparse.Namespace: Объект с распарсенными аргументами.
        
    Arguments:
        --generate: Запустить режим генерации ключей
        --encrypt: Запустить режим шифрования
        --decrypt: Запустить режим расшифровки
        --config: Путь к JSON файлу конфигурации
    """
    parser = argparse.ArgumentParser(
        description='Гибридная криптосистема SM4 + RSA',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  %(prog)s --generate --config config/path.json
  %(prog)s --encrypt --config config/path.json
  %(prog)s --decrypt --config config/path.json
        """
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--generate',
        action='store_true',
        help='Режим генерации ключей'
    )
    group.add_argument(
        '--encrypt',
        action='store_true',
        help='Режим шифрования файла'
    )
    group.add_argument(
        '--decrypt',
        action='store_true',
        help='Режим расшифровки файла'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        required=True,
        help='Путь к JSON файлу конфигурации'
    )
    
    return parser.parse_args()


def main():
    """
    Основная функция приложения.
    
    Загружает конфигурацию и запускает выбранный режим работы.
    Обрабатывает ошибки и выводит сообщения об успехе/неудаче.
    """
    args = parse_arguments()
    
    try:
        print("[*] Загрузка конфигурации...")
        config = io_utils.load_json_config(args.config)
        mode = 'generate' if args.generate else 'encrypt' if args.encrypt else 'decrypt'
        
        match mode:
            case 'generate':
                print("Режим: Генерация ключей\n")
                modes.generate_keys_mode(config)
                
            case 'encrypt':
                print("Режим: Шифрование\n")
                modes.encrypt_mode(config)
                
            case 'decrypt':
                print("Режим: Расшифровка\n")
                modes.decrypt_mode(config)
            
            case _:
                print("Неизвестный режим работы", file=sys.stderr)
                sys.exit(1)
        
        print("\nОперация завершена успешно!")
        
    except io_utils.FileReadError as e:
        print(f"\nОшибка чтения: {e}", file=sys.stderr)
        sys.exit(1)
    except io_utils.FileWriteError as e:
        print(f"\nОшибка записи: {e}", file=sys.stderr)
        sys.exit(1)
    except io_utils.ConfigLoadError as e:
        print(f"\nОшибка конфигурации: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"\nОшибка: Файл не найден - {e.filename}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nПроизошла ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()