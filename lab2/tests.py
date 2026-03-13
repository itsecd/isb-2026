import math
import sys
from scipy.special import gammaincc, erfc

def monobit_test(sequence):
    """
    Частотный побитовый тест
    """
    n = len(sequence)
    s = sum(1 if bit == '1' else -1 for bit in sequence)
    s_obs = abs(s) / math.sqrt(n)
    p_value = erfc(s_obs / math.sqrt(2))
    return p_value

def runs_test(sequence):
    """
    Тест на серии
    """
    n = len(sequence)
    pi = sequence.count('1') / n

    if abs(pi - 0.5) >= (2.0 / math.sqrt(n)):
        return 0.0

    v_n = 0
    for i in range(n - 1):
        if sequence[i] != sequence[i+1]:
            v_n += 1

    numerator = abs(v_n - 2 * n * pi * (1 - pi))
    denominator = 2 * math.sqrt(2 * n * pi * (1 - pi))

    if denominator == 0:
        return 0.0

    p_value = erfc(numerator / denominator)
    return p_value


def longest_run_ones_block_test(sequence):
    """
    Тест на самую длинную последовательность единиц в блоке
    """
    n = len(sequence)
    m = 8
    n_blocks = n // m

    max_runs = []
    for i in range(n_blocks):
        block = sequence[i * m: (i + 1) * m]
        max_run = 0
        current_run = 0

        for bit in block:
            if bit == '1':
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 0
        max_runs.append(max_run)

    v = [0, 0, 0, 0]
    for run in max_runs:
        if run <= 1:
            v[0] += 1
        elif run == 2:
            v[1] += 1
        elif run == 3:
            v[2] += 1
        else:
            v[3] += 1

    pi = [0.2148, 0.3672, 0.2305, 0.1875]

    chi_square = 0
    for i in range(4):
        expected = n_blocks * pi[i]
        chi_square += ((v[i] - expected) ** 2) / expected

    p_value = gammaincc(1.5, chi_square / 2.0)

    return p_value


def main():
    if len(sys.argv) > 1:
        seq = sys.argv[1]
    else:
        seq = input("Введите бинарную последовательность (128 бит): ").strip()

    if len(seq) != 128 or not all(c in '01' for c in seq):
        print("Ошибка: Последовательность должна содержать ровно 128 бит (0 и 1).")
        return

    p1 = monobit_test(seq)
    res1 = "случайна" if p1 >= 0.01 else "не случайна"
    print(f"1. Частотный побитовый тест: P-value = {p1:.6f} -> {res1}")

    p2 = runs_test(seq)
    res2 = "случайна" if p2 >= 0.01 else "не случайна"
    print(f"2. Тест на одинаковые подряд идущие биты: P-value = {p2:.6f} -> {res2}")

    p3 = longest_run_ones_block_test(seq)
    res3 = "случайна" if p3 >= 0.01 else "не случайна"
    print(f"3. Тест на самую длинную последовательность единиц в блоке: P-value = {p3:.6f} -> {res3}")

if __name__ == "__main__":
    main()
