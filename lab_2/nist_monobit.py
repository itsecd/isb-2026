import math
from typing import Tuple


def monobit_test(seq: str) -> Tuple[int, float]:
    """Выполняет частотный побитовый тест NIST и возвращает (S, p-value)."""
    n: int = len(seq)
    s: int = sum(1 if c == "1" else -1 for c in seq)
    p_value: float = math.erfc(abs(s) / math.sqrt(2.0 * n))
    return s, p_value