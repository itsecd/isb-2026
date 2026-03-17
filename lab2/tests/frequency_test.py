import math
from utils import erfc

def frequency_test(sequence):
    """
    Частотный побитовый тест (Frequency Test).
   
    """
    n = len(sequence)
    
    if n == 0:
        return 0.0, False

    s = 0
    for bit in sequence:
        if bit == '1':
            s += 1
        else:
            s -= 1
    

    s_obs = abs(s) / math.sqrt(n)
    

    p_value = erfc(s_obs / math.sqrt(2))
    

    result = p_value >= 0.01
    
    return p_value, result

def print_frequency_test(sequence, sequence_name):
    """Запускает тест и выводит результаты."""
    p_value, result = frequency_test(sequence)
    
    print(f"\n--- Частотный побитовый тест ---")
    print(f"Последовательность: {sequence_name}")
    print(f"Длина: {len(sequence)} бит")
    print(f"Количество единиц: {sequence.count('1')}")
    print(f"Количество нулей: {sequence.count('0')}")
    print(f"P-value: {p_value:.6f}")
    print(f"Результат: {'СЛУЧАЙНАЯ' if result else 'НЕ СЛУЧАЙНАЯ'}")
    
    return p_value, result