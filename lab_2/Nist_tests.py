import math

from constants import (
    BLOCK_SIZE,
    PI_VALUES,
    SEQUENCE_FILES,
    P_VALUE_LIMIT,
    RESULT_FILE
)

from scipy.special import gammaincc

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

    v = 0

    for i in range(n - 1):
        if sequence[i] != sequence[i + 1]:
            v += 1

    numerator = abs(v - 2 * n * pi * (1 - pi))
    denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)

    p_value = math.erfc(numerator / denominator)

    return p_value


def longest_run_test(sequence):
    """
    Тест самой длинной последовательности единиц в блоке.
    """

    M = BLOCK_SIZE
    N = len(sequence)

    if N < M:
        return 0.0

    K = N // M

    blocks = []

    for i in range(K):
        block = sequence[i * M:(i + 1) * M]
        blocks.append(block)

    max_runs = []

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

        max_runs.append(max_run)

    v = [0, 0, 0, 0]

    for run in max_runs:

        if run <= 1:
            v[0] += 1
        elif run == 2:
            v[1] += 1
        elif run == 3:
            v[2] += 1
        else:
            v[3] += 1

    chi = 0

    for i in range(4):

        expected = K * PI_VALUES[i]
        chi += ((v[i] - expected) ** 2) / expected

    p_value = gammaincc(3/2 ,chi / 2)

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
            text += f"Частотный тест: {p1}\n"
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