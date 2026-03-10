import math
from scipy.special import gammaincc

def read_file(name):
    """
    Читает содержимое файла и возвращает строку без пробельных символов по краям.
    
    Аргументы:
        name (str): Имя файла для чтения.
    
    Возвращает:
        str: Содержимое файла с удалёнными начальными и конечными пробелами.
    """
    with open(name) as f:
        return f.read().strip()

def test1(seq):
    """
    Частотный тест (Monobit Test) из набора NIST.
    Проверяет, близка ли доля единиц к 0.5.
    
    Аргументы:
        seq (str): Бинарная последовательность из символов '0' и '1'.
    
    Возвращает:
        tuple: (p_value, результат), где p_value — вероятность, результат — "ПРОЙДЕН" или "НЕ ПРОЙДЕН".
    """
    n = len(seq)
    s = sum(2 * int(b) - 1 for b in seq)
    p = math.erfc(abs(s) / math.sqrt(2 * n))
    return p, "ПРОЙДЕН" if p >= 0.01 else "НЕ ПРОЙДЕН"

def test2(seq):
    """
    Тест на серии (Runs Test) из набора NIST.
    Проверяет, соответствует ли количество серий из единиц и нулей случайной последовательности.
    
    Аргументы:
        seq (str): Бинарная последовательность из символов '0' и '1'.
    
    Возвращает:
        tuple: (p_value, результат), где p_value — вероятность, результат — "ПРОЙДЕН", "НЕ ПРОЙДЕН" или "НЕ ПРИМЕНИМ".
    """
    n = len(seq)
    ones = seq.count('1')
    if abs(ones / n - 0.5) > 2 / math.sqrt(n):
        return 0, "НЕ ПРИМЕНИМ"
    
    runs = 1
    for i in range(1, n):
        if seq[i] != seq[i - 1]:
            runs += 1
    
    exp = 2 * ones * (n - ones) / n + 1
    var = (exp - 1) * (exp - 2) / (n - 1)
    p = math.erfc(abs(runs - exp) / math.sqrt(2 * var))
    return p, "ПРОЙДЕН" if p >= 0.01 else "НЕ ПРОЙДЕН"

def test3(seq):
    """
    Тест на серию единиц в блоке (Test for the Longest Run of Ones in a Block) из набора NIST.
    Проверяет распределение максимальных длин серий единиц в блоках фиксированной длины.
    
    Аргументы:
        seq (str): Бинарная последовательность из символов '0' и '1'.
    
    Возвращает:
        tuple: (p_value, результат), где p_value — вероятность, результат — "ПРОЙДЕН" или "НЕ ПРОЙДЕН".
    """
    n, M = len(seq), 8
    blocks = [seq[i:i + M] for i in range(0, n, M)]
    v = [0, 0, 0, 0]
    
    for b in blocks:
        maxrun = 0
        cur = 0
        for bit in b:
            if bit == '1':
                cur += 1
                maxrun = max(maxrun, cur)
            else:
                cur = 0
        if maxrun <= 1:
            v[0] += 1
        elif maxrun == 2:
            v[1] += 1
        elif maxrun == 3:
            v[2] += 1
        else:
            v[3] += 1
    
    pi = [0.2148, 0.3672, 0.2305, 0.1875]
    chi = sum((v[i] - 16 * pi[i]) ** 2 / (16 * pi[i]) for i in range(4))
    p = gammaincc(1.5, chi / 2)
    return p, "ПРОЙДЕН" if p >= 0.01 else "НЕ ПРОЙДЕН"


files = ["seq_cpp.txt", "seq_java.txt", "seq_python.txt"]

print("\n" + "=" * 50)
print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
print("=" * 50)

for f in files:
    try:
        seq = read_file(f)
        print(f"\nФайл: {f}")
        print(f"Длина: {len(seq)} бит")
        print(f"Последовательность: {seq[:32]}...")

        p1, r1 = test1(seq)
        p2, r2 = test2(seq)
        p3, r3 = test3(seq)

        print(f"1. Частотный тест: p={p1:.4f} - {r1}")
        print(f"2. Тест на серии:  p={p2:.4f} - {r2}")
        print(f"3. Длинные серии:  p={p3:.4f} - {r3}")

    except FileNotFoundError:
        print(f"\nФайл {f} не найден")