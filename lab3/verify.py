import argparse
import hashlib
import sys


def compute_sha256(file_path: str) -> str:
    """
    Вычисляет SHA-256 хеш указанного файла.
    Читает данные блоками для оптимизации использования памяти.

    """
    hasher = hashlib.sha256()
    with open(file_path, "rb") as stream:
        while chunk := stream.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


def verify_integrity(original_path: str, decrypted_path: str) -> bool:
    """
    Сравнивает два файла по криптографическим хешам SHA-256.
    Выводит результаты вычислений и итог проверки в консоль.

    """
    print(f"[\nВычисление хеша: {original_path}")
    hash_orig = compute_sha256(original_path)
    print(f"Хеш оригинала:   {hash_orig}")

    print(f"Вычисление хеша: {decrypted_path}")
    hash_dec = compute_sha256(decrypted_path)
    print(f"Хеш результата:  {hash_dec}")

    if hash_orig == hash_dec:
        print("\nФайлы идентичны. Целостность НЕ нарущена ^^")
        return True
    print("\nХеш-суммы не совпадают. Файлы различаются.")
    return False


def main() -> None:

    parser = argparse.ArgumentParser(
        description="Проверка целостности файлов по SHA-256 хешам (Lab 3)"
    )
    parser.add_argument("original", help="Путь к исходному файлу")
    parser.add_argument("decrypted", help="Путь к расшифрованному файлу")
    args = parser.parse_args()

    try:
        verify_integrity(args.original, args.decrypted)
    except FileNotFoundError as exc:
        print(f"[ERROR] Файл не найден: {exc}", file=sys.stderr)
        sys.exit(1)
    except PermissionError as exc:
        print(f"[ERROR] Отказано в доступе: {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"[ERROR] Неожиданная ошибка: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()