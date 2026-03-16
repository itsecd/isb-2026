import math
import os
from typing import Tuple, Optional
from scipy.special import gammainc
from constants import P, THRESHOLD


def read_txt_file(file_path: str) -> Optional[str]:
    """
    A function for reading a text file.
    :param file_path: path to the text file
    :return: text file as a string
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read().strip()
            sequence = ''.join(c for c in content if c in '01')
            return sequence if sequence else None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None


def write_txt_file(data: str, file_path: str) -> None:
    """
    A function for writing text to a file
    :param data: data to enter into the file
    :param file_path: the path to the file to save the data
    :return: None
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(data))
    except Exception as e:
        print(f"Error writing to file {file_path}: {e}")


def frequency_test(sequence: str) -> float:
    """
    Frequency bitwise test
    :param sequence: bitwise sequence
    :return: P-value
    """
    n = len(sequence)
    x_i = [1 if bit == '1' else -1 for bit in sequence]
    s = sum(x_i) / math.sqrt(n)
    p_value = math.erfc(abs(s) / math.sqrt(2))

    return p_value


def runs_test(sequence: str) -> float:
    """
    A test for identical consecutive bits
    :param sequence: bitwise sequence
    :return: P-value
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


def block_statistic(sequence: str) -> Tuple[int, int, int, int]:
    """
    Calculates statistic of identical bits in each block of 8 bits in the sequence
    :param sequence: bitwise sequence
    :return: statistic (v1, v2, v3, v4)
    """
    v1, v2, v3, v4 = 0, 0, 0, 0

    for i in range(0, len(sequence), 8):
        block = sequence[i:i + 8]
        if len(block) < 8:
            continue

        max_len = 0
        current_len = 0

        for bit in block:
            if bit == "1":
                current_len += 1
                max_len = max(max_len, current_len)
            else:
                current_len = 0

        if max_len <= 1:
            v1 += 1
        elif max_len == 2:
            v2 += 1
        elif max_len == 3:
            v3 += 1
        else:
            v4 += 1

    return v1, v2, v3, v4


def longest_run_test(statistic: Tuple[int, int, int, int]) -> float:
    """
    Test for the longest sequence of units in a block
    :param statistic: statistic from block_statistic
    :return: P-value
    """
    chi_square = 0.0
    blocks = sum(statistic)

    if blocks == 0:
        return 0.0

    for i in range(4):
        expected = blocks * P[i]
        chi_square += ((statistic[i] - expected) ** 2) / expected

    p_value = gammainc(3 / 2, chi_square / 2)
    return p_value


def save_results_to_file(filename: str, sequence_name: str,
                         freq_p: float, runs_p: float, long_p: float) -> None:
    """
    Save test results to a file
    :param filename: output filename
    :param sequence_name: name of the sequence
    :param freq_p: frequency test p-value
    :param runs_p: runs test p-value
    :param long_p: longest run test p-value
    :return: None
    """
    freq_pass = freq_p >= THRESHOLD
    runs_pass = runs_p >= THRESHOLD
    long_pass = long_p >= THRESHOLD

    result_text = f"""NIST Statistical Test Results
{'=' * 50}
Sequence: {sequence_name}
Length: 128 bits

1. Frequency Test (Monobit Test)
   P-value: {freq_p:.6f}
   Result: {'PASSED' if freq_pass else 'FAILED'}

2. Runs Test
   P-value: {runs_p:.6f}
   Result: {'PASSED' if runs_pass else 'FAILED'}

3. Longest Run Test
   P-value: {long_p:.6f}
   Result: {'PASSED' if long_pass else 'FAILED'}

{'=' * 50}
Test passed if P-value >= {THRESHOLD}
"""
    write_txt_file(result_text, filename)


def print_test_results(name: str, freq_p: float, runs_p: float, long_p: float) -> None:
    """
    Print test results to console
    :param name: sequence name
    :param freq_p: frequency test p-value
    :param runs_p: runs test p-value
    :param long_p: longest run test p-value
    :return: None
    """
    freq_pass = "PASSED" if freq_p >= THRESHOLD else "FAILED"
    runs_pass = "PASSED" if runs_p >= THRESHOLD else "FAILED"
    long_pass = "PASSED" if long_p >= THRESHOLD else "FAILED"

    print(f"\nTesting {name}:")
    print(f"  Frequency Test: P={freq_p:.6f} - {freq_pass}")
    print(f"  Runs Test: P={runs_p:.6f} - {runs_pass}")
    print(f"  Longest Run Test: P={long_p:.6f} - {long_pass}")


def main() -> None:
    print("NIST Statistical Tests")
    print("=" * 50)

    test_files = [
        ("../task1/seq_generator_cpp.txt", "C++ Generator"),
        ("../task1/seq_generator_java.txt", "Java Generator")
    ]

    for filepath, name in test_files:
        sequence = read_txt_file(filepath)

        if not sequence:
            print(f"\nError: Cannot read {filepath}")
            continue

        print(f"\nSequence: {sequence}")

        freq_p = frequency_test(sequence)
        runs_p = runs_test(sequence)
        statistic = block_statistic(sequence)
        long_p = longest_run_test(statistic)

        print_test_results(name, freq_p, runs_p, long_p)

        out_filename = f"result/cpp_results.txt" if "C++" in name else f"result/java_results.txt"
        save_results_to_file(out_filename, name, freq_p, runs_p, long_p)
        print(f"  Results saved to {out_filename}")


if __name__ == "__main__":
    main()