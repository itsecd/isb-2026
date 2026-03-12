import random
import math

N = 128


# генерация последовательности


def generate_sequence():
    return [random.randint(0, 1) for _ in range(N)]


# 1. Частотный побитовый тест


def frequency_test(seq):

    x = [1 if bit == 1 else -1 for bit in seq]

    S = sum(x)

    Sn = abs(S) / math.sqrt(N)

    p_value = math.erfc(Sn / math.sqrt(2))

    return p_value


# 2. Тест на одинаковые подряд идущие биты


def runs_test(seq):

    ones = sum(seq)

    zeta = ones / N

    if abs(zeta - 0.5) >= (2 / math.sqrt(N)):
        return 0

    V = 1

    for i in range(N - 1):
        if seq[i] != seq[i + 1]:
            V += 1

    p_value = math.erfc(
        abs(V - 2 * N * zeta * (1 - zeta)) / (2 * math.sqrt(2 * N) * zeta * (1 - zeta))
    )

    return p_value


# 3. Самая длинная последовательность единиц в блоке


def longest_run_test(seq):

    M = 8

    blocks = [seq[i : i + M] for i in range(0, N, M)]

    v = [0, 0, 0, 0]

    for block in blocks:
        max_run = 0
        run = 0

        for bit in block:
            if bit == 1:
                run += 1
                max_run = max(max_run, run)
            else:
                run = 0

        if max_run <= 1:
            v[0] += 1
        elif max_run == 2:
            v[1] += 1
        elif max_run == 3:
            v[2] += 1
        else:
            v[3] += 1

    pi = [0.2148, 0.3672, 0.2305, 0.1875]

    chi2 = 0

    for i in range(4):
        chi2 += ((v[i] - 16 * pi[i]) ** 2) / (16 * pi[i])

    p_value = math.exp(-chi2 / 2)

    return p_value


# основная программа


seq = generate_sequence()

sequence_str = "".join(map(str, seq))

# сохраняем последовательность
with open("sequence.txt", "w") as f:
    f.write(sequence_str)


p1 = frequency_test(seq)
p2 = runs_test(seq)
p3 = longest_run_test(seq)


# результаты
result_text = f"""
Сгенерированная последовательность:
{sequence_str}

Frequency Test P-value = {p1}
Runs Test P-value = {p2}
Longest Run Test P-value = {p3}

Результаты тестов:

Frequency Test: {"PASS" if p1 >= 0.01 else "FAIL"}
Runs Test: {"PASS" if p2 >= 0.01 else "FAIL"}
Longest Run Test: {"PASS" if p3 >= 0.01 else "FAIL"}
"""


# сохраняем результаты
with open("results.txt", "w") as f:
    f.write(result_text)


print(result_text)
