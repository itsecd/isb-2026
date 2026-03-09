#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Программа для статистического анализа псевдослучайных последовательностей
Реализует три теста NIST:
1. Частотный побитовый тест
2. Тест на одинаковые подряд идущие биты
3. Тест на самую длинную последовательность единиц в блоке

Автор: Студент 2 курса
Дата: 2024
"""

import math
import sys
from scipy.special import gammaincc

def read_sequence(filename):
    """
    Читает последовательность битов из файла.
    
    Args:
        filename (str): Имя файла с последовательностью битов
        
    Returns:
        list: Список целых чисел 0 и 1
        
    Raises:
        FileNotFoundError: Если файл не найден
    """
    try:
        with open(filename, 'r') as f:
            line = f.read().strip()
        return [int(bit) for bit in line if bit in ('0', '1')]
    except FileNotFoundError:
        print(f"Ошибка: Файл {filename} не найден!")
        sys.exit(1)

def frequency_test(seq):
    """
    Частотный побитовый тест (Frequency Test).
    
    Проверяет, близка ли доля единиц и нулей к 0.5.
    Преобразует 0->-1, 1->1, вычисляет сумму и нормализует.
    
    Args:
        seq (list): Последовательность битов (0 и 1)
        
    Returns:
        float: P-значение теста (>= 0.01 - последовательность случайна)
    """
    n = len(seq)
    # Преобразуем 0 в -1, 1 в 1
    x = [1 if bit == 1 else -1 for bit in seq]
    s = sum(x)
    s_obs = abs(s) / math.sqrt(n)
    p_value = math.erfc(s_obs / math.sqrt(2))
    return p_value

def runs_test(seq):
    """
    Тест на одинаковые подряд идущие биты (Runs Test).
    
    Проверяет, соответствует ли количество смен битов (01 или 10)
    случайной последовательности. Сначала проверяется условие 
    |pi - 0.5| < 2/sqrt(N), иначе тест не применим.
    
    Args:
        seq (list): Последовательность битов (0 и 1)
        
    Returns:
        float: P-значение теста (0.0 если тест не применим)
    """
    n = len(seq)
    pi = sum(seq) / n  # доля единиц
    tau = 2 / math.sqrt(n)
    
    # Проверяем условие применимости теста
    if abs(pi - 0.5) >= tau:
        return 0.0
    
    # Вычисляем число знакоперемен
    v = 1
    for i in range(n-1):
        if seq[i] != seq[i+1]:
            v += 1
    
    numerator = abs(v - 2 * n * pi * (1 - pi))
    denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)
    
    # Избегаем деления на ноль
    if denominator == 0:
        return 0.0
        
    p_value = math.erfc(numerator / denominator)
    return p_value

def longest_run_test(seq):
    """
    Тест на самую длинную последовательность единиц в блоке.
    
    Разбивает последовательность на блоки по 8 бит, в каждом ищет
    максимальную длину непрерывных единиц. Сравнивает распределение
    этих длин с теоретическим с помощью критерия хи-квадрат.
    
    Args:
        seq (list): Последовательность битов (0 и 1)
        
    Returns:
        float: P-значение теста
    """
    n = len(seq)
    m = 8  # длина блока
    k = n // m  # количество блоков (для N=128, k=16)
    
    # Теоретические вероятности для M=8
    pi_vals = [0.2148, 0.3672, 0.2305, 0.1875]
    
    # Инициализация счетчиков v
    v = [0, 0, 0, 0]  # v0, v1, v2, v3
    
    # Анализ каждого блока
    for i in range(0, n, m):
        block = seq[i:i+m]
        max_run = 0
        current_run = 0
        
        for bit in block:
            if bit == 1:
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 0
        
        # Распределение по категориям
        if max_run <= 1:
            v[0] += 1
        elif max_run == 2:
            v[1] += 1
        elif max_run == 3:
            v[2] += 1
        else:  # >=4
            v[3] += 1
    
    # Вычисление хи-квадрат
    chi2 = 0
    for i in range(4):
        expected = k * pi_vals[i]
        chi2 += ((v[i] - expected) ** 2) / expected
    
    # Вычисление P-value через неполную гамма-функцию
    p_value = gammaincc(3/2, chi2/2)  # igamc(3/2, chi2/2)
    return p_value

def save_results(filename, results):
    """
    Сохраняет результаты тестирования в файл.
    
    Args:
        filename (str): Имя файла для сохранения
        results (list): Список кортежей (название_теста, p_value, статус)
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ NIST\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"Анализируемый файл: {results[0][0]}\n")
        f.write(f"Дата и время: {results[0][1]}\n")
        f.write(f"Длина последовательности: {results[0][2]} бит\n\n")
        
        f.write("-" * 60 + "\n")
        f.write(f"{'Тест':<40} {'P-value':<12} {'Результат':<10}\n")
        f.write("-" * 60 + "\n")
        
        for i in range(1, len(results)):
            test_name, p_value, status = results[i]
            f.write(f"{test_name:<40} {p_value:<12.5f} {status:<10}\n")
        
        f.write("=" * 60 + "\n\n")
        f.write("Примечание: Последовательность считается случайной,\n")
        f.write("если P-value >= 0.01 (уровень значимости 1%)\n")

def main():
    """
    Основная функция программы.
    
    Читает последовательность из файла, запускает все три теста
    и выводит результаты на экран и в файл.
    """
    if len(sys.argv) != 2:
        print("Использование: python nist_tests.py <filename>")
        print("Пример: python nist_tests.py sequence_cpp.txt")
        return
    
    filename = sys.argv[1]
    seq = read_sequence(filename)
    
    if len(seq) != 128:
        print(f"Предупреждение: Ожидалась длина 128 бит, получено {len(seq)} бит.")
        print("Тесты могут работать некорректно.")
    
    # Запускаем тесты
    print(f"\nАнализ файла: {filename}")
    print("-" * 50)
    
    p1 = frequency_test(seq)
    p2 = runs_test(seq)
    p3 = longest_run_test(seq)
    
    # Формируем результаты для экрана
    tests = [
        ("Частотный побитовый тест", p1),
        ("Тест на подряд идущие биты", p2),
        ("Тест на самую длинную последовательность", p3)
    ]
    
    # Вывод на экран
    for test_name, p_value in tests:
        status = "ПРОЙДЕН" if p_value >= 0.01 else "НЕ ПРОЙДЕН"
        if p_value == 0.0 and test_name == "Тест на подряд идущие биты":
            status = "НЕ ПРИМЕНИМ"
        print(f"{test_name}:")
        print(f"  P-value = {p_value:.6f}")
        print(f"  Статус: {status}\n")
    
    # Сохраняем в файл
    from datetime import datetime
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    results_for_file = [
        (filename, now, len(seq)),  # метаданные
        ("Частотный побитовый тест", p1, "ПРОЙДЕН" if p1 >= 0.01 else "НЕ ПРОЙДЕН"),
        ("Тест на подряд идущие биты", p2, "ПРОЙДЕН" if p2 >= 0.01 else ("НЕ ПРИМЕНИМ" if p2 == 0.0 else "НЕ ПРОЙДЕН")),
        ("Тест на самую длинную последовательность", p3, "ПРОЙДЕН" if p3 >= 0.01 else "НЕ ПРОЙДЕН")
    ]
    
    output_filename = f"results_{filename.split('.')[0]}.txt"
    save_results(output_filename, results_for_file)
    print(f"Результаты сохранены в файл: {output_filename}")

if __name__ == "__main__":
    main()