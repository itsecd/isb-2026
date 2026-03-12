import math
import sys


def read_bit_sequence(file_path: str) -> str:
    """
    Reading bit string from file
    """
    with open(file_path, "r", encoding="utf-8") as file:
        data = file.read()
    return "".join([bit for bit in data if bit in ("0", "1")])


def frequency_test(bit_string: str) -> float:
    """
    Frequency monobit test
    """
    n = len(bit_string)
    if n == 0:
        return 0.0

    sum_x = 0
    for bit in bit_string:
        sum_x += 1 if bit == '1' else -1

    s_obs = abs(sum_x) / math.sqrt(n)
    p_value = math.erfc(s_obs / math.sqrt(2))

    return p_value


def runs_test(bit_string: str) -> float:
    """
    Runs test for consecutive identical bits
    """
    n = len(bit_string)
    if n == 0:
        return 0.0

    ones = bit_string.count('1')
    pi = ones / n

    v_n = 0
    for i in range(n - 1):
        if bit_string[i] != bit_string[i + 1]:
            v_n += 1

    condition = abs(pi - 0.5) < (2 / math.sqrt(n))

    if condition:
        numerator = abs(v_n - 2 * n * pi * (1 - pi))
        denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)
        if denominator == 0:
            return 0.0
        p_value = math.erfc(numerator / denominator)
    else:
        p_value = 0.0

    return p_value


def incomplete_gamma_lower(a: float, x: float, epsilon: float = 1e-10, max_iter: int = 1000) -> float:
    """
     Lower incomplete gamma function using a series expansion
    """
    if x < 0:
        return 0.0

    term = 1.0 / a
    result = term
    n = 1

    while n < max_iter:
        term *= x / (a + n)
        result += term
        if term < epsilon:
            break
        n += 1

    return (x ** a) * math.exp(-x) * result


def longest_run_test(bit_string: str) -> float:
    """
    Test for the longest run of ones in a block
    """
    n = len(bit_string)
    M = 8
    N = n // M

    if N < 3:
        return 0.0

    # Точные вероятности по стандарту NIST для M = 8
    pi_probs = [0.21484375, 0.3671875, 0.23046875, 0.1875]
    v = [0, 0, 0, 0]

    for i in range(N):
        block = bit_string[i * M: (i + 1) * M]

        max_run = 0
        current = 0
        for bit in block:
            if bit == '1':
                current += 1
                max_run = max(max_run, current)
            else:
                current = 0

        if max_run <= 1:
            v[0] += 1
        elif max_run == 2:
            v[1] += 1
        elif max_run == 3:
            v[2] += 1
        else:
            v[3] += 1

    chi_square = 0
    for i in range(4):
        expected = N * pi_probs[i]
        chi_square += ((v[i] - expected) ** 2) / expected

    a = 1.5
    x = chi_square / 2.0

    gamma_lower = incomplete_gamma_lower(a, x)
    gamma_full = math.gamma(a)
    p_value = 1.0 - (gamma_lower / gamma_full)

    return p_value


def main() -> None:
    """
    Run all NIST tests for the bit sequence from results.txt.
    """
    input_file = "results.txt"

    try:
        bits = read_bit_sequence(input_file)
    except FileNotFoundError:
        print(f"Ошибка: Файл {input_file} не найден. Проверьте путь.")
        sys.exit(1)

    if not bits:
        print("Ошибка: Файл пуст или не содержит битовой последовательности.")
        sys.exit(1)

    freq_p = frequency_test(bits)
    runs_p = runs_test(bits)
    longest_run_p = longest_run_test(bits)

    report = (
        "NIST Statistical Tests Results\n"
        "-----------------------------\n"
        f"Frequency (Monobit) Test p-value: {freq_p:.6f}\n"
        f"Runs Test p-value: {runs_p:.6f}\n"
        f"Longest Run of Ones Test p-value: {longest_run_p:.6f}\n"
    )

    print(report)

    with open(input_file, "a", encoding="utf-8") as f:
        f.write("\n" + report)
        print(f"--- Результаты успешно добавлены в {input_file} ---")


if __name__ == "__main__":
    main()