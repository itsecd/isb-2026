import math
import os
import scipy.special as sp
from typing import Dict, Optional, Union

def read_sequence(filename: str) -> Optional[str]:
    """
    Считывает бинарную последовательность из указанного текстового файла.
    """
    if not os.path.exists(filename):
        return None
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read().strip()

def write_results(filename: str, all_results: Dict[str, Dict[str, Union[float, str]]]) -> None:
    """
    Записывает результаты статистических тестов в текстовый файл.
    Вывод в консоль не производится.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        for generator_name, results in all_results.items():
            f.write(f"--- Результаты для {generator_name} ---\n")
            for key, value in results.items():
                f.write(f"{key}: {value}\n")
            f.write("\n")

def frequency_test(seq: str) -> float:
    """
    Выполняет частотный побитовый тест (Frequency Test) для проверки 
    соотношения нулей и единиц в последовательности.
    """
    n = len(seq)
    sn = sum(1 if bit == '1' else -1 for bit in seq)
    s_obs = abs(sn) / math.sqrt(n)
    p_value = math.erfc(s_obs / math.sqrt(2))
    return p_value

def runs_test(seq: str) -> float:
    """
    Выполняет тест на одинаковые подряд идущие биты (Runs Test) 
    для оценки частоты смены битов ('0' на '1' и наоборот).
    Расчет строго по методическим указаниям (без +1 к V_N).
    """
    n = len(seq)
    pi = seq.count('1') / n
    
    # Проверка предварительного условия
    if abs(pi - 0.5) >= (2 / math.sqrt(n)):
        return 0.0

    v_n_obs = sum(1 for i in range(n - 1) if seq[i] != seq[i+1])
    
    # Вычисляем P-value
    numerator = abs(v_n_obs - 2 * n * pi * (1 - pi))
    denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)
    p_value = math.erfc(numerator / denominator)
    
    return p_value

def longest_run_ones_in_a_block_test(seq: str) -> float:
    """
    Выполняет тест на самую длинную последовательность единиц в блоке 
    (Longest Run of Ones in a Block Test). Оценивает кластеризацию единиц.
    """
    pi_vals = [0.2148, 0.3672, 0.2305, 0.1875]
    M = 8
    N = 128
    num_blocks = N // M
    
    v = [0, 0, 0, 0]
    
    for i in range(num_blocks):
        block = seq[i*M : (i+1)*M]
        max_run = 0
        current_run = 0
        for bit in block:
            if bit == '1':
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 0
                
        if max_run <= 1: v[0] += 1
        elif max_run == 2: v[1] += 1
        elif max_run == 3: v[2] += 1
        else: v[3] += 1

    chi_squared = sum(((v[i] - num_blocks * pi_vals[i]) ** 2) / (num_blocks * pi_vals[i]) for i in range(4))
    p_value = sp.gammaincc(3/2, chi_squared/2)
    return p_value

if __name__ == "__main__":
    files_to_test: Dict[str, str] = {
        "ГПСЧ C++": "sequence.txt",
        "ГПСЧ Java": "sequence_java.txt"
    }
    
    all_results: Dict[str, Dict[str, Union[float, str]]] = {}
    
    for name, filename in files_to_test.items():
        seq = read_sequence(filename)
        if seq and len(seq) == 128:
            all_results[name] = {
                "Частотный побитовый тест (P-value)": frequency_test(seq),
                "Тест на подряд идущие биты (P-value)": runs_test(seq),
                "Тест на самую длинную последовательность единиц (P-value)": longest_run_ones_in_a_block_test(seq)
            }
        else:
            all_results[name] = {"Ошибка": f"Файл {filename} не найден или его длина не равна 128 битам"}
            
    write_results("test_results.txt", all_results)