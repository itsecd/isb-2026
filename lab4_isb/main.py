import l4
import argparse
import json




def parse_arguments() -> argparse.Namespace:
    """
    Парсинг аргументов командной строки.
    :return: объект с аргументами командной строки
    """

    parser = argparse.ArgumentParser(description="Run collision experiments and save results to CSV.")
    parser.add_argument(
        "--source",
        choices=["file", "args"],
        default="args",
        help="Source of parameters: 'file' for JSON file, 'args' for command-line arguments."
    )
    parser.add_argument(
        "--config_file",
        type=str,
        default="config.json",
        help="Path to JSON configuration file."
    )
    parser.add_argument(
        "--length",
        type=int,
        default=10,
        help="Length of the random strings."
    )
    parser.add_argument(
        "--bits",
        type=int,
        choices=[8, 12, 16],
        help="Number of bits for the shortened hash."
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run experiments for 8, 12 and 16 bits."
    )
    parser.add_argument(
        "--num_experiments",
        type=int,
        default=1000,
        help="Number of experiments to run."
    )
    parser.add_argument(
        "--file_name",
        type=str,
        default="collisions.csv",
        help="CSV file to save collision data."
    )
    parser.add_argument(
        "--stats_file",
        type=str,
        default="stats.csv",
        help="CSV file to save statistics."
    )
    return parser.parse_args()


def load_config(config_file: str) -> dict:
    """
    Загрузка параметров из JSON-файла.
    :param config_file: путь к JSON-файлу
    :return: словарь с параметрами
    """

    try:
        with open(config_file, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Config file not found: {config_file}") from e
    except PermissionError as e:
        raise PermissionError(f"No permission to read config file: {config_file}") from e
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in config file: {config_file}") from e
    except OSError as e:
        raise OSError(f"Error occurred while reading config file {config_file}: {e}") from e


def bits_list_check(bits_list: list[int]) -> None:
    """
    Проверка списка длин укороченного хеша.
    :param bits_list: список длин хеша в битах
    :return: не возвращается
    """

    if not bits_list:
        raise ValueError("At least one hash length must be specified")
    for bits in bits_list:
        if bits not in [8, 12, 16]:
            raise ValueError("Bits must be one of the following: 8, 12, 16")


def get_bits_from_args(args: argparse.Namespace) -> list[int]:
    """
    Получение списка длин хеша из аргументов командной строки.
    :param args: объект с аргументами командной строки
    :return: список длин хеша в битах
    """

    if args.all:
        return [8, 12, 16]
    if args.bits is not None:
        return [args.bits]
    raise ValueError("You must specify --bits or use --all")


def get_bits_from_config(config: dict) -> list[int]:
    """
    Получение списка длин хеша из JSON-конфига.
    :param config: словарь с параметрами из JSON-файла
    :return: список длин хеша в битах
    """

    bits_value = config.get("bits")
    if bits_value == "all":
        return [8, 12, 16]
    if isinstance(bits_value, int):
        return [bits_value]
    if isinstance(bits_value, list):
        return bits_value
    raise ValueError(
        'Config field "bits" must be 8, 12, 16, "all", or a list of these values'
    )


def get_parameters(args: argparse.Namespace) -> tuple[int, list[int], int, str, str]:
    """
    Получение параметров из аргументов командной строки или JSON-файла.
    :param args: объект с аргументами командной строки
    :return: length, bits_list, num_experiments, file_name, stats_file
    """

    if args.source == "file":
        config = load_config(args.config_file)
        length = int(config.get("length", 10))
        bits_list = get_bits_from_config(config)
        num_experiments = int(config.get("num_experiments", 1000))
        file_name = config.get("file_name", "collisions.csv")
        stats_file = config.get("stats_file", "stats.csv")
    else:
        length = args.length
        bits_list = get_bits_from_args(args)
        num_experiments = args.num_experiments
        file_name = args.file_name
        stats_file = args.stats_file
    if length <= 0:
        raise ValueError("Length must be a positive number")
    if num_experiments <= 0:
        raise ValueError("Number of experiments must be a positive number")
    bits_list_check(bits_list)
    return length, bits_list, num_experiments, file_name, stats_file


def run_collision_experiments(length: int, bits_list: list[int], num_experiments: int, file_name: str, stats_file: str) -> list[dict]:
    """
    Запуск экспериментов по поиску коллизий и сохранение статистики.
    :param length: длина генерируемых случайных строк
    :param bits_list: список длин укороченного хеша в битах
    :param num_experiments: количество экспериментов для каждой длины хеша
    :param file_name: путь к CSV-файлу для сохранения найденных коллизий
    :param stats_file: путь к CSV-файлу для сохранения статистики
    :return: список словарей со статистикой
    """

    l4.create_dict_csv(file_name, "experiment", "bits", "hash", "string1", "string2", "attempts")
    for bits in bits_list:
        l4.experiment(
            length=length,
            bits=bits,
            num_experiments=num_experiments,
            file_name=file_name
        )
    stats = l4.stats_from_csv(file_name)
    l4.stats_to_csv(stats_file, stats)

    return stats


def main() -> None:
    """
    Главная функция программы.
    :return: не возвращается
    """

    try:
        args = parse_arguments()
        length, bits_list, num_experiments, file_name, stats_file = get_parameters(args)
        stats = run_collision_experiments(
            length=length,
            bits_list=bits_list,
            num_experiments=num_experiments,
            file_name=file_name,
            stats_file=stats_file
        )
        print(f"\nCollision Statistics: {stats}")
        print(f"Collision results saved to {file_name}")
        print(f"Statistics saved to {stats_file}")
    except (ValueError, TypeError, KeyError, FileNotFoundError, PermissionError, IsADirectoryError, OSError) as e: 
        print(f"Error: {e}")


if __name__ == "__main__":
    main()