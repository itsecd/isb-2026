"""CLI режим с argparse и tqdm."""
import argparse
import time
from hmac_core import compute_hmac, verify_hmac
from constants import DEFAULT_KEY


def demo_tqdm():
    """Демонстрация tqdm для визуализации."""
    try:
        from tqdm import tqdm
        for i in tqdm(range(100), desc="Проверка", unit="шаг"):
            time.sleep(0.005)
    except ImportError:
        print("tqdm не установлен. Установите: pip install tqdm")


def run_cli():
    parser = argparse.ArgumentParser(description="HMAC проверка подлинности сообщений")
    parser.add_argument("--mode", choices=["compute", "verify", "demo-tqdm"], default="compute",
                        help="Режим работы")
    parser.add_argument("--message", type=str, help="Сообщение")
    parser.add_argument("--key", type=str, default=DEFAULT_KEY, help="Секретный ключ")
    parser.add_argument("--hmac", type=str, help="HMAC для проверки (в режиме verify)")

    args = parser.parse_args()

    if args.mode == "compute":
        if not args.message:
            print("Ошибка: укажите --message")
            return
        h = compute_hmac(args.message, args.key)
        print(f"HMAC: {h}")

    elif args.mode == "verify":
        if not args.message or not args.hmac:
            print("Ошибка: укажите --message и --hmac")
            return
        ok = verify_hmac(args.message, args.key, args.hmac)
        print("Подлинность подтверждена" if ok else "Подлинность НЕ подтверждена")

    elif args.mode == "demo-tqdm":
        demo_tqdm()


if __name__ == "__main__":
    run_cli()