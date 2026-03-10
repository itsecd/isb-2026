import math
from scipy.stats import chi2
import const


def read_sequence(filepath):
    try:
        with open(filepath, "r") as f:
            data = f.read().strip()
            sequence = [int(b) for b in data if b in "01"][: const.N]
            return sequence
    except Exception as e:
        print(f"Error reading file: {e}")
        return []


def test_frequency(seq: list[int]) -> tuple[float, str]:
    n = len(seq)
    if n == 0:
        return 0.0, "FAIL"

    s_n = sum(1 if x == 1 else -1 for x in seq)
    s_obs = abs(s_n) / math.sqrt(n)
    p_val = math.erfc(s_obs / math.sqrt(2))

    verdict = "PASS" if p_val >= 0.01 else "FAIL"
    return p_val, verdict


def test_runs(seq: list[int]) -> tuple[float, str]:
    n = len(seq)
    pi = sum(seq) / n

    if abs(pi - 0.5) >= 2 / math.sqrt(n) or pi == 0.0 or pi == 1.0:
        return 0.0, "FAIL"

    v_n = sum(1 for i in range(n - 1) if seq[i] != seq[i + 1])

    denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)
    p_val = math.erfc(abs(v_n - 2 * n * pi * (1 - pi)) / denominator)

    return p_val, "PASS" if p_val >= 0.01 else "FAIL"


def test_longest_run_of_ones(sequence: list[int]) -> tuple[float, str, float, list]:
    n = len(sequence)

    if n == 0 or n % const.BLOCK_SIZE_M != 0:
        return 0.0, "FAIL", 0.0, [0, 0, 0, 0]

    num_blocks = n // const.BLOCK_SIZE_M
    V = [0, 0, 0, 0]

    for i in range(num_blocks):
        block_start = i * const.BLOCK_SIZE_M
        block = sequence[block_start : block_start + const.BLOCK_SIZE_M]

        max_run = 0
        current_run = 0
        for bit in block:
            if bit == 1:
                current_run += 1
            else:
                max_run = max(max_run, current_run)
                current_run = 0
        max_run = max(max_run, current_run)

        if max_run <= 1:
            V[0] += 1
        elif max_run == 2:
            V[1] += 1
        elif max_run == 3:
            V[2] += 1
        elif max_run >= 4:
            V[3] += 1

    chi_square_stat = 0.0
    for i in range(4):
        E_i = num_blocks * const.CONST_PI[i]
        if E_i > 0:
            term = (V[i] - E_i) ** 2 / E_i
            chi_square_stat += term

    p_value = chi2.sf(1.5, chi_square_stat / 2)
    verdict = "PASS" if p_value >= 0.01 else "FAIL"

    return p_value, verdict, chi_square_stat


def main():
    input_file = input("Enter sequence file path: ")
    output_file = input("Enter result file name: ")
    seq = read_sequence(input_file)

    if not seq:
        print("Failed to read sequence. Exiting.")
        return

    p1, v1 = test_frequency(seq)
    p2, v2 = test_runs(seq)
    p3, v3, chi2_stat = test_longest_run_of_ones(seq)

    output = f"""
--- NIST Test Results ---
Test Parameters: N={const.N}, M={const.BLOCK_SIZE_M}
File Analyzed: {input_file}
----------------------------------
2.1 Frequency Test:      P-value = {p1:.6f} ({v1})
2.2 Runs Test:           P-value = {p2:.6f} ({v2})
2.3 LST: X^2 = {chi2_stat:.4f}. P-value = {p3:.6f} ({v3})
"""

    with open(output_file, "w") as f:
        f.write(output)


if __name__ == "__main__":
    main()
