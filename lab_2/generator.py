import random
import time
import argparse


def parse_arguments() -> argparse.Namespace:
    """
    Функция для парсинга аргументов командной строки.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("output_file", help="Путь к файлу для записи результата")
    return parser.parse_args()


def write_file(filename: str, num: str) -> None:
    """
    Функция для записи в файл
    """
    with open(filename, mode="w", encoding="utf-8") as file:
        file.write(num)


def generator(filename: str) -> None:
    """
    Генератов случайных чисел

    """
    random.seed(time.time())
    data = ""
    for i in range(0, 128):
        random_vol = random.randint(0, 1)
        data += str(random_vol)
    write_file(filename, data)


if __name__ == "__main__":
    args = parse_arguments()
    generator(args.output_file)
