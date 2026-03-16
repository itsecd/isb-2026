import random


def save_file(file_name: str, text: str) -> None:
    """
    Сохранение файла
    """
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(text)
    return


def random_bits_generator(bits_len: int) -> str:
    """
    Генератор псевдослучайных двоичных чисел
    """
    bits = ""
    for i in range(bits_len):
        bits += str(random.randint(0,1))
    return bits


def main() -> None:
    try:
        bits = random_bits_generator(128)
        print(bits)
        save_file("py_random_vec.txt", bits)
    except Exception as exc:
        print(f"Возникла ошибка: {exc}")


if __name__ == "__main__":
    main()