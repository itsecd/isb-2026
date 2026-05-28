"""CLI интерфейс для гибридной криптосистемы RSA + Camellia

Использование:
    python main.py --generation --settings settings.json --keysize 256
    python main.py --encryption --settings settings.json
    python main.py --decryption --settings settings.json
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from file_utils import load_json_settings
from hybrid_crypto import generate_hybrid_keys, encrypt_hybrid, decrypt_hybrid


def main():
    """Главная функция CLI интерфейса.
    
    Поддерживает три режима:
        --generation: генерация ключей (требует --keysize)
        --encryption: шифрование файла
        --decryption: дешифрование файла
    
    Returns:
        Код возврата: 0 - успех, 1 - ошибка, 130 - прерывание
    """
    parser = argparse.ArgumentParser(
        description="Гибридная криптосистема RSA-2048 + Camellia"
    )
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("--generation", action="store_true",
                       help="Генерация ключей (требует --keysize)")
    group.add_argument("--encryption", action="store_true",
                       help="Шифрование файла")
    group.add_argument("--decryption", action="store_true",
                       help="Дешифрование файла")

    parser.add_argument("--settings", required=True,
                        help="Путь к JSON файлу с настройками")
    parser.add_argument("--keysize", type=int, choices=[128, 192, 256],
                        help="Размер ключа Camellia: 128/192/256 бит")

    args = parser.parse_args()
    settings = load_json_settings(args.settings)

    try:
        match args:
            case _ if args.generation:
                match args.keysize:
                    case None:
                        print("Ошибка: при --generation нужен --keysize")
                        sys.exit(1)
                    case ks:
                        success, message = generate_hybrid_keys(settings, ks)
            
            case _ if args.encryption:
                success, message = encrypt_hybrid(settings)
            
            case _ if args.decryption:
                success, message = decrypt_hybrid(settings)
            
            case _:
                print("Не выбрана операция")
                sys.exit(1)

        match success:
            case True:
                print(f" УСПЕХ: {message}")
            case False:
                print(f" ОШИБКА: {message}")
                sys.exit(1)

    except KeyboardInterrupt:
        print("\nОперация прервана пользователем")
        sys.exit(130)
    except Exception as e:
        print(f"Непредвиденная ошибка: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()