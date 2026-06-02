import argparse
import hashlib
from hash import calculating_hash, integrity_check, collision_demo
from tqdm import tqdm


def run_cli() -> None:
    """
    Запускает консольный интерфейс программы, обрабатывая аргументы командной строки.
    """
    parser = argparse.ArgumentParser(description="Консольный интерфейс для работы с SHA-256")
    parser.add_argument("--file", type=str, help="Путь к файлу для быстрого расчета хэша SHA-256.")
    parser.add_argument("--check", nargs=2, metavar=("FILE", "HASH_FILE"), help="Проверить целостность файла (укажите путь к файлу и к файлу хэша).")
    parser.add_argument("--collision", type=int, metavar="LEN", help="Запустить поиск усеченной коллизии по длине префикса.")

    args = parser.parse_args()

    try:
        if args.file:
            print(f"Расчет хэша для файла: {args.file}")
            hash_value = calculating_hash(args.file)
            print(f"Результат SHA-256: {hash_value}")

        elif args.check:
            src_path, hash_path = args.check
            print(f"Запуск проверки целостности для файла: {src_path}")
            if integrity_check(src_path, hash_path):
                print("Целостность подтверждена, файл не изменен.")
            else:
                print("Целостность нарушена, файл был изменен.")

        elif args.collision is not None:
            attempts_max = 300000
            
            with tqdm(total=attempts_max, desc="Поиск коллизии", unit=" Попытка") as pbar:
                result = collision_demo(
                    attempts=attempts_max,
                    prefix_len=args.collision,
                    progress_callback=lambda current: pbar.update(current - pbar.n)
                )
                pbar.update(attempts_max - pbar.n)
            
            if result["first"]:
                h1 = hashlib.sha256(result["first"].encode()).hexdigest()
                h2 = hashlib.sha256(result["second"].encode()).hexdigest()
        
                print(f"\n=== КОЛЛИЗИЯ НАЙДЕНА (Попыток: {result['attempts']}) ===\n"
                      f"Совпавший префикс: {h1[:args.collision]}\n"
                      f"Текст 1: {result['first']} -> Хеш: {h1}\n"
                      f"Текст 2: {result['second']} -> Хеш: {h2}")
            else:
                print(f"\nКоллизия не найдена за {result['attempts']} попыток.")
        
        else:
            parser.print_help()

    except Exception as e:
        print(f"\nОшибка при выполнении операции: {e}")


if __name__ == "__main__":
    run_cli()