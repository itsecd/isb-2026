import math
from typing import List, Tuple
from scipy.special import gammaincc


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
    ones = bits.count('1')
    pi = ones / n
    if abs(pi - 0.5) > 2 / math.sqrt(n):
        return 0.0  # тест не применим
    
    runs = 1
    for i in range(1, n):
        if bits[i] != bits[i - 1]:
            runs += 1

    numerator = 2 * ones * (n - ones) / n + 1
    denominator = (numerator - 1) * (numerator - 2) / (n - 1)
    p_value = math.erfc(abs(runs - numerator) / math.sqrt(2 * denominator))
    return p_value


def longest_run_test(bits: str) -> float:
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
    chi_square = sum(((counts[i] - num_blocks * probabilities[i]) ** 2) / (num_blocks * probabilities[i]) for i in range(4))
    df = 3
    p_value = gammaincc(df / 2, chi_square / 2)
    return p_value


def status(p_value: float) -> str:
    """Return 'Passed' or 'Failed' based on p-value"""
    if p_value >= 0.01:
        return "Passed"
    else:
        return "Failed"


def compile_analysis(bits: str, language: str) -> (str, str):
    """Return console string with P-values and file string with Passed/Failed"""
    p_freq = frequency_test(bits)
    p_runs = runs_test(bits)
    p_long = longest_run_test(bits)

    console_str = (
        f"\nFor {language}:\n"
        f"Frequency test P-value: {p_freq}\n"
        f"Runs test P-value: {p_runs}\n"
        f"Longest run test P-value: {p_long}\n"
    )

    file_str = (
        f"\nFor {language}:\n"
        f"Frequency test: {status(p_freq)}\n"
        f"Runs test: {status(p_runs)}\n"
        f"Longest run test: {status(p_long)}\n"
    )

    return console_str, file_str


if __name__ == "__main__":
    sequences = [("Python", "sequences/seq_python.txt"),
                 ("Java", "sequences/seq_java.txt"),
                 ("C++", "sequences/seq_cpp.txt")]

    res_cons, res_txt = "", ""

    for lang, path in sequences:
        cons, f_res = compile_analysis(read_sequence(path), lang)
        res_cons += cons
        res_txt  += f_res

    print(res_cons)

    with open("result.txt", "w", encoding="utf-8") as f:
        f.write(res_txt)

    print("Results saved to result.txt")