from random import randint


def RandomBitsGenerator():
    """Генератор случаййных чисел"""
    with open("result_py.txt", "w") as f:
        for i in range(0, 128):
            f.write(f"{randint(0, 1)}")


if __name__ == "__main__":
    RandomBitsGenerator()
