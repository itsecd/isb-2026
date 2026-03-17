import math
import sys
import os
from datetime import datetime
from scipy.special import gammaincc
import constants

def read_sequence(filename):
    """Читает последовательность битов из файла, возвращает список int"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            sequence = [int(bit) for bit in content if bit in ('0', '1')]
            if len(sequence) == 0:
                print(f"Ошибка: Файл {filename} не содержит битов 0/1")
                sys.exit(1)
            return sequence
    except FileNotFoundError:
        print(f"Ошибка: Файл {filename} не найден!")
        sys.exit(1)

def frequency_test(seq):
    """Частотный тест: проверяет соотношение 0 и 1"""
    n = len(seq)
    s_sum = sum(1 if bit == 1 else -1 for bit in seq)
    s_obs = abs(s_sum) / math.sqrt(n)
    return math.erfc(s_obs / math.sqrt(2))

def runs_test(seq):
    """Тест на подряд идущие биты: анализирует частоту смены битов"""
    n = len(seq)
    ones = sum(seq)
    pi = ones / n
     # Условие применимости теста
    if abs(pi - 0.5) >= 2.0 / math.sqrt(n):
        return 0.0
    # Подсчет количества знакоперемен
    runs = 1
    for i in range(n - 1):
        if seq[i] != seq[i + 1]:
            runs += 1
    
    numerator = abs(runs - 2 * n * pi * (1 - pi))
    denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)
    
    if denominator == 0:
        return 0.0
    
    return math.erfc(numerator / denominator)

def longest_run_test(seq):
    """Тест на самую длинную последовательность единиц в блоке"""
    n = len(seq)
    m = constants.BLOCK_SIZE_M
    k = n // m
    v = [0, 0, 0, 0] 
    # Анализ каждого блока
    for i in range(0, n, m):
        block = seq[i:i+m]
        max_run = 0
        curr = 0
        for bit in block:
            if bit == 1:
                curr += 1
                max_run = max(max_run, curr)
            else:
                curr = 0
        # Распределение по категориям
        if max_run <= 1: v[0] += 1
        elif max_run == 2: v[1] += 1
        elif max_run == 3: v[2] += 1
        else: v[3] += 1
    # Вычисление хи-квадрат
    chi_square = sum(((v[i] - k * constants.PI_VALUES[i]) ** 2) / 
                     (k * constants.PI_VALUES[i]) for i in range(4))
    # Вычисление P-value через неполную гамма-функцию
    p_value = gammaincc(3/2, chi_square/2)
    return p_value, chi_square

def main():
    # Получаем список файлов для анализа
    files = sys.argv[1:]
    if not files or files[0].lower() == 'all':
        files = [f for f in os.listdir('.') if f.startswith('sequence_') and f.endswith('.txt')]
        if not files:
            print("Файлы sequence_*.txt не найдены")
            return
    
    results_data = []
    print("\n" + "=" * 60)
    print("ТЕСТИРОВАНИЕ NIST")
    print("=" * 60)
    
    for filename in files:
        if not os.path.exists(filename):
            print(f"Файл {filename} не найден, пропускаем")
            continue
        
        # Читаем и анализируем последовательность
        seq = read_sequence(filename)
        n = len(seq)
        zeros, ones = seq.count(0), seq.count(1)
        
        p_freq = frequency_test(seq)
        p_runs = runs_test(seq)
        p_long, chi2 = longest_run_test(seq)
        
        status_freq = "ПРОЙДЕН" if p_freq >= constants.ALPHA else "НЕ ПРОЙДЕН"
        status_runs = "ПРОЙДЕН" if p_runs >= constants.ALPHA else "НЕ ПРОЙДЕН" if p_runs > 0 else "НЕ ПРИМЕНИМ"
        status_long = "ПРОЙДЕН" if p_long >= constants.ALPHA else "НЕ ПРОЙДЕН"
       
        print(f"\nФайл: {filename}")
        print(f"Длина: {n} | 0: {zeros} | 1: {ones}")
        print(f"  Частотный тест:    p={p_freq:.6f} - {status_freq}")
        print(f"  Тест на runs:      p={p_runs:.6f} - {status_runs}")
        print(f"  Тест longest run:  p={p_long:.6f} (χ²={chi2:.4f}) - {status_long}")
        
        # Сохраняем для общего файла
        results_data.append({
            'file': filename,
            'len': n,
            'zeros': zeros,
            'ones': ones,
            'p_freq': p_freq,
            'p_runs': p_runs,
            'p_long': p_long,
            'chi2': chi2,
            'status_freq': status_freq,
            'status_runs': status_runs,
            'status_long': status_long
        })

    with open("results.txt", 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ NIST\n")
        f.write(f"Уровень значимости: α = {constants.ALPHA}\n")
        f.write("=" * 70 + "\n\n")
        
        for data in results_data:
            f.write(f"Файл: {data['file']}\n")
            f.write(f"Длина: {data['len']} | 0: {data['zeros']} | 1: {data['ones']}\n")
            f.write(f"  Частотный тест:    p={data['p_freq']:.6f} - {data['status_freq']}\n")
            f.write(f"  Тест на runs:      p={data['p_runs']:.6f} - {data['status_runs']}\n")
            f.write(f"  Тест longest run:  p={data['p_long']:.6f} (χ²={data['chi2']:.4f}) - {data['status_long']}\n")
            f.write("=" * 70 + "\n")
            f.write("\n")
            
    print(f"\nРезультаты сохранены в файл: results.txt")
    print("Готово!")

if __name__ == "__main__":
    main()