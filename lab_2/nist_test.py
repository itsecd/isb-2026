import math

from scipy.special import gammaincc

from consts import BLOCK_SIZE, PI


def test_frequency(text: str) -> float:
    """
    Frequency NIST test.
    Return P value for this text
    """
    Sn = text.count("1") - text.count("0")
    Sn *= 1 / (len(text)) ** 0.5

    return math.erfc(Sn / 2 ** 0.5)