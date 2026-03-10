import math
from typing import Tuple, List


def read_sequence(path: str) -> str:
    """Read binary sequence from file"""
    with open(path, encoding="utf-8") as file:
        return file.read().strip()


def frequency_test(bits: str) -> float:
    """Frequency Test"""
    n = len(bits)

    s = sum(1 if bit == "1" else -1 for bit in bits)

    s_obs = abs(s) / math.sqrt(n)
    p_value = math.erfc(s_obs / math.sqrt(2))

    return p_value


def runs_test(bits: str) -> float:
    """Runs Test"""
    n = len(bits)

    pi = bits.count("1") / n

    if abs(pi - 0.5) >= (2 / math.sqrt(n)):
        return 0.0

    runs = 1

    for i in range(1, n):
        if bits[i] != bits[i - 1]:
            runs += 1

    numerator = abs(runs - 2 * n * pi * (1 - pi))
    denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)

    p_value = math.erfc(numerator / denominator)

    return p_value


def longest_run_test(bits: str) -> Tuple[float, List[int]]:
    """Longest Run of Ones Test"""
    block_size = 8
    num_blocks = len(bits) // block_size

    counts = [0, 0, 0, 0]

    for i in range(num_blocks):
        block = bits[i * block_size:(i + 1) * block_size]

        longest = 0
        current = 0

        for bit in block:
            if bit == "1":
                current += 1
                longest = max(longest, current)
            else:
                current = 0

        if longest <= 1:
            counts[0] += 1
        elif longest == 2:
            counts[1] += 1
        elif longest == 3:
            counts[2] += 1
        else:
            counts[3] += 1

    probabilities = [0.2148, 0.3672, 0.2305, 0.1875]

    chi_square = 0

    for i in range(4):
        expected = num_blocks * probabilities[i]
        chi_square += ((counts[i] - expected) ** 2) / expected

    return chi_square, counts


def compile_analysis(bits: str, language: str) -> str:
    """Run tests and return formatted result"""
    p_value_freq = frequency_test(bits)
    p_value_runs = runs_test(bits)
    chi_square, counts = longest_run_test(bits)

    result = (
        f"\nFor {language}:\n"
        f"Frequency test P-value: {p_value_freq}\n"
        f"Runs test P-value: {p_value_runs}\n"
        f"Longest run test counts: {counts}\n"
        f"Chi-square: {chi_square}\n"
    )

    return result


if __name__ == "__main__":

    bits = read_sequence("sequences/seq_python.txt")

    results = ""
    results += compile_analysis(bits, "Python")
    results += compile_analysis(bits, "Java")
    results += compile_analysis(bits, "C++")

    print(results)

    with open("result.txt", "w", encoding="utf-8") as file:
        file.write(results)

    print("Results saved to result.txt")