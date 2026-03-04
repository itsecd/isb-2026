from constants import BITS_C, BITS_CPP, BITS_JAVA
from math import erfc, sqrt
from scipy.special import gammaincc


def frequency_bitwise_test(bits: str) -> float:
    """Частотный побитовый тест"""
    char_map = {"1": 1, "0": -1}
    sum_n = 0
    for c in bits:
        sum_n += char_map[c]
    sum_n /= sqrt(len(bits))
    return erfc(sum_n / sqrt(2))


def identical_consecutive_bits_test(bits: str) -> float:
    """Тест на одинаковые подряд идущие биты"""
    n = len(bits)
    z = bits.count("1") / n

    if not abs(z - 0.5) < (2 / sqrt(n)):
        return 0

    v = 0
    for i in range(n - 1):
        v += (bits[i] != bits[i + 1])

    x = abs(v - 2 * n * z * (1 - z)) / (2 * sqrt(2 * n) * z * (1 - z))
    return erfc(x)


def longest_sequence_test(bits: str, m: int = 8) -> float:
    """Тест на максимальную последовательность единиц в блоке"""
    v1, v2, v3, v4 = 0, 0, 0, 0
    for i in range(len(bits) // m):
        block = bits[m * i:m * (i + 1)]

        max_l = 0
        temp = "1"
        # Далеко не лучший способ, но сойдёт
        for _ in range(m):
            if temp in block:
                max_l += 1
            else:
                break
            temp += "1"

        if max_l >= 4:
            v4 += 1
        elif max_l == 3:
            v3 += 1
        elif max_l == 2:
            v2 += 1
        else:
            v1 += 1
    pi1, pi2, pi3, pi4 = 0.2148, 0.3672, 0.2305, 0.1875
    x_2 = 0
    x_2 += ((v1 - 16 * pi1) ** 2) / (16 * pi1)
    x_2 += ((v2 - 16 * pi2) ** 2) / (16 * pi2)
    x_2 += ((v3 - 16 * pi3) ** 2) / (16 * pi3)
    x_2 += ((v4 - 16 * pi4) ** 2) / (16 * pi4)

    return float(gammaincc(3 / 2, x_2 / 2))


def analyse(bits: str) -> None:
    """Анализ битовой строки с помощью тестов NIST"""
    print(f"{frequency_bitwise_test(bits) = }")  # классная фишка Python :)
    print(f"{identical_consecutive_bits_test(bits) = }")
    print(f"{longest_sequence_test(bits) = }")


def main():
    print("Последовательность C:")
    with open(BITS_C, mode="r") as f:
        analyse(f.read())

    print("\nПоследовательность C++:")
    with open(BITS_CPP, mode="r") as f:
        analyse(f.read())

    print("\nПоследовательность Java:")
    with open(BITS_JAVA, mode="r") as f:
        analyse(f.read())


if __name__ == "__main__":
    main()
