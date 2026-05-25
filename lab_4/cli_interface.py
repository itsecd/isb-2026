import argparse

from crypto_engine import compute_hmac, verify_hmac
from settings import DEFAULT_KEY


def main():
    parser = argparse.ArgumentParser(
        description="HMAC SHA-256 для проверки подлинности сообщений"
    )

    parser.add_argument(
        "--mode", required=True, choices=["compute", "verify"], help="Режим работы"
    )

    parser.add_argument("--message", help="Сообщение")

    parser.add_argument("--key", default=DEFAULT_KEY, help="Секретный ключ")

    parser.add_argument("--hmac", help="HMAC для проверки")

    args = parser.parse_args()

    match args.mode:
        case "compute":
            if not args.message:
                print("Ошибка: укажите --message")
                return

            h = compute_hmac(args.message, args.key)
            print(f"HMAC: {h}")

        case "verify":
            if not args.message or not args.hmac:
                print("Ошибка: укажите --message и --hmac")
                return

            ok = verify_hmac(args.message, args.key, args.hmac)

            print("HMAC верный" if ok else "HMAC неверный")

        case _:
            print("Неизвестный режим")


if __name__ == "__main__":
    main()
