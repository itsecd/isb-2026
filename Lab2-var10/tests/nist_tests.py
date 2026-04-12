import math
from scipy.special import erfc, gammaincc

def read_sequence(filepath: str) -> str:
    with open(filepath, 'r') as f:
        seq = ''.join(ch for ch in f.read() if ch in '01')
    return seq.strip()

def frequency_test(seq: str) -> float:
    """Частотный побитовый тест (исправлен: добавлен abs)."""
    n = len(seq)
    x = [1 if bit == '1' else -1 for bit in seq]
    S = abs(sum(x)) / math.sqrt(n)          # <- модуль!
    return erfc(S / math.sqrt(2))

def runs_test(seq: str) -> float:
    """Тест на одинаковые подряд идущие биты (исправлен знаменатель)."""
    n = len(seq)
    ones = seq.count('1')
    zeta = ones / n

    if abs(zeta - 0.5) >= 2.0 / math.sqrt(n):
        return 0.0

    # Число смен битов (без +1)
    V = 0
    for i in range(n - 1):
        if seq[i] != seq[i+1]:
            V += 1

    numerator = abs(V - 2 * n * zeta * (1 - zeta))
    denominator = 2 * math.sqrt(2 * n * zeta * (1 - zeta))   # <- правильный знаменатель
    if denominator == 0:
        return 0.0
    return erfc(numerator / denominator)

def longest_run_test(seq: str) -> float:
    """Тест на самую длинную последовательность единиц в блоке (N=128)."""
    n = len(seq)
    if n != 128:
        raise ValueError("Тест рассчитан на последовательность 128 бит")
    M = 8
    blocks = [seq[i:i+M] for i in range(0, n, M)]
    max_lengths = []
    for block in blocks:
        cur = 0
        best = 0
        for bit in block:
            if bit == '1':
                cur += 1
                best = max(best, cur)
            else:
                cur = 0
        max_lengths.append(best)

    v = [0, 0, 0, 0]
    for run_len in max_lengths:
        if run_len <= 1:
            v[0] += 1
        elif run_len == 2:
            v[1] += 1
        elif run_len == 3:
            v[2] += 1
        else:
            v[3] += 1

    pi = [0.2148, 0.3672, 0.2305, 0.1875]
    chi2 = sum((v[i] - 16 * pi[i]) ** 2 / (16 * pi[i]) for i in range(4))
    return gammaincc(3/2, chi2/2)

def run_all_tests(seq: str, label: str = ""):
    if label:
        print(f"\n=== {label} ===")
    print(f"Длина: {len(seq)}")
    p_freq = frequency_test(seq)
    p_runs = runs_test(seq)
    p_long = longest_run_test(seq)
    print(f"Частотный тест:        P = {p_freq:.6f} -> {'случайная' if p_freq >= 0.01 else 'НЕ случайная'}")
    print(f"Тест на серии:         P = {p_runs:.6f} -> {'случайная' if p_runs >= 0.01 else 'НЕ случайная'}")
    print(f"Тест на длинную серию: P = {p_long:.6f} -> {'случайная' if p_long >= 0.01 else 'НЕ случайная'}")
    if all(p >= 0.01 for p in (p_freq, p_runs, p_long)):
        print("Вывод: Последовательность случайна.")
    else:
        print("Вывод: Последовательность НЕ случайна.")