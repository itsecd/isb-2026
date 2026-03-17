import math
from scipy.special import gammaincc


def read_sequence(filename):
    with open(filename, 'r') as f:
        return f.read().strip()


def frequency_test(seq):
    n = len(seq)
    ones = seq.count('1')
    s_obs = abs(ones - (n - ones)) / math.sqrt(n)
    p_value = math.erfc(s_obs / math.sqrt(2))
    return p_value, ones, n - ones, s_obs


def runs_test(seq):
    n = len(seq)
    ones = seq.count('1')

    runs = 1
    for i in range(1, n):
        if seq[i] != seq[i - 1]:
            runs += 1

    expected = 2 * ones * (n - ones) / n + 1
    variance = (2 * ones * (n - ones) * (2 * ones * (n - ones) - n)) / (n ** 2 * (n - 1))
    s_obs = (runs - expected) / math.sqrt(variance)
    p_value = math.erfc(abs(s_obs) / math.sqrt(2))
    return p_value, runs, expected, s_obs


def longest_run_test(seq):
    n = len(seq)
    M = 8
    N = n // M

    pi = [0.2148, 0.3672, 0.2305, 0.1875]
    v = [0, 0, 0, 0]

    for i in range(0, N * M, M):
        block = seq[i:i + M]
        max_run = 0
        curr = 0
        for bit in block:
            if bit == '1':
                curr += 1
                max_run = max(max_run, curr)
            else:
                curr = 0

        if max_run <= 1:
            v[0] += 1
        elif max_run == 2:
            v[1] += 1
        elif max_run == 3:
            v[2] += 1
        else:
            v[3] += 1

    chi_square = sum(((v[i] - N * pi[i]) ** 2) / (N * pi[i]) for i in range(4))
    p_value = gammaincc(3 / 2, chi_square / 2)
    return p_value, v, chi_square


files = [
    ("C++", "sequence_cpp.txt"),
    ("Java", "sequence_java.txt"),
    ("Python", "sequence_python.txt")
]

with open("results.txt", "w", encoding="utf-8") as f:
    f.write("Результаты тестирования\n")

    for lang, filename in files:
        try:
            seq = read_sequence(filename)

            f.write(f"{lang} ({filename}):\n{seq}\n\n")

            p, ones, zeros, s = frequency_test(seq)
            f.write("1. Частотный побитовый тест\n")
            f.write(f"   Единиц: {ones}, Нулей: {zeros}\n")
            f.write(f"   S_obs: {s:.4f}\n")
            f.write(f"   P-value: {p:.4f}\n")
            f.write(f"   Результат: {'Пройден' if p >= 0.01 else 'Не пройден'}\n\n")

            p, runs, expected, s = runs_test(seq)
            f.write("2. Тест на одинаковые подряд идущие биты\n")
            f.write(f"   Серий: {runs}, Ожидалось: {expected:.2f}\n")
            f.write(f"   S_obs: {s:.4f}\n")
            f.write(f"   P-value: {p:.4f}\n")
            f.write(f"   Результат: {'Пройден' if p >= 0.01 else 'Не пройден'}\n\n")

            p, v, chi = longest_run_test(seq)
            f.write("3. Тест на самую длинную последовательность единиц\n")
            f.write(f"   Распределение: <=1:{v[0]}, 2:{v[1]}, 3:{v[2]}, >=4:{v[3]}\n")
            f.write(f"   Хи-квадрат: {chi:.4f}\n")
            f.write(f"   P-value: {p:.4f}\n")
            f.write(f"   Результат: {'Пройден' if p >= 0.01 else 'Не пройден'}\n\n")

        except FileNotFoundError:
            f.write(f"Файл {filename} не найден\n\n")

print("Результаты сохранены в results.txt")