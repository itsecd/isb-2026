import random


def write_file(path: str, text: str) -> None:
    """
    Write text to file.
    """
    try:
        if path:
            with open(path, "w", encoding="utf-8") as file:
                file.write(text)
    except FileNotFoundError:
        raise


def get_random_sequence(length: int = 128) -> str:
    """
    Generate a pseudo-random binary sequence.
    """
    return "".join(str(random.randint(0, 1)) for _ in range(length))


def main():
    sequence = get_random_sequence()
    print(sequence)

    write_file("../sequences/seq_python.txt", sequence)


if __name__ == "__main__":
    main()