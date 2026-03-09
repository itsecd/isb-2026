import time
import random
import re


def save_data(data: str) -> None:
    with open("python_gen.txt", "w", encoding="utf-8") as file:
        file.write(data)


def random_gen() -> str:
    data = ""
    random.seed(time.time())
    for i in range(128):
        data += str(random.randint(0, 1))
    return data


def main() -> None:
    try:
        generated = random_gen()
        save_data(generated)
    except Exception as ex:
        print("Ошибка: ", ex)


if __name__ == "__main__":
    main()
