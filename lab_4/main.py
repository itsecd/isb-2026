import argparse

from hmac_core import generate_hmac, verify_hmac

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    generate_parser = subparsers.add_parser("generate", help="Сформировать HMAC-SHA256")
    generate_parser.add_argument("--message", help="Сообщение")
    generate_parser.add_argument("--key", help="Секретный ключ")
    verify_parser = subparsers.add_parser("verify", help="Проверить HMAC-SHA256")
    verify_parser.add_argument("--message", help="Сообщение")
    verify_parser.add_argument("--key", help="Секретный ключ")
    verify_parser.add_argument("--hmac", help="Полученный HMAC")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        match args.command:
            case "generate":
                mac = generate_hmac(args.message, args.key)
                print("Сообщение: ", args.message)
                print("HMAC-SHA256: ", mac)
            case "verify":
                is_valid = verify_hmac(args.message, args.key, args.hmac)
                if is_valid:
                    print("Результат: КОРРЕКТНО")
                    print("Сообщение подлинное и не было изменено.")
                else:
                    print("Результат: НЕКОРРЕКТНО")
                    print("Cообщение, ключ или HMAC указаны неверно.")
            case _:
                print("Ошибка: неизвестная команда.")
    except Exception as error:
        print("Ошибка:", error)


if __name__ == "__main__":
    main()