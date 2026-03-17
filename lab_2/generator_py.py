import random


def generate_sequence(length: int) -> str:
    """
    Генерация псевдослучайной последовательности длины length
    """
    return "".join(str(random.randint(0, 1)) for _ in range(length))


def save_sequence(filename: str, data: str) -> None:
    """
    Сохранение последовательности в файл
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)


def main() -> None:
    size = 128
    sequence = generate_sequence(size)
    save_sequence("python_sequence.txt", sequence)
    print("Python sequence successfully generated")


if __name__ == "__main__":
    main()