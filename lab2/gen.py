import random
import time


def generate():
    try:
        random.seed(time.time())

        bits = ""

        for _ in range(128):
            bits += str(random.randint(0, 1))

        with open("py_sequence.txt", "w", encoding="utf-8") as f:
            f.write(bits)

        print("Python: файл успешно создан")

    except Exception as e:
        print(f"Ошибка Python генерации: {e}")


if __name__ == "__main__":
    generate()
