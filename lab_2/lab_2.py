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


def main():
    """Основная функция программы"""

    files = ["sequence_py.txt", "sequence_cpp.txt", "sequence_java.txt"]
    tests = [
        ("Частотный побитовый тест", freq_test),
        ("Тест на одинаковые подряд идущие биты", run_test),
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
