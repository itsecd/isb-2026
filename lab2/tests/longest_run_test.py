import math
from utils import igamc

# Константы из методички для M = 8 (N = 128 бит)
PI_VALUES = [0.2148, 0.3672, 0.2305, 0.1875]

def longest_run_test(sequence):
    """
    Тест на самую длинную последовательность единиц в блоке.
    
    """
    n = len(sequence)
    

    if n != 128:
        print(f"Предупреждение: тест оптимален для 128 бит, получено {n} бит")
    
    M = 8  
    num_blocks = n // M
    
    if num_blocks < 16:
        print(f"Предупреждение: нужно минимум 16 блоков, получено {num_blocks}")
        return 0.0, False, [0, 0, 0, 0]
    

    v = [0, 0, 0, 0]
    

    for i in range(num_blocks):
        block = sequence[i*M : (i+1)*M]

        max_run = 0
        current_run = 0
        
        for bit in block:
            if bit == '1':
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 0
        
 
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
        expected = num_blocks * PI_VALUES[i]
        chi_square += ((v[i] - expected) ** 2) / expected
    

    p_value = igamc(3/2, chi_square/2)
    

    result = p_value >= 0.01
    
    return p_value, result, v

def print_longest_run_test(sequence, sequence_name):
    """Запускает тест и выводит результаты."""
    p_value, result, v = longest_run_test(sequence)
    
    print(f"\n--- Тест на самую длинную последовательность единиц ---")
    print(f"Последовательность: {sequence_name}")
    print(f"Длина: {len(sequence)} бит")
    print(f"Блоки по 8 бит: {len(sequence) // 8}")
    print(f"v0 (макс. длина ≤ 1): {v[0]}")
    print(f"v1 (макс. длина = 2): {v[1]}")
    print(f"v2 (макс. длина = 3): {v[2]}")
    print(f"v3 (макс. длина ≥ 4): {v[3]}")
    print(f"P-value: {p_value:.6f}")
    print(f"Результат: {'СЛУЧАЙНАЯ' if result else 'НЕ СЛУЧАЙНАЯ'}")
    
    return p_value, result