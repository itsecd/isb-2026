import math
from scipy.special import gammaincc


"""Модуль реализации статистических тестов NIST."""


def load_bit_sequence(filepath: str) -> str:
    """
    Считать бинарную последовательность из файла.

    Args:
        filepath: Путь к файлу.

    Returns:
        Битовая строка длиной 128.
    """

    with open(filepath, "r", encoding="utf-8") as file:
        sequence = file.read().strip()

    if len(sequence) != 128:
        raise ValueError("Последовательность должна содержать ровно 128 бит")

    return sequence


def frequency_test(filename: str) -> float:
    """
    Частотный побитовый тест.

    Args:
        filename: Файл с последовательностью.

    Returns:
        Значение p-value.
    """

    bit_sequence = load_bit_sequence(filename)
    n = len(bit_sequence)

    ones = bit_sequence.count("1")
    zeros = bit_sequence.count("0")

    deviation = abs(ones - zeros)

    s = deviation / math.sqrt(n)

    p_value = math.erfc(s / math.sqrt(2))

    return p_value


def runs_test(filename: str) -> float:
    """
    Тест на одинаковые подряд идущие биты.

    Args:
        filename: Файл с последовательностью.

    Returns:
        Значение p-value.
    """

    bit_sequence = load_bit_sequence(filename)
    n = len(bit_sequence)

    pi = bit_sequence.count("1") / n

    if abs(pi - 0.5) >= (2 / math.sqrt(n)):
        return 0.0

    transitions = 0

    for i in range(n - 1):
        if bit_sequence[i] != bit_sequence[i + 1]:
            transitions += 1

    numerator = abs(transitions - 2 * n * pi * (1 - pi))

    denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)

    p_value = math.erfc(numerator / denominator)

    return p_value


def longest_run_test(filename: str) -> float:
    """
    Тест на самую длинную последовательность единиц в блоке.

    Args:
        filename: Файл с последовательностью.

    Returns:
        Значение p-value.
    """

    bit_sequence = load_bit_sequence(filename)

    M = 8
    N = 128
    K = N // M

    v = [0, 0, 0, 0]

    for i in range(0, N, M):
        block = bit_sequence[i : i + M]

        max_run = 0
        run = 0

        for bit in block:
            if bit == "1":
                run += 1
                max_run = max(max_run, run)
            else:
                run = 0

        if max_run <= 1:
            v[0] += 1

        elif max_run == 2:
            v[1] += 1

        elif max_run == 3:
            v[2] += 1

        else:
            v[3] += 1

    pi = [0.2148, 0.3672, 0.2305, 0.1875]

    chi2 = 0

    for i in range(4):
        chi2 += ((v[i] - K * pi[i]) ** 2) / (K * pi[i])

    p_value = gammaincc(3 / 2, chi2 / 2)

    return p_value


def run_tests(filename: str, name: str) -> str:
    """
    Запустить все тесты для одной последовательности.

    Args:
        filename: Файл последовательности.
        name: Название последовательности.

    Returns:
        Текст с результатами тестов.
    """

    p1 = frequency_test(filename)
    p2 = runs_test(filename)
    p3 = longest_run_test(filename)

    result = f"""
{name} sequence:

Frequency Test P-value = {p1}
Runs Test P-value = {p2}
Longest Run Test P-value = {p3}

Test results:
Frequency Test: {"PASS" if p1 >= 0.01 else "FAIL"}
Runs Test: {"PASS" if p2 >= 0.01 else "FAIL"}
Longest Run Test: {"PASS" if p3 >= 0.01 else "FAIL"}

"""

    return result


def main() -> None:
    """
    Основная функция программы.
    """

    cpp_file = "sequence_cpp.txt"
    java_file = "sequence_java.txt"

    cpp_results = run_tests(cpp_file, "C++")
    java_results = run_tests(java_file, "Java")

    print(cpp_results)
    print(java_results)

    with open("results.txt", "w", encoding="utf-8") as file:
        file.write(cpp_results)
        file.write(java_results)


if __name__ == "__main__":
    main()
