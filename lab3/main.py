import argparse
import sys
import workflow
import crypto_storage as storage

def collect_arguments() -> argparse.Namespace:
    """
    Настраивает и разбирает аргументы командной строки.
    
    Returns:
        argparse.Namespace: Аргументы CLI
    Raises:
        Exception: При ошибке инициализации парсера.
    """
    try:
        parser = argparse.ArgumentParser(description="Гибридная криптосистема RSA+Blowfish")
        mode_group = parser.add_mutually_exclusive_group(required=True)
        mode_group.add_argument("--gen-keys", action="store_true", help="Режим генерации ключей")
        mode_group.add_argument("--encrypt", action="store_true", help="Режим шифрования")
        mode_group.add_argument("--decrypt", action="store_true", help="Режим дешифрования")
        parser.add_argument("--config", default="path.json", help="Путь к JSON-конфигурации")
        parser.add_argument("--key-size", type=int, choices=range(32, 449, 8), default=128, help="Длина ключа Blowfish")
        parser.add_argument("--input-file", help="Путь к входному файлу")
        parser.add_argument("--output-file", help="Путь к выходному файлу")
        parser.add_argument("--sym-key-path", help="Путь к зашифрованному симметричному ключу")
        parser.add_argument("--priv-key-path", help="Путь к приватному RSA-ключу")
        parser.add_argument("--pub-key-path", help="Путь к публичному RSA-ключу")
        return parser.parse_args()
    except Exception as exc:
        print(f"Ошибка инициализации аргументов: {exc}", file=sys.stderr)
        sys.exit(1)

def main() -> None:
    """
    Точка входа приложения. Определяет режим работы и вызывает соответствующий модуль workflow.
    
    Raises:
        Exception: При критической ошибке выполнения.
    """
    try:
        args = collect_arguments()
        config = storage.open_json(args.config)
        sym_key = args.sym_key_path or config["sym_key"]
        priv_key = args.priv_key_path or config["private_key"]
        pub_key = args.pub_key_path or config["public_key"]
        src_file = args.input_file or config["initial_file"]
        dst_file = args.output_file or config["encrypted_file"]
        key_size = args.key_size
        match (args.gen_keys, args.encrypt, args.decrypt):
            case (True, _, _):
                workflow.run_key_generation(sym_key, priv_key, pub_key, key_size)
            case (_, True, _):
                workflow.run_encryption(src_file, dst_file, sym_key, priv_key)
            case (_, _, True):
                dst_file = args.output_file or config["decrypted_file"]
                workflow.run_decryption(src_file, dst_file, sym_key, priv_key)
    except KeyError as exc:
        print(f"Отсутствует обязательный ключ в конфигурации: {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as error:
        print(f"Критическая ошибка выполнения: {error}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
