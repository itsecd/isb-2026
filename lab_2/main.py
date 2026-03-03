import math

from scipy.special import gammaincc

from values import P_VALUE, BLOCK_SIZE, PI


def frequency_bits(seq: str) -> float:
    """
    Docstring for frequency_bits

    :param seq: Source sequence
    :type seq: str
    :return: P value of frequency bits test
    :rtype: float
    """
    s_n = (seq.count("1") - seq.count("0")) / math.sqrt(len(seq))
    return math.erfc(s_n / math.sqrt(2))


def count_same_bits(seq: str) -> float:
    """
    Docstring for count_same_bits

    :param seq: Source sequence
    :type seq: str
    :return: P value of count same bits test
    :rtype: float
    """
    one_ratio = seq.count("1") / len(seq)

    if abs(one_ratio - 0.5) > (2 / math.sqrt(len(seq))):
        return 0.0

    switch_count = seq.count("01") + seq.count("10")

    return math.erfc(
        abs(switch_count - (2 * len(seq) * one_ratio * (1 - one_ratio)))
        / (2 * math.sqrt(2 * len(seq) * one_ratio * (1 - one_ratio)))
    )


def max_count_in_block(seq: str) -> float:

    v = [0, 0, 0, 0]
    for i in range(len(seq) // BLOCK_SIZE):
        block = seq[BLOCK_SIZE * i : BLOCK_SIZE * i + BLOCK_SIZE]
        count_of_one = block.count("1")
        if count_of_one <= 1:
            v[0] += 1
        elif count_of_one == 2:
            v[1] += 1
        elif count_of_one == 3:
            v[2] += 1
        else:
            v[3] += 1

    xi = 0
    for i in range(4):
        xi += ((v[i] - 16 * PI[i]) ** 2) / (16 * PI[i])

    return gammaincc(1.5, xi / 2)


def main() -> None:
    """
    Docstring for main
    """


if __name__ == "__main__":
    main()
