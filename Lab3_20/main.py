"""CLI интерфейс для гибридной криптосистемы RSA + Camellia"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from file_utils import load_json_settings
from hybrid_crypto import generate_hybrid_keys, encrypt_hybrid, decrypt_hybrid


def main():
    """Главная функция CLI"""
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("--generation", action="store_true")
    group.add_argument("--encryption", action="store_true")
    group.add_argument("--decryption", action="store_true")

    parser.add_argument("--settings", required=True)
    parser.add_argument("--keysize", type=int, choices=[128, 192, 256],
                        help="Для Camellia: 128/192/256 бит")

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
                print(f"успех {message}")
            case False:
                print(f"не успех {message}")
                sys.exit(1)

    except KeyboardInterrupt:
        print("\n Операция прервана пользователем")
        sys.exit(130)
    except Exception as e:
        print(f" Непредвиденная ошибка: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()