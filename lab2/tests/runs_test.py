import math
from utils import erfc

def runs_test(seq: str) -> float:
    """тест на одинаковые подряд биты"""
    n = len(seq)
    ones = seq.count('1')
    ones_ratio = ones / n
    
    if abs(ones_ratio - 0.5) > (2 / math.sqrt(n)):
        return 0.0
    
    runs = seq.count('01') + seq.count('10')
    
    numerator = abs(runs - 2 * n * ones_ratio * (1 - ones_ratio))
    denominator = 2 * math.sqrt(2 * n) * ones_ratio * (1 - ones_ratio)
    
    p_value = math.erfc(numerator / denominator)
    return p_value

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