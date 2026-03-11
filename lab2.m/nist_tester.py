import math
import os

from scipy.special import gammaincc


def erfc(x):
    return math.erfc(x)


def frequency_test(seq):
    """Частотный побитовый тест. 
    Проверяет, примерно ли одинаковое количество нулей и единиц в последовательности."""
    n = len(seq)
    sum_bits = 0
    for bit in seq:
        sum_bits += 1 if bit == '1' else -1
    
    s_obs = abs(sum_bits) / math.sqrt(n)
    return erfc(s_obs / math.sqrt(2))


def runs_test(seq):
    """Тест на одинаковые подряд идущие биты.
    Проверяет, соответствует ли частота смены битов случайной последовательности."""
    n = len(seq)
    
    ones = seq.count('1')
    pi = ones / n
    
    if abs(pi - 0.5) > (2 / math.sqrt(n)):
        return 0.0
    
    v = sum(1 for i in range(n - 1) if seq[i] != seq[i + 1])
    
    numerator = abs(v - 2 * n * pi * (1 - pi))
    denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)
    
    return erfc(numerator / denominator) if denominator != 0 else 0.0


def longest_run_test(seq):
    """Тест на самую длинную последовательность единиц в блоке.
    Разбивает последовательность на блоки по 8 бит и анализирует
    максимальные длины последовательностей единиц в каждом блоке"""
    n = len(seq)
    m = 8
    blocks_count = n // m
    
    v = [0, 0, 0, 0]
    
    for i in range(blocks_count):
        block = seq[i*m : (i+1)*m]
        
        max_run = 0
        current = 0
        for bit in block:
            if bit == '1':
                current += 1
                max_run = max(max_run, current)
            else:
                current = 0
        
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
        expected = blocks_count * pi[i]
        chi2 += ((v[i] - expected) ** 2) / expected
    
    from scipy.special import gammaincc
    p_value = gammaincc(1.5, chi2 / 2.0)
    
    return p_value


def read_sequence(filename):
    """Чтение последовательности из файла."""
    try:
        with open(filename, 'r') as f:
            seq = f.read().strip()
        
        if len(seq) != 128 or not all(c in '01' for c in seq):
            return None
        return seq
    except:
        return None


def main():
    """Основная функция."""
    
    files = [
        "sequences/sequence_java.txt",
        "sequences/sequence_python.txt", 
        "sequences/sequence_cpp.txt"
    ]
    languages = ["Java", "Python", "C++"]
    
    results = []
    
    for filename, lang in zip(files, languages):
        seq = read_sequence(filename)
        
        if seq is None:
            results.append([lang, "ОШИБКА", "-", "-", "-"])
            continue
        
        p1 = frequency_test(seq)
        p2 = runs_test(seq)
        p3 = longest_run_test(seq)
        
        if None in [p1, p2, p3]:
            results.append([lang, "ОШИБКА", "-", "-", "-"])
            continue
        
        status1 = "ПРОЙДЕН" if p1 >= 0.01 else "НЕ ПРОЙДЕН"
        status2 = "ПРОЙДЕН" if p2 >= 0.01 else "НЕ ПРОЙДЕН"
        status3 = "ПРОЙДЕН" if p3 >= 0.01 else "НЕ ПРОЙДЕН"
        
        results.append([lang, status1, status2, status3])
    
    try:
        with open("test_results.txt", "w") as f:
            f.write("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ NIST\n")
            f.write("=" * 50 + "\n")
            f.write(f"{'Язык':<10} {'Тест 1':<10} {'Тест 2':<10} {'Тест 3':<10}\n")
            f.write("-" * 50 + "\n")
            for r in results:
                f.write(f"{r[0]:<10} {r[1]:<10} {r[2]:<10} {r[3]:<10}\n")
        
        print("Тестирование завершено. Результаты в test_results.txt")
    except:
        print("Ошибка при сохранении")


if __name__ == "__main__":
    main()