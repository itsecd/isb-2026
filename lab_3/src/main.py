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
        print("Загрузка конфигурации...")
        config = io_utils.load_json_config(args.config)
        
        if args.generate:
            print("Режим: Генерация ключей\n")
            modes.generate_keys_mode(
                symmetric_key_path=config['symmetric_key'],
                encrypted_symmetric_key_path=config['encrypted_symmetric_key'],
                public_key_path=config['public_key'],
                private_key_path=config['private_key']
            )
            
        elif args.encrypt:
            print("Режим: Шифрование\n")
            modes.encrypt_mode(
                input_path=config['initial_file'],
                output_path=config['encrypted_file'],
                private_key_path=config['private_key'],
                encrypted_symmetric_key_path=config['encrypted_symmetric_key']
            )
            
        elif args.decrypt:
            print("Режим: Расшифровка\n")
            modes.decrypt_mode(
                input_path=config['encrypted_file'],
                output_path=config['decrypted_file'],
                private_key_path=config['private_key'],
                encrypted_symmetric_key_path=config['encrypted_symmetric_key']
            )
            
        print("\nОперация завершена успешно!")
        
    except FileNotFoundError as e:
        print(f"\nОшибка: Файл не найден - {e.filename}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nПроизошла ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()