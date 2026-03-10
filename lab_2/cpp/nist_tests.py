import math
from typing import List


def read_bit_sequence(file_path: str) -> List[int]:
    """
    Read a bit sequence from a file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        data = file.read()

    bits = [int(bit) for bit in data if bit in ("0", "1")]
    return bits


def frequency_monobit_test(bits: List[int]) -> float:
    """
    Perform the Frequency Test.
    """
    n = len(bits)
    if n == 0:
        return 0.0

    s = sum(1 if bit == 1 else -1 for bit in bits)
    s_obs = abs(s) / math.sqrt(n)
    p_value = math.erfc(s_obs / math.sqrt(2))

    return p_value


def runs_test(bits: List[int]) -> float:
    """
    Perform the Runs Test (NIST SP 800-22).
    """
    n = len(bits)
    if n == 0:
        return 0.0

    pi = sum(bits) / n

    if abs(pi - 0.5) >= (2 / math.sqrt(n)):
        return 0.0

    runs = 1
    for i in range(1, n):
        if bits[i] != bits[i - 1]:
            runs += 1

    numerator = abs(runs - (2 * n * pi * (1 - pi)))
    denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)

    if denominator == 0:
        return 0.0

    p_value = math.erfc(numerator / denominator)
    return p_value


def longest_run_of_ones_test(bits: List[int]) -> float:
    """
    Perform the Longest Run of Ones in a Block Test (NIST SP 800-22).
    """
    n = len(bits)
    if n < 128:
        return 0.0  

    if n < 6272:
        M = 8
        K = 3
        pi_probs = [0.21484375, 0.3671875, 0.23046875, 0.1875]
    elif n < 750000:
        M = 128
        K = 5
        pi_probs = [0.1174035788, 0.242955959, 0.24936348, 0.175287612, 0.102701071, 0.112288299]
    else:
        M = 10000
        K = 6
        pi_probs = [0.0882, 0.2092, 0.2483, 0.1933, 0.1208, 0.0675, 0.0727]

    num_blocks = n // M
    frequencies = [0] * (K + 1)

    for i in range(num_blocks):
        block = bits[i * M: (i + 1) * M]
        max_run = 0
        current_run = 0

        for bit in block:
            if bit == 1:
                current_run += 1
                if current_run > max_run:
                    max_run = current_run
            else:
                current_run = 0

        if M == 8:
            if max_run <= 1:
                frequencies[0] += 1
            elif max_run == 2:
                frequencies[1] += 1
            elif max_run == 3:
                frequencies[2] += 1
            else:
                frequencies[3] += 1
        elif M == 128:
            if max_run <= 4:
                frequencies[0] += 1
            elif max_run == 5:
                frequencies[1] += 1
            elif max_run == 6:
                frequencies[2] += 1
            elif max_run == 7:
                frequencies[3] += 1
            elif max_run == 8:
                frequencies[4] += 1
            else:
                frequencies[5] += 1
        else:
            if max_run <= 10:
                frequencies[0] += 1
            elif max_run == 11:
                frequencies[1] += 1
            elif max_run == 12:
                frequencies[2] += 1
            elif max_run == 13:
                frequencies[3] += 1
            elif max_run == 14:
                frequencies[4] += 1
            elif max_run == 15:
                frequencies[5] += 1
            else:
                frequencies[6] += 1

    chi_squared = 0.0
    for i in range(K + 1):
        expected = num_blocks * pi_probs[i]
        chi_squared += ((frequencies[i] - expected) ** 2) / expected

    x = chi_squared / 2.0
    nu = K / 2.0

    if nu == 1.5:
        return math.erfc(math.sqrt(x)) + (2.0 / math.sqrt(math.pi)) * math.sqrt(x) * math.exp(-x)
    elif nu == 2.5:
        sqrt_x = math.sqrt(x)
        return math.erfc(sqrt_x) + (2.0 / math.sqrt(math.pi)) * sqrt_x * math.exp(-x) + (
                    4.0 / (3.0 * math.sqrt(math.pi))) * (x ** 1.5) * math.exp(-x)
    elif nu == 3.0:
        return math.exp(-x) * (1.0 + x + (x ** 2) / 2.0)
    else:
        return 0.0


def main() -> None:
    """
    Run all NIST tests for the bit sequence from results.txt and append to result.txt.
    """
    input_file = "results.txt"

    try:
        bits = read_bit_sequence(input_file)
    except FileNotFoundError:
        print(f"Ошибка: Файл {input_file} не найден.")
        return

    freq_p = frequency_monobit_test(bits)
    runs_p = runs_test(bits)
    longest_run_p = longest_run_of_ones_test(bits)

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