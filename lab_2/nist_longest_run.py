from typing import List, Tuple


def longest_run_in_block_prepare(seq: str) -> Tuple[List[int], float, int, float, float]:
    """Считает параметры для калькулятора Гамма-функции: (N=128,M=8): v, chi2, K, a=K/2, x=chi2/2."""
    n: int = len(seq)
    if n != 128:
        raise ValueError("Этот вариант теста рассчитан на N=128.")

    m: int = 8
    blocks: List[str] = [seq[i:i + m] for i in range(0, n, m)]
    if len(blocks) != 16:
        raise RuntimeError("Ожидается 16 блоков по 8 бит.")

    def max_run_ones(block: str) -> int:
        """Находит максимальную длину подряд идущих единиц в одном блоке."""
        cur: int = 0
        best: int = 0
        for ch in block:
            if ch == "1":
                cur += 1
                if cur > best:
                    best = cur
            else:
                cur = 0
        return best

    # Категории:
    # v1: максимум <= 1; v2: максимум=2; v3: максимум=3; v4: максимум>=4
    v1 = v2 = v3 = v4 = 0
    for b in blocks:
        r: int = max_run_ones(b)
        if r <= 1:
            v1 += 1
        elif r == 2:
            v2 += 1
        elif r == 3:
            v3 += 1
        else:
            v4 += 1

    v: List[int] = [v1, v2, v3, v4]

    # Вероятности π_i для M=8
    pis: List[float] = [0.2148, 0.3672, 0.2305, 0.1875]

    chi2: float = 0.0
    for i in range(4):
        expected: float = 16.0 * pis[i]
        chi2 += (v[i] - expected) ** 2 / expected

    k: int = 3
    a: float = k / 2.0
    x: float = chi2 / 2.0
    return v, chi2, k, a, x


def parse_p_value(user_input: str) -> float:
    """Преобразует введённое пользователем p-value в float."""
    s: str = user_input.strip().replace(",", ".")
    p: float = float(s)
    if not (0.0 <= p <= 1.0):
        raise ValueError("P-value должно быть в диапазоне [0; 1].")
    return p