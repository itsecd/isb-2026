"""Реализация трёх NIST-тестов с проверкой входных данных и обработкой ошибок."""

import math
import sys
from scipy.special import erfc, gammaincc


def _validate_bits(bits: str) -> None:
    """Проверяет, что bits - непустая строка из '0' и '1'."""
    if not isinstance(bits, str):
        raise ValueError("bits должна быть строкой")
    if len(bits) == 0:
        raise ValueError("bits не может быть пустой строкой")
    if not all(c in ('0', '1') for c in bits):
        raise ValueError("bits должна содержать только символы '0' и '1'")


def monobit_test(bits: str) -> float:
    """
    Частотный (монобитный) тест.

    Parameters
    ----------
    bits : str
        Бинарная строка из символов '0' и '1'.

    Returns
    -------
    float
        P-value. В случае ошибки возвращает -1.0.
    """
    try:
        _validate_bits(bits)
        n = len(bits)
        count_ones = bits.count('1')
        s_n = abs(2 * count_ones - n)
        p_value = erfc(s_n / math.sqrt(2 * n))
        return p_value
    except Exception as e:
        print(f"Ошибка в monobit_test: {e}", file=sys.stderr)
        return -1.0


def runs_test(bits: str) -> float:
    """
    Тест прогонов (серий).

    Parameters
    ----------
    bits : str
        Бинарная строка.

    Returns
    -------
    float
        P-value. При ошибке или неприменимости теста возвращает -1.0.
    """
    try:
        _validate_bits(bits)
        n = len(bits)
        pi = bits.count('1') / n
        if abs(pi - 0.5) >= (2.0 / math.sqrt(n)):
            return 0.0

        runs = 1
        for i in range(1, n):
            if bits[i] != bits[i - 1]:
                runs += 1

        numerator = abs(runs - 2 * n * pi * (1 - pi))
        denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)
        if denominator == 0:
            return 0.0
        p_value = erfc(numerator / denominator)
        return p_value
    except Exception as e:
        print(f"Ошибка в runs_test: {e}", file=sys.stderr)
        return -1.0


def longest_run_ones_in_block(bits: str) -> float:
    """
    Тест на самую длинную серию единиц в блоке.

    Parameters
    ----------
    bits : str
        Бинарная строка.

    Returns
    -------
    float
        P-value, или -1.0 если строка слишком короткая или произошла ошибка.
    """
    try:
        _validate_bits(bits)
        n = len(bits)
        if n < 128:
            return -1.0

        if n < 6272:
            m = 8
            v = [1, 2, 3, 4]
            pi = [0.21484375, 0.36718750, 0.23046875, 0.18750000]
        elif n < 75000:
            m = 128
            v = [4, 5, 6, 7, 8, 9]
            pi = [
                0.1174035788, 0.2429559590, 0.2493634830,
                0.1751770600, 0.1027010710, 0.1123988470
            ]
        else:
            m = 10000
            v = [10, 11, 12, 13, 14, 15, 16]
            pi = [
                0.0882, 0.2092, 0.2483, 0.1933,
                0.1208, 0.0675, 0.0727
            ]

        num_blocks = n // m
        counts = [0] * len(pi)

        for block_idx in range(num_blocks):
            block = bits[block_idx * m:(block_idx + 1) * m]
            longest = 0
            cur = 0
            for bit in block:
                if bit == '1':
                    cur += 1
                    if cur > longest:
                        longest = cur
                else:
                    cur = 0

            if longest <= v[0]:
                counts[0] += 1
            elif longest >= v[-1]:
                counts[-1] += 1
            else:
                for i in range(len(v) - 1):
                    if v[i] < longest <= v[i + 1]:
                        counts[i + 1] += 1
                        break

        chi2 = 0.0
        for i in range(len(pi)):
            expected = num_blocks * pi[i]
            chi2 += (counts[i] - expected) ** 2 / expected

        degrees = len(pi) - 1
        p_value = gammaincc(degrees / 2.0, chi2 / 2.0)
        return p_value
    except Exception as e:
        print(f"Ошибка в longest_run_ones_in_block: {e}", file=sys.stderr)
        return -1.0