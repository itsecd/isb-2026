import random


FILE_PATH = "../sequences/py_seq.txt"


def main() -> None:
    """Генерация и запись в файл 128-битной последовательности"""
    length = 128
    sequence = ""

    for i in range(length):
        sequence += str(random.randint(0, 1))
    
    with open(FILE_PATH, "w", encoding="utf-8") as file:
        file.write(sequence)


if __name__ == "__main__":
    main()