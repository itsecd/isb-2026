import math
from scipy.special import erfc, gammaincc


def read_sequence(filename):
    """Чтение файла"""

    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{filename}' not found")


def freq_test(sequence):
    """Частотный побитовый тест"""

    n = len(sequence)

    s_n = 0
    for bit in sequence:
        if bit == "1":
            s_n += 1
        else:
            s_n -= 1

    s_obs = abs(s_n) / math.sqrt(n)
    p_value = erfc(s_obs / math.sqrt(2))

    return p_value


def run_test(sequence):
    """Тест на одинаковые подряд идущие биты"""

    n = len(sequence)
    pi = sequence.count("1") / n

    if abs(pi - 0.5) >= (2 / math.sqrt(n)):
        return 0.0

    v_n = 0
    for i in range(n - 1):
        if sequence[i] != sequence[i + 1]:
            v_n += 1

    p_value = erfc(
        abs(v_n - 2 * n * pi * (1 - pi)) / (2 * math.sqrt(2 * n) * pi * (1 - pi))
    )
    return p_value


def long_run_test(sequence):
    """Тест на самую длинную последовательность единиц в блоке"""

    n = len(sequence)
    m = 8
    num_blocks = n // m

    blocks = []
    for i in range(num_blocks):
        blocks.append(sequence[i * m : (i + 1) * m])

    v = [0, 0, 0, 0]

    for block in blocks:
        max_run = 0
        current_run = 0
        for bit in block:
            if bit == "1":
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 0

        if max_run <= 1:
            v[0] += 1
        elif max_run == 2:
            v[1] += 1
        elif max_run == 3:
            v[2] += 1
        else:
            v[3] += 1

    pi = [0.2148, 0.3672, 0.2305, 0.1875]

    chi_squared = 0
    for i in range(4):
        expected = num_blocks * pi[i]
        chi_squared += ((v[i] - expected) ** 2) / expected

    p_value = gammaincc(1.5, chi_squared / 2)

    return p_value


def main():
    """Основная функция программы"""

    files = ["sequence_py.txt", "sequence_cpp.txt", "sequence_java.txt"]
    tests = [
        ("Частотный побитовый тест", freq_test),
        ("Тест на одинаковые подряд идущие биты", run_test),
        ("Тест на самую длинную последовательность единиц", long_run_test),
    ]

    with open("results.txt", "w", encoding="utf-8") as f:
        for file in files:
            seq = read_sequence(file)
            print(f"\n=== {file} ===")
            f.write(f"\n=== {file} ===\n")

            for name, test in tests:
                p = test(seq)
                status = "СЛУЧАЙНАЯ" if p >= 0.01 else "НЕ СЛУЧАЙНАЯ"
                print(f"{name}: {p:.6f} -> {status}")
                f.write(f"{name}: {p:.6f} -> {status}\n")


if __name__ == "__main__":
    main()
