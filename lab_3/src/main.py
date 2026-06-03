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
import json

from . import io_utils
from . import modes


def parse_arguments() -> argparse.Namespace:
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
    group.add_argument('--generate', action='store_true', help='Генерация ключей')
    group.add_argument('--encrypt', action='store_true', help='Шифрование файла')
    group.add_argument('--decrypt', action='store_true', help='Расшифровка файла')
    
    parser.add_argument('--config', type=str, required=True, help='Путь к config/path.json')
    
    return parser.parse_args()


def main() -> None:
    """Основная функция приложения."""
    args = parse_arguments()
    
    print("Загрузка конфигурации...")
    try:
        config = io_utils.load_json_config(args.config)
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        sys.exit(1)
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        sys.exit(1)
        
    mode = 'generate' if args.generate else 'encrypt' if args.encrypt else 'decrypt'
    
    try:
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
                print("Неизвестный режим работы.", file=sys.stderr)
                sys.exit(1)
                
        print("\nОперация завершена успешно!")
        
    except FileNotFoundError as e:
        print(f"\nОшибка: необходимый файл отсутствует - {e.filename}")
        sys.exit(1)
    except PermissionError as e:
        print(f"\nОшибка: нет прав доступа к файлу - {e.filename}")
        sys.exit(1)
    except ValueError as e:
        print(f"\nОшибка параметров: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nПроизошла непредвиденная ошибка: {type(e).__name__}: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()