import math
from scipy.special import gammaincc

from config import RUN_BLOCK, EXPECTED_PROBABILITIES


def monobit_test(seq: str) -> float:
    n = len(seq)
    balance = sum(1 if bit == "1" else -1 for bit in seq)
    statistic = abs(balance) / math.sqrt(n)
    return math.erfc(statistic / math.sqrt(2))


def runs_test(seq: str) -> float:
    n = len(seq)
    ones_ratio = seq.count("1") / n

    if ones_ratio == 0 or ones_ratio == 1:
        return 0.0

    if abs(ones_ratio - 0.5) > (2 / math.sqrt(n)):
        return 0.0

    transitions = sum(seq[i] != seq[i + 1] for i in range(n - 1))
    expected = 2 * n * ones_ratio * (1 - ones_ratio)
    deviation = abs(transitions - expected)
    denominator = 2 * math.sqrt(2 * n) * ones_ratio * (1 - ones_ratio)

    return math.erfc(deviation / denominator)


def longest_block_run(seq: str) -> float:
    block_count = len(seq) // RUN_BLOCK
    categories = [0, 0, 0, 0]

    for start in range(0, block_count * RUN_BLOCK, RUN_BLOCK):
        block = seq[start:start + RUN_BLOCK]
        longest = max(map(len, block.split("0")))

        index = (
            0 if longest <= 1
            else 1 if longest == 2
            else 2 if longest == 3
            else 3
        )

        categories[index] += 1

    chi_square = sum(
        ((categories[i] - block_count * EXPECTED_PROBABILITIES[i]) ** 2) /
        (block_count * EXPECTED_PROBABILITIES[i])
        for i in range(4)
    )

    return gammaincc(1.5, chi_square / 2)
