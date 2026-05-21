"""CLI режим с argparse."""
import argparse
from hmac_core import compute_hmac, verify_hmac
from constants import DEFAULT_KEY


def run_cli():
    parser = argparse.ArgumentParser(description="HMAC проверка подлинности сообщений")
    parser.add_argument("--mode", choices=["compute", "verify"], default="compute",
                        help="Режим работы")
    parser.add_argument("--message", type=str, help="Сообщение")
    parser.add_argument("--key", type=str, default=DEFAULT_KEY, help="Секретный ключ")
    parser.add_argument("--hmac", type=str, help="HMAC для проверки (в режиме verify)")

    args = parser.parse_args()

    match args.mode:
        case "compute":
            if not args.message:
                print("Ошибка: укажите --message")
                return
            try:
                h = compute_hmac(args.message, args.key)
                print(f"Сообщение: {args.message}")
                print(f"HMAC: {h}")
            except Exception as e:
                print(f"Ошибка: {e}")

        case "verify":
            if not args.message or not args.hmac:
                print("Ошибка: укажите --message и --hmac")
                return
            try:
                ok = verify_hmac(args.message, args.key, args.hmac)
                print(f"Сообщение: {args.message}")
                if ok:
                    print("Результат: Подлинность подтверждена ")
                else:
                    print("Результат: Подлинность НЕ подтверждена (данные изменены или ключ неверен)")
            except Exception as e:
                print(f"Ошибка: {e}")


if __name__ == "__main__":
    run_cli()