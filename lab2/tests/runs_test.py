import math
from utils import erfc

def runs_test(sequence):
    """
    Тест на одинаковые подряд идущие биты (Runs Test).
    
    """
    n = len(sequence)
    
    if n == 0:
        return 0.0, False
    

    ones = sequence.count('1')
    pi = ones / n
    

    if abs(pi - 0.5) >= (2 / math.sqrt(n)):
        return 0.0, False
    

    runs = 1
    for i in range(1, n):
        if sequence[i] != sequence[i-1]:
            runs += 1
    

    numerator = abs(runs - 2 * n * pi * (1 - pi))
    denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)
    
    if denominator == 0:
        return 0.0, False
    
    p_value = erfc(numerator / denominator)
    

    result = p_value >= 0.01
    
    return p_value, result

def print_runs_test(sequence, sequence_name):
    """Запускает тест и выводит результаты."""
    p_value, result = runs_test(sequence)
    
    print(f"\n--- Тест на одинаковые подряд идущие биты ---")
    print(f"Последовательность: {sequence_name}")
    print(f"Длина: {len(sequence)} бит")
    print(f"Количество единиц: {sequence.count('1')}")
    print(f"Доля единиц: {sequence.count('1')/len(sequence):.3f}")
    print(f"P-value: {p_value:.6f}")
    print(f"Результат: {'СЛУЧАЙНАЯ' if result else 'НЕ СЛУЧАЙНАЯ'}")
    
    return p_value, result