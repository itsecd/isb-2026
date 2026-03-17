"""
Программа для статистического анализа псевдослучайных последовательностей
Реализует три теста NIST:
1. Частотный побитовый тест (Frequency Test)
2. Тест на одинаковые подряд идущие биты (Runs Test)
3. Тест на самую длинную последовательность единиц в блоке (Longest Run Test)

Автор: Студент
Дата: 2026
"""

import math
import sys
import os
from datetime import datetime
from scipy.special import gammaincc
import constants


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
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            # Извлекаем только символы 0 и 1
            sequence = [int(bit) for bit in content if bit in ('0', '1')]
            
            if len(sequence) == 0:
                print(f"Ошибка: Файл {filename} не содержит битовых символов (0 или 1)")
                sys.exit(1)
                
            return sequence
    except FileNotFoundError:
        print(f"Ошибка: Файл {filename} не найден!")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при чтении файла {filename}: {e}")
        sys.exit(1)


def frequency_test(seq):
    """
    Частотный побитовый тест (Frequency Test).
    
    Проверяет, близка ли доля единиц и нулей к 0.5.
    Преобразует 0->-1, 1->1, вычисляет сумму и нормализует.
    
    Args:
        seq (list): Последовательность битов (0 и 1)
        
    Returns:
        float: P-значение теста
    """
    n = len(seq)
    
    # Преобразуем 0 в -1, 1 в 1
    s_sum = 0
    for bit in seq:
        s_sum += 1 if bit == 1 else -1
    
    # Вычисляем статистику теста
    s_obs = abs(s_sum) / math.sqrt(n)
    
    # Вычисляем P-value через дополнительную функцию ошибок
    p_value = math.erfc(s_obs / math.sqrt(2))
    
    return p_value


