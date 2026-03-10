import random
import time


def generate_string(length: int) -> str:
    """
    Функия для генерации псч
    """
    result = ""
    random.seed(time.time())
    for i in range(length):
        rand_int = random.randint(0,255)
        rand_int_8bit = "0"*(8-len(bin(rand_int)[2:]))+bin(rand_int)[2:]
        result += rand_int_8bit
    return result


def main() -> None:
    """
    Главная фунцкия, осуществляющая генерацию псч и её запись в файл
    """
    bitstring = generate_string(16)
    with open("python_string.txt", "w", encoding="utf-8") as file:
        file.write(bitstring)


if __name__ == "__main__":
    main()