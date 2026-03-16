import math
import os
from scipy.special import gammaincc


def read_sequence(filename):
    try:
        # Показываем, какой файл ищем и где мы находимся
        print(f"Пытаюсь открыть файл: {filename}")
        print(f"Текущая директория: {os.getcwd()}")
        print(f"Файл существует: {os.path.exists(filename)}")

        with open(filename, 'r') as f:
            content = f.read().strip()
            print(f"Содержимое файла (первые 50 символов): {content[:50]}")
            bits = [int(c) for c in content if c in '01']
            print(f"Прочитано бит: {len(bits)}")
            return bits
    except Exception as e:
        print(f"ОШИБКА: {e}")
        return []


def frequency_test(bits):
    n = len(bits)
    s = sum(1 if b else -1 for b in bits)
    return math.erfc(abs(s) / math.sqrt(2 * n))


def runs_test(bits):
    n = len(bits)
    pi = sum(bits) / n

    if abs(pi - 0.5) >= 2 / math.sqrt(n):
        return 0.0

    v = 1
    for i in range(n - 1):
        if bits[i] != bits[i + 1]:
            v += 1

    return math.erfc(abs(v - 2 * n * pi * (1 - pi)) / (2 * math.sqrt(2 * n) * pi * (1 - pi)))


def longest_run_test(bits):
    n = len(bits)
    if n < 128:
        return 0.0

    M = 8
    N = n // M
    v = [0, 0, 0, 0]
    pi = [0.2148, 0.3672, 0.2305, 0.1875]

    for i in range(N):
        block = bits[i * M:(i + 1) * M]
        curr = max_run = 0
        for b in block:
            curr = curr + 1 if b else 0
            max_run = max(max_run, curr)

        if max_run <= 1:
            v[0] += 1
        elif max_run == 2:
            v[1] += 1
        elif max_run == 3:
            v[2] += 1
        else:
            v[3] += 1

    chi2 = sum((v[i] - N * pi[i]) ** 2 / (N * pi[i]) for i in range(4))
    return gammaincc(3 / 2, chi2 / 2)


def main():
    print("=" * 50)
    print("НАЧАЛО РАБОТЫ ПРОГРАММЫ")
    print("=" * 50)

    # Проверяем все возможные пути
    files = [
        ("C++", "C++.txt"),
        ("Java", "java.txt"),
        ("Python", "python.txt")
    ]

    # Также проверим альтернативные пути
    alt_files = [
        ("C++ (generator/)", "generator/C++.txt"),
        ("Java (generator/)", "generator/java.txt"),
        ("Python (generator/)", "generator/python.txt"),
    ]

    with open("results.txt", "w", encoding="utf-8") as f:
        f.write("| Language    | Frequency | Runs      | LongRun   | Result |\n")
        f.write("|-------------|-----------|-----------|-----------|--------|\n")

        for lang, fname in files:
            print(f"\n--- Обработка: {lang} ---")
            bits = read_sequence(fname)

            if bits and len(bits) > 0:
                if len(bits) >= 128:
                    freq = frequency_test(bits)
                    runs = runs_test(bits)
                    longrun = longest_run_test(bits)
                    status = "PASSED" if all(p >= 0.01 for p in [freq, runs, longrun]) else "FAILED"
                    f.write(f"| {lang:<11} | {freq:.7f} | {runs:.7f} | {longrun:.7f} | {status:<6} |\n")
                    print(f"  РЕЗУЛЬТАТ: {status}")
                else:
                    print(f"  ОШИБКА: недостаточно бит (нужно 128, есть {len(bits)})")
                    f.write(f"| {lang:<11} | {'ERROR':<9} | {'ERROR':<9} | {'ERROR':<9} | {'ERROR':<6} |\n")
            else:
                print(f"  ОШИБКА: не удалось прочитать биты")
                f.write(f"| {lang:<11} | {'ERROR':<9} | {'ERROR':<9} | {'ERROR':<9} | {'ERROR':<6} |\n")

    print("\n" + "=" * 50)
    print("ПРОВЕРКА АЛЬТЕРНАТИВНЫХ ПУТЕЙ:")
    print("=" * 50)

    for lang, fname in alt_files:
        print(f"\n{lang}: {fname}")
        print(f"  Существует: {os.path.exists(fname)}")

    print("\n" + "=" * 50)
    print("РЕЗУЛЬТАТЫ (results.txt):")
    print("=" * 50)

    with open("results.txt", "r", encoding="utf-8") as f:
        print(f.read())


if __name__ == "__main__":
    main()