def runs_test(seq):
    """
    Тест на одинаковые подряд идущие биты (Runs Test).
    
    Проверяет, соответствует ли количество смен битов (01 или 10)
    случайной последовательности.
    
    Args:
        seq (list): Последовательность битов (0 и 1)
        
    Returns:
        float: P-значение теста (0.0 если тест не применим)
    """
    n = len(seq)
    
    # Вычисляем долю единиц
    ones = sum(seq)
    pi = ones / n
    # Проверяем условие применимости теста
    if abs(pi - 0.5) >= 2.0 / math.sqrt(n):
        return 0.0
    # Вычисляем количество знакоперемен
    runs = 1
    for i in range(n - 1):
        if seq[i] != seq[i + 1]:
            runs += 1
    # Вычисляем P-value по правильной формуле из документации NIST
    numerator = abs(runs - 2 * n * pi * (1 - pi))
    denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)
    
    if denominator == 0:
        return 0.0
    
    # Вычисляем P-value
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
        tuple: (P-значение, статистика хи-квадрат)
    """
    n = len(seq)
    m = constants.BLOCK_SIZE_M
    k = n // m  # количество блоков
    
    # Теоретические вероятности
    pi_vals = constants.PI_VALUES
    
    # Инициализация счетчиков v
    v = [0, 0, 0, 0]
    
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
        else:
            v[3] += 1
    
    chi_square = 0
    for i in range(4):
        expected = k * pi_vals[i]
        chi_square += ((v[i] - expected) ** 2) / expected
    
    # Вычисление P-value через неполную гамма-функцию
    p_value = gammaincc(3/2, chi_square/2)
    
    return p_value, chi_square


def analyze_sequence(filename):
    """
    Анализирует последовательность из файла с помощью всех трёх тестов.
    
    Args:
        filename (str): Имя файла с последовательностью
        
    Returns:
        tuple: (имя_файла, длина, результаты_тестов)
    """
    print(f"\nАнализ файла: {filename}")
    print("-" * 50)
    
    # Читаем последовательность
    seq = read_sequence(filename)
    n = len(seq)
    
    # Статистика последовательности
    zeros = seq.count(0)
    ones = seq.count(1)
    print(f"Длина: {n} бит")
    print(f"0: {zeros}, 1: {ones}")
    print(f"Соотношение 0/1: {zeros/ones:.2f}" if ones > 0 else "Соотношение: только нули")
    
    # Предупреждение о длине
    if n != constants.SEQUENCE_LENGTH:
        print(f"Предупреждение: Ожидалась длина {constants.SEQUENCE_LENGTH} бит, получено {n} бит.")
    
    # Запускаем тесты
    p1 = frequency_test(seq)
    p2 = runs_test(seq)
    p3, chi2 = longest_run_test(seq)
    
    # Формируем результаты
    results = [
        ("Частотный побитовый тест", p1),
        ("Тест на подряд идущие биты", p2),
        ("Тест на самую длинную последовательность", p3, chi2)
    ]
    
    # Вывод на экран
    for i, result in enumerate(results):
        if i < 2:
            test_name, p_value = result
            status = "ПРОЙДЕН" if p_value >= constants.ALPHA else "НЕ ПРОЙДЕН"
            if p_value == 0.0 and test_name == "Тест на подряд идущие биты":
                status = "НЕ ПРИМЕНИМ"
            print(f"\n{test_name}:")
            print(f"  P-value = {p_value:.6f}")
            print(f"  Статус: {status}")
        else:
            test_name, p_value, chi2_val = result
            status = "ПРОЙДЕН" if p_value >= constants.ALPHA else "НЕ ПРОЙДЕН"
            print(f"\n{test_name}:")
            print(f"  Хи-квадрат = {chi2_val:.4f}")
            print(f"  P-value = {p_value:.6f}")
            print(f"  Статус: {status}")
    
    print()
    
    return filename, n, zeros, ones, results


def save_results_to_file(results, output_filename):
    """
    Сохраняет результаты тестирования в файл.
    
    Args:
        results: Кортеж с результатами анализа
        output_filename (str): Имя файла для сохранения
    """
    filename, n, zeros, ones, test_results = results
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ NIST\n")
        f.write("=" * 70 + "\n\n")
        
        # Метаданные
        f.write(f"Анализируемый файл: {filename}\n")
        f.write(f"Дата и время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Длина последовательности: {n} бит\n")
        f.write(f"Количество нулей: {zeros}\n")
        f.write(f"Количество единиц: {ones}\n")
        f.write(f"Соотношение 0/1: {zeros/ones:.2f}\n\n" if ones > 0 else "Соотношение: только нули\n\n")
        
        f.write("-" * 70 + "\n")
        f.write(f"{'Тест':<40} {'P-value':<12} {'Результат':<10}\n")
        f.write("-" * 70 + "\n")
        
        for i, result in enumerate(test_results):
            if i < 2:
                test_name, p_value = result
                status = "ПРОЙДЕН" if p_value >= constants.ALPHA else "НЕ ПРОЙДЕН"
                if p_value == 0.0 and test_name == "Тест на подряд идущие биты":
                    status = "НЕ ПРИМЕНИМ"
                f.write(f"{test_name:<40} {p_value:<12.6f} {status:<10}\n")
            else:
                test_name, p_value, chi2_val = result
                status = "ПРОЙДЕН" if p_value >= constants.ALPHA else "НЕ ПРОЙДЕН"
                f.write(f"{test_name:<40} {p_value:<12.6f} {status:<10}\n")
                f.write(f"  (Хи-квадрат = {chi2_val:.4f})\n")
        
        f.write("=" * 70 + "\n\n")
        f.write(f"Примечание: Последовательность считается случайной,\n")
        f.write(f"если P-value >= {constants.ALPHA} (уровень значимости {constants.ALPHA*100}%)\n")


def print_usage():
    """Выводит информацию об использовании программы"""
    print("\n" + "=" * 60)
    print("ИНСТРУКЦИЯ ПО ИСПОЛЬЗОВАНИЮ")
    print("=" * 60)
    print("\n1. Тестирование одного файла:")
    print("   python test.py sequence_cpp.txt")
    print("\n2. Тестирование нескольких файлов:")
    print("   python test.py sequence_cpp.txt sequence_java.txt sequence_py.txt")
    print("\n3. Тестирование всех файлов sequence_*.txt в папке:")
    print("   python test.py all")
    print("\n4. Интерактивный режим (без аргументов):")
    print("   python test.py")
    print("\n" + "=" * 60)


def main():
    """
    Основная функция программы.
    """
    # Интерактивный режим (без аргументов)
    if len(sys.argv) == 1:
        print_usage()
        print("\n" + "=" * 60)
        print("ИНТЕРАКТИВНЫЙ РЕЖИМ")
        print("=" * 60)
        
        # Ищем все файлы sequence_.txt в папке
        sequence_files = []
        for file in os.listdir('.'):
            if file.startswith('sequence_') and file.endswith('.txt'):
                sequence_files.append(file)
        
        if sequence_files:
            print("\nНайдены файлы последовательностей:")
            for i, file in enumerate(sequence_files, 1):
                print(f"  {i}. {file}")
            
            choice = input("\nВведите номера файлов через пробел (или 'all' для всех): ").strip()
            
            if choice.lower() == 'all':
                files_to_analyze = sequence_files
            else:
                try:
                    indices = [int(x) for x in choice.split()]
                    files_to_analyze = [sequence_files[i-1] for i in indices if 1 <= i <= len(sequence_files)]
                except:
                    print("Некорректный ввод. Завершение.")
                    return
        else:
            print("\nФайлы sequence_*.txt не найдены в текущей директории.")
            files_to_analyze = []
    
    # Режим "all" - тестировать все файлы sequence_*.txt
    elif len(sys.argv) == 2 and sys.argv[1].lower() == 'all':
        files_to_analyze = []
        for file in os.listdir('.'):
            if file.startswith('sequence_') and file.endswith('.txt'):
                files_to_analyze.append(file)
        
        if not files_to_analyze:
            print("Файлы sequence_*.txt не найдены в текущей директории.")
            return
    
    # Режим с указанными файлами
    else:
        files_to_analyze = sys.argv[1:]
    
    # Проверяем, есть ли что анализировать
    if not files_to_analyze:
        print("Нет файлов для анализа.")
        return
    
    print(f"\nБудут проанализированы файлы: {', '.join(files_to_analyze)}")
    
    all_results = []
    
    for filename in files_to_analyze:
        if not os.path.exists(filename):
            print(f"Предупреждение: Файл {filename} не существует, пропускаем.")
            continue
        
        results = analyze_sequence(filename)
        all_results.append(results)
        
        # Сохраняем результаты в отдельный файл
        base_name = os.path.splitext(filename)[0]
        output_filename = f"results_{base_name}.txt"
        save_results_to_file(results, output_filename)
        print(f"Результаты сохранены в файл: {output_filename}")
    
    # Если анализировали несколько файлов, создаём сводный отчёт
    if len(all_results) > 1:
        summary_filename = "results_summary.txt"
        with open(summary_filename, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("СВОДНЫЙ ОТЧЁТ ПО ТЕСТИРОВАНИЮ NIST\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Проанализировано файлов: {len(all_results)}\n\n")
            
            f.write("-" * 80 + "\n")
            header = f"{'Файл':<20} {'Длина':<8} {'0/1':<12} {'Частотный':<10} {'Runs':<10} {'Longest Run':<12}\n"
            f.write(header)
            f.write("-" * 80 + "\n")
            
            for res in all_results:
                filename, n, zeros, ones, test_res = res
                short_name = os.path.basename(filename)[:20]
                
                p_freq = test_res[0][1]
                p_runs = test_res[1][1]
                p_long = test_res[2][1]
                
                status_freq = "✓" if p_freq >= constants.ALPHA else "✗"
                status_runs = "✓" if p_runs >= constants.ALPHA else "✗"
                status_long = "✓" if p_long >= constants.ALPHA else "✗"
                
                f.write(f"{short_name:<20} {n:<8} {zeros}/{ones:<11} ")
                f.write(f"{p_freq:.3f}/{status_freq:<6} {p_runs:.3f}/{status_runs:<6} {p_long:.3f}/{status_long}\n")
            
            f.write("=" * 80 + "\n")
        
        print(f"\nСводный отчёт сохранён в файл: {summary_filename}")
    
    print("\nТестирование завершено!")


if __name__ == "__main__":
    main()
