import math

from constants import (
    BLOCK_SIZE,
    PI_VALUES,
    SEQUENCE_FILES,
    P_VALUE_LIMIT,
    RESULT_FILE
)
from lab_2.constants import RESULT_FILE


def read_sequence(filename):
    """
    Чтение бинарной последовательности из файла.
    """

    with open(filename, "r", encoding="utf-8") as file:
        sequence = file.read().strip()

    return sequence


def frequency_test(sequence):
    """
    Частотный побитовый тест - проверка равномерности распределения нулей и единиц.
    """

    n = len(sequence)

    s = 0

    for bit in sequence:
        if bit == "1":
            s += 1
        else:
            s -= 1

    s_obs = abs(s) / math.sqrt(n)

    p_value = math.erfc(s_obs / math.sqrt(2))

    return p_value


def runs_test(sequence):
    """
    Тест на одинаковые подряд идущие биты - проверка количества смен битов в последовательности.
    """

    n = len(sequence)

    ones = sequence.count("1")
    pi = ones / n

    if abs(pi - 0.5) >= (2 / math.sqrt(n)):
        return 0.0

    v = 1

    for i in range(1, n):
        if sequence[i] != sequence[i - 1]:
            v += 1

    numerator = abs(v - 2 * n * pi * (1 - pi))
    denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)

    p_value = math.erfc(numerator / denominator)

    return p_value


def longest_run_test(sequence):
    """
    Тест самой длинной последовательности единиц в блоке.
    """

    blocks = []

    for i in range(0, len(sequence), BLOCK_SIZE):
        blocks.append(sequence[i:i + BLOCK_SIZE])

    v1 = 0
    v2 = 0
    v3 = 0
    v4 = 0

    for block in blocks:

        max_run = 0
        current_run = 0

        for bit in block:

            if bit == "1":
                current_run += 1

                if current_run > max_run:
                    max_run = current_run
            else:
                current_run = 0

        if max_run <= 1:
            v1 += 1
        elif max_run == 2:
            v2 += 1
        elif max_run == 3:
            v3 += 1
        else:
            v4 += 1

    counts = [v1, v2, v3, v4]

    chi = 0

    for i in range(4):

        expected = 16 * PI_VALUES[i]

        chi += ((counts[i] - expected) ** 2) / expected

    p_value = math.exp(-chi / 2)

    return p_value


def check_result(p_value):
    """
    Проверка случайности последовательности.
    """

    if p_value >= P_VALUE_LIMIT:
        return "Последовательность случайная."

    return "Последовательность не случайная."


def main():
    """
    Основная функция.
    """
    with open(RESULT_FILE, "w", encoding="utf-8") as results:

        for filename in SEQUENCE_FILES:

            sequence = read_sequence(filename)

            text = f"\nФайл: {filename}\n"

            p1 = frequency_test(sequence)
            text +=f"Частотный тест: {p1}\n"
            text += check_result(p1) + "\n"

            p2 = runs_test(sequence)
            text += f"Тест серий: {p2}\n"
            text += check_result(p2) + "\n"

            p3 = longest_run_test(sequence)
            text += f"Тест длинной серии: {p3}\n"
            text += check_result(p3) + "\n"

            print(text)

            results.write(text)

if __name__ == "__main__":
    main()