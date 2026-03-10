import math
from typing import List


def read_bit_sequence(file_path: str) -> List[int]:
    """
    Read a bit sequence from a file.

    The file should contain a sequence of 0 and 1 characters.

    Args:
        file_path: Path to the file containing the bit sequence.

    Returns:
        List of integers (0 or 1).
    """
    with open(file_path, "r", encoding="utf-8") as file:
        data = file.read()

    bits = [int(bit) for bit in data if bit in ("0", "1")]
    return bits


def frequency_monobit_test(bits: List[int]) -> float:
    """
    Perform the Frequency Test.

    Checks whether the number of ones and zeros in the sequence
    are approximately the same.

    Args:
        bits: Bit sequence.

    Returns:
        p-value of the test.
    """
    n = len(bits)
    s = sum(1 if bit == 1 else -1 for bit in bits)

    s_obs = abs(s) / math.sqrt(n)
    p_value = math.erfc(s_obs / math.sqrt(2))

    return p_value


def runs_test(bits: List[int]) -> float:
    """
    Perform the Runs Test.

    Checks whether the number of runs of consecutive bits
    is consistent with randomness.

    Args:
        bits: Bit sequence.

    Returns:
        p-value of the test.
    """
    n = len(bits)
    pi = sum(bits) / n

    if abs(pi - 0.5) >= (2 / math.sqrt(n)):
        return 0.0

    runs = 1
    for i in range(1, n):
        if bits[i] != bits[i - 1]:
            runs += 1

    numerator = abs(runs - (2 * n * pi * (1 - pi)))
    denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)

    p_value = math.erfc(numerator / denominator)
    return p_value


def longest_run_of_ones_test(bits: List[int], block_size: int = 8) -> float:
    """
    Perform the Longest Run of Ones in a Block Test.

    The sequence is divided into blocks and the longest run
    of ones in each block is evaluated.

    Args:
        bits: Bit sequence.
        block_size: Size of each block.

    Returns:
        Approximate p-value of the test.
    """
    n = len(bits)
    num_blocks = n // block_size

    if num_blocks == 0:
        raise ValueError("Sequence too short for chosen block size.")

    blocks = [
        bits[i * block_size:(i + 1) * block_size]
        for i in range(num_blocks)
    ]

    longest_runs = []

    for block in blocks:
        max_run = 0
        current_run = 0

        for bit in block:
            if bit == 1:
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 0

        longest_runs.append(max_run)

    mean_run = sum(longest_runs) / len(longest_runs)
    variance = sum((r - mean_run) ** 2 for r in longest_runs) / len(longest_runs)

    if variance == 0:
        return 0.0

    z = abs(mean_run - (block_size / 2)) / math.sqrt(variance)
    p_value = math.erfc(z / math.sqrt(2))

    return p_value


def main() -> None:
    """
    Run all NIST tests for the bit sequence from results.txt.
    """
    bits = read_bit_sequence("results.txt")

    freq_p = frequency_monobit_test(bits)
    runs_p = runs_test(bits)
    longest_run_p = longest_run_of_ones_test(bits)

    print("NIST Statistical Tests Results")
    print("-----------------------------")
    print(f"Frequency (Monobit) Test p-value: {freq_p:.6f}")
    print(f"Runs Test p-value: {runs_p:.6f}")
    print(f"Longest Run of Ones Test p-value: {longest_run_p:.6f}")


if __name__ == "__main__":
    main()