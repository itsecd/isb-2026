import sys
import argparse
from attack import find_collision, run_experiments, get_expected_attempts
from hash_utils import get_hash, compute_full_hash

def run_cli_mode(args: argparse.Namespace) -> None:
    """Выполняет логику приложения в режиме командной строки.

    Args:
        args: Объект с распарсенными аргументами командной строки.
    """
    match (args.single, args.experiment):
        case (True, False):
            bits = args.bits
            max_attempts = args.max_attempts
            print(f"Максимальное количество попыток: {max_attempts}")
            try:
                str1, str2, attempts, _ = find_collision(bits, max_attempts)
                match (str1 is not None, str2 is not None):
                    case (True, True):
                        expected = get_expected_attempts(bits)
                        print("\nКоллизия найдена!")
                        print(f"Попыток: {attempts}")
                        print(f"Ожидаемое количество попыток (теория): ~{expected}")
                        print(f"Эффективность: {expected / attempts * 100:.1f}% от теории")
                        print(f"\nСтрока 1: \"{str1}\"")
                        print(f"Хеш ({bits} бит): {get_hash(str1, bits)}")
                        print(f"\nСтрока 2: \"{str2}\"")
                        print(f"Хеш ({bits} бит): {get_hash(str2, bits)}")
                        print("\nПолные SHA-256 хеши:")
                        print(f"Строка 1: {compute_full_hash(str1)}")
                        print(f"Строка 2: {compute_full_hash(str2)}")
                    case _:
                        print(f"\nКоллизия не найдена за {attempts} попыток.")
            except Exception as e:
                print(f"Ошибка при поиске коллизии: {e}")
                sys.exit(1)

        case (False, True):
            bits = args.bits
            count = args.count
            print(f"Количество экспериментов: {count}\n")
            try:
                results = run_experiments(bits, count, args.max_attempts)
                successful = [r for r in results if r.get("success")]
                match successful:
                    case []:
                        print("Коллизий не найдено ни в одном эксперименте.")
                    case _:
                        avg_attempts = sum(r["attempts"] for r in successful) / len(successful)
                        expected = get_expected_attempts(bits)
                        print("\nСтатистика:")
                        print(f"Экспериментов с коллизией: {len(successful)}/{len(results)}")
                        print(f"Среднее количество попыток: {avg_attempts:.1f}")
                        print(f"Ожидаемое количество попыток (теория): ~{expected}")
                        print(f"Отклонение: {(avg_attempts - expected) / expected * 100:+.1f}%")
            except Exception as e:
                print(f"Ошибка при запуске экспериментов: {e}")
                sys.exit(1)

        case _:
            print("Ошибка: не выбран режим работы (--single или --experiment)")
            sys.exit(1)

def main() -> None:
    """Точка входа в приложение. Парсит аргументы и запускает соответствующий режим."""
    parser = argparse.ArgumentParser(description="Атака «Парадокс дней рождения»")
    parser.add_argument('--gui', action='store_true', help='Запуск графического интерфейса')
    parser.add_argument('--single', action='store_true', help='Поиск одной коллизии')
    parser.add_argument('--experiment', action='store_true', help='Серия экспериментов')
    parser.add_argument('--bits', type=int, default=16, choices=[8, 12, 16],
                        help='Длина хеша в битах (8, 12, 16)')
    parser.add_argument('--max-attempts', type=int, default=100000,
                        help='Максимальное количество попыток')
    parser.add_argument('--count', type=int, default=5,
                        help='Количество экспериментов')

    try:
        args = parser.parse_args()
    except SystemExit:
        sys.exit(0)

    match (args.gui, args.single, args.experiment):
        case (True, False, False):
            from gui import run_gui
            run_gui()
        case (False, True, False):
            run_cli_mode(args)
        case (False, False, True):
            run_cli_mode(args)
        case (False, False, False):
            parser.print_help()
        case _:
            print("Ошибка: можно выбрать только один режим работы")
            sys.exit(1)

if __name__ == "__main__":
    main()