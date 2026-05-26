import argparse
import sys
from hasher import (
    calculate_file_hash,
    save_hash_to_file,
    verify_file_integrity,
    simulate_collision_search,
)


def run_cli() -> None:
    """
    Выполняет парсинг аргументов командной строки и запускает соответствующую логику.

    Поддерживает три подкоманды:
        - hash: Вычисление и сохранение SHA-256 хеша файла.
        - verify: Проверка целостности файла по сохраненному хешу.
        - collision: Запуск симуляции поиска частичной коллизии.

    Raises:
        OSError: Ошибка ввода-вывода при работе с файловой системой через CLI.
        ValueError: Ошибка некорректных входных параметров.
        SystemExit: Завершение программы с кодом 1 в случае критической ошибки.
    """
    parser = argparse.ArgumentParser(
        description="Finding a hash, checking the integrity of a file, and simulating a collision search")

    subparsers = parser.add_subparsers(
        dest="command", help="Available Commands")

    hash_parser = subparsers.add_parser(
        "hash", help="Calculate and save the hash of a file")
    hash_parser.add_argument(
        "-f", "--file", required=True, help="The path to the target file")
    hash_parser.add_argument("-o", "--out", required=True,
                             help="Path to save the result")

    verify_parser = subparsers.add_parser(
        "verify", help="Verify file integrity")
    verify_parser.add_argument(
        "-f", "--file", required=True, help="Access to the file being checked")
    verify_parser.add_argument(
        "-hash", "--hashfile", required=True, help="Path to the file with the reference hash")

    args = parser.parse_args()

    try:
        if args.command == "hash":
            h = calculate_file_hash(args.file)
            save_hash_to_file(h, args.out)
            print(f"Хеш успешно записан в: {args.out}\nSHA-256: {h}")

        else:
            flag, cur, exp = verify_file_integrity(args.file, args.hashfile)
            if flag:
                print("Целостность подтверждена")
            else:
                print("Нарушение целостности")
                print(f"Ожидаемый: {exp}")
                print(f"Текущий: {cur}")

    except OSError as e:
        print(
            f"Критическая ошибка ввода-вывода в CLI: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Ошибка валидации параметров: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}", file=sys.stderr)
        sys.exit(1)
