'''2.1. Частотный побитовый тест.
2.2. Тест на одинаковые подряд идущие биты.
2.3. Тест на самую длинную последовательность единиц в блоке.'''

import math
from scipy.special import gammaincc

from consts_lab2 import (
    CPP_RESULTS,
    PYTHON_RESULTS,
    JAVA_RESULTS
    )
    
def frequency_test(bit_sequence):
    """
    Частотный побитовый тест
    """
    sequence_length = len(bit_sequence)
    
    if sequence_length == 0:
        return 0.0
    
    ones_count = bit_sequence.count("1")
    zeros_count = bit_sequence.count("0")

    deviation = abs(ones_count - zeros_count)
    s_statistic = deviation / math.sqrt(sequence_length)

    p_value = math.erfc(s_statistic / math.sqrt(2))
    return p_value

def bit_test(bit_sequence):
    """
    Тест на одинаковые подряд идущие биты
    """
    sequence_length = len(bit_sequence)
    
    ones_probability = bit_sequence.count("1") / sequence_length

    if abs(ones_probability - 0.5) >= (2 / math.sqrt(sequence_length)):
        return 0.0
    
    transitions_count = 0
    for i in range(sequence_length - 1):
        if bit_sequence[i] != bit_sequence[i + 1]:
            transitions_count += 1

    numerator = abs(transitions_count - 2 * sequence_length * ones_probability * (1 - ones_probability))
    denominator = 2 * math.sqrt(2 * sequence_length) * ones_probability * (1 - ones_probability)
    
    p_value = math.erfc(numerator / denominator)
    return p_value

def count_max_runs(bit_sequence):
    """
    Подсчитывает распределение по максимальной длине единиц
    """
    block_size = 8

    runs_distribution = {1: 0, 2: 0, 3: 0, 4: 0}

    for i in range(0, 128, block_size):
        block = bit_sequence[i:i + block_size]

        max_run_length = 0
        current_run_length = 0

        for bit in block:
            if bit == "1":
                current_run_length += 1
                if current_run_length > max_run_length:
                    max_run_length = current_run_length
            else:
                current_run_length = 0

        if max_run_length <= 1:
            runs_distribution[1] += 1
        elif max_run_length == 2:
            runs_distribution[2] += 1
        elif max_run_length == 3:
            runs_distribution[3] += 1
        elif max_run_length >= 4:
            runs_distribution[4] += 1
    
    return runs_distribution

def calculate_chi_square(runs_counts):
    """
    Вычисляет статистику хи-квадрат для распределения серий
    """
    expected_probabilities = {1: 0.2148, 2: 0.3672, 3: 0.2305, 4: 0.1875}
    chi_square_stat = 0.0
    
    for category in range(1, 5):
        expected_count = 16 * expected_probabilities[category]
        chi_square_stat += ((runs_counts[category] - expected_count) ** 2) / expected_count

    return chi_square_stat

def len_one_test(filename):
    """
    Тест на самую длинную последовательность единиц в блоке
    """
    runs_counts = count_max_runs(filename)
    chi_square_stat = calculate_chi_square(runs_counts)

    p_value = gammaincc(3 / 2.0, chi_square_stat / 2.0)
    return p_value

def main():

    print("Тесты:\n")
    
    print("C++:\n")
    print(f"Частотный побитовый тест: {frequency_test(CPP_RESULTS)}\n")
    print(f"Тест на одинаковые подряд идущие биты: {bit_test(CPP_RESULTS)}\n")
    print(f"Тест на самую длинную последовательность единиц в блоке: {len_one_test(CPP_RESULTS)}\n")

    print("Python:\n")
    print(f"Частотный побитовый тест: {frequency_test(PYTHON_RESULTS)}\n")
    print(f"Тест на одинаковые подряд идущие биты: {bit_test(PYTHON_RESULTS)}\n")
    print(f"Тест на самую длинную последовательность единиц в блоке: {len_one_test(PYTHON_RESULTS)}\n")

    print("Java:\n")
    print(f"Частотный побитовый тест: {frequency_test(JAVA_RESULTS)}\n")
    print(f"Тест на одинаковые подряд идущие биты: {bit_test(JAVA_RESULTS)}\n")
    print(f"Тест на самую длинную последовательность единиц в блоке: {len_one_test(JAVA_RESULTS)}\n")

if __name__ == "__main__":
    main()
