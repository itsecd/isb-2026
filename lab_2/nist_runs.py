import math
from typing import Optional, Tuple


def runs_test(seq: str) -> Tuple[float, Optional[int], float, bool]:
    """Выполняет тест серий NIST и возвращает (pi, Vn или None, p-value, выполнено_условие)."""
    n: int = len(seq)
    ones: int = sum(1 for c in seq if c == "1")
    pi: float = ones / n

    if abs(pi - 0.5) >= (2.0 / math.sqrt(n)):
        return pi, None, 0.0, False

    vn: int = 1 + sum(1 for i in range(n - 1) if seq[i] != seq[i + 1])

    num: float = abs(vn - (2.0 * n * pi * (1.0 - pi)))
    den: float = 2.0 * math.sqrt(2.0 * n) * pi * (1.0 - pi)
    p_value: float = math.erfc(num / den)

    return pi, vn, p_value, True