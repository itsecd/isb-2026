import argparse
import math

from tqdm import tqdm

from collisions import find_single_collision
from errors import FileUtilsError, HashError
from fileutils import save_json


def parse_arguments() -> argparse.Namespace:
    """
    Adds and parses command-line arguments
    """
    parser = argparse.ArgumentParser(description="Лабораторная №4 Хеш-функции (Поиск коллизий на укороченных хешах).")
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-find', '--find-collision', action='store_true', help='Поиск одной коллизии')
    group.add_argument('-stat', '--statistics', action='store_true', help='Серия экспериментов для сбора статистики')

    parser.add_argument('-b', '--bits', type=int, choices=[8, 12, 16], default=8,
                        help='Разрядность усеченного хеша (8, 12, 16)')
    parser.add_argument('-e', '--experiments', type=int, default=100,
                        help='Количество экспериментов для запуска статистики')
    parser.add_argument('-o', '--output', type=str, help='Путь для экспорта результатов в формате JSON')
    return parser.parse_args()


def main() -> None:
    try:
        args = parse_arguments()

        match args:
            case _ if args.find_collision:
                print(f"Поиск коллизии для хеша длиной {args.bits} бит.")
                str1, str2, hash_value, attempts = find_single_collision(args.bits)
                print("Коллизия найдена.")
                print(f"Строка 1: {str1}")
                print(f"Строка 2: {str2}")
                print(f"Значение: {hash_value} (hex: {hex(hash_value)})")
                print(f"Попыток: {attempts}")
            case _ if args.statistics:
                print(f"Запуск серии попыток из {args.experiments} экспериментов для хеша длиной {args.bits}")
                attempts_list = []
                for _ in tqdm(range(args.experiments), desc="Сбор статистики", unit="эксп."):
                    _, _, _, attempts = find_single_collision(args.bits)
                    attempts_list.append(attempts)
                min_attempts = min(attempts_list)
                max_attempts = max(attempts_list)
                avg_attempts = sum(attempts_list) / len(attempts_list)
                theory = 1.25 * math.sqrt(2 ** args.bits)

                print("Результаты экспериментов:")
                print(f"Минимум попыток: {min_attempts}")
                print(f"Максимум попыток: {max_attempts}")
                print(f"Среднее количество попыток: {avg_attempts}")
                print(f"Ожидаемое количество попыток: {theory:.2f}")

                if args.output:
                    result = {
                        "bits": args.bits,
                        "experiments_count": args.experiments,
                        "min_attempts": min_attempts,
                        "max_attempts": max_attempts,
                        "average_attempts_practical": avg_attempts,
                        "expected_attempts_theoretical": theory,
                        "raw_data": attempts_list
                    }
                    save_json(args.output, result)
                print(f"Результаты сохранены в {args.output}")
    except FileUtilsError as err:
        print(f"Error while working with files: {err}")
    except HashError as err:
        print(f"Error while working with collisions: {err}")
    except Exception as err:
        print(f"Something went wrong. {err}")


if __name__ == "__main__":
    main()
