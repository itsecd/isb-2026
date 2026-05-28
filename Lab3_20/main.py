# main.py
import argparse
import sys
from hybrid_crypto import load_settings, generation_mode, encryption_mode, decryption_mode


def main():
    """
    Главная функция, обрабатывающая аргументы командной строки и запускающая
    соответствующий режим работы (генерация/шифрование/расшифрование).
    """
    parser = argparse.ArgumentParser(description="Гибридная криптосистема RSA + Camellia")
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("--generation", action="store_true", help="Режим генерации ключей")
    group.add_argument("--encryption", action="store_true", help="Режим шифрования файла")
    group.add_argument("--decryption", action="store_true", help="Режим расшифрования файла")

    parser.add_argument("--settings", required=True, help="Путь к файлу настроек settings.json")
    parser.add_argument("--keysize", type=int, choices=[128, 192, 256],
                        help="Размер ключа Camellia в битах (требуется для --generation)")

    args = parser.parse_args()
    settings = load_settings(args.settings)

    match args:
        case _ if args.generation:
            if not args.keysize:
                print("Ошибка: при --generation нужен --keysize")
                sys.exit(1)
            generation_mode(settings, args.keysize)
        
        case _ if args.encryption:
            encryption_mode(settings)
        
        case _ if args.decryption:
            decryption_mode(settings)


if __name__ == "__main__":
    main()