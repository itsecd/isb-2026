import argparse
import math
from scipy.special import gammaincc
from typing import Optional
from values import ALPHA, LONGEST_RUN_BLOCK_SIZE, LONGEST_RUN_EXPECTED_PROBS, LONGEST_RUN_NUM_BLOCKS


def monobit_test(bits: str) -> tuple[float, bool]:
    """
    Частотный побитовый тест.
    Возвращает p-value и результат.
    """
    n = len(bits)
    s_sum = sum(1 if b == '1' else -1 for b in bits)
    s_obs = abs(s_sum) / math.sqrt(n)
    p_value = math.erfc(s_obs / math.sqrt(2))
    return p_value, p_value >= ALPHA


def runs_test(bits: str) -> tuple[Optional[float], bool]:
    """
    Тест на одинаковые подряд идущие биты.
    Возвращает p-value (или None, если тест неприменим) и результат.
    """
    n = len(bits)
    ones = bits.count('1')
    pi = ones / n
    tau = 2.0 / math.sqrt(n)
    if abs(pi - 0.5) >= tau:
        return None, False

    runs = 1
    for i in range(1, n):
        if bits[i] != bits[i-1]:
            runs += 1

    numerator = abs(runs - 2 * n * pi * (1 - pi))
    denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)
    p_value = math.erfc(numerator / denominator)
    return p_value, p_value >= ALPHA


def longest_run_test(bits: str) -> tuple[float, bool]:
    """
    Тест на самую длинную последовательность единиц в блоке.
    Для длины 128 бит размер блока 8.
    Возвращает p-value и результат.
    """
    n = len(bits)
    block_size = LONGEST_RUN_BLOCK_SIZE
    num_blocks = n // block_size
    if num_blocks != LONGEST_RUN_NUM_BLOCKS:
        print(f"Ожидалось {LONGEST_RUN_NUM_BLOCKS} блоков, получено {num_blocks}")

    expected = [p * num_blocks for p in LONGEST_RUN_EXPECTED_PROBS]

    observed = [0, 0, 0, 0]
    for i in range(num_blocks):
        block = bits[i*block_size : (i+1)*block_size]

        max_run = 0
        cur_run = 0
        for b in block:
            if b == '1':
                cur_run += 1
                if cur_run > max_run:
                    max_run = cur_run
            else:
                cur_run = 0
        if max_run <= 1:
            observed[0] += 1
        elif max_run == 2:
            observed[1] += 1
        elif max_run == 3:
            observed[2] += 1
        else:
            observed[3] += 1

    chi2 = sum((obs - exp) ** 2 / exp for obs, exp in zip(observed, expected))
    p_value = gammaincc(1.5, chi2 / 2)
    return p_value, p_value >= ALPHA


def main():
    parser = argparse.ArgumentParser(description='Тестирование бинарных последовательностей.')
    parser.add_argument('files', metavar='FILE', nargs='+', help='файлы с бинарными последовательностями (128 бит)')
    args = parser.parse_args()

    for filename in args.files:
        try:
            with open(filename, 'r') as f:
                bits = f.read().strip()
        except Exception as e:
            print(f"Ошибка чтения файла {filename}: {e}")
            continue

        if len(bits) != 128 or not all(b in '01' for b in bits):
            print(f"Ошибка: файл {filename} должен содержать ровно 128 символов '0' и '1'")
            continue

        print(f"\nАнализ последовательности из файла: {filename}")
        print(f"Последовательность: {bits}\n")

        p_mono, res_mono = monobit_test(bits)
        print(f"Monobit Frequency Test:")
        print(f"  p-value = {p_mono:.4f}  {'ПРОЙДЕН' if res_mono else 'НЕ ПРОЙДЕН'}")

        p_runs, res_runs = runs_test(bits)
        print(f"\nRuns Test:")
        if p_runs is None:
            print("  Тест не применим (частота единиц слишком далека от 0.5)")
        else:
            print(f"  p-value = {p_runs:.4f}  {'ПРОЙДЕН' if res_runs else 'НЕ ПРОЙДЕН'}")

        p_long, res_long = longest_run_test(bits)
        print(f"\nLongest Run of Ones in a Block Test:")
        print(f"  p-value = {p_long:.4f}  {'ПРОЙДЕН' if res_long else 'НЕ ПРОЙДЕН'}")


if __name__ == "__main__":
    main()
