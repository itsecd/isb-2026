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


def test_identical_bits(text: str) -> float:
    """
    NIST test for a sequence of identical bits.
    Return P value for this text
    """
    ksi = text.count("1") / len(text)
    if not (abs(ksi - 0.5) < 2 / (len(text)) ** 0.5):
        return 0
    Vn = text.count("01") + text.count("10")
    num = abs(Vn - 2 * len(text) * ksi * (1 - ksi))
    denom = 2 * ((2 * len(text)) ** 0.5) * ksi * (1 - ksi)
    return math.erfc(num / denom)
