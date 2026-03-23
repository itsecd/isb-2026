import math
import os
from scipy.special import gammainc
from typing import List, Tuple, Dict, Optional
import constants
    
def read_sequence(file_path: str) -> Optional[str]:
    """
    Чтение файла с последовательностью

    Args:
        file_path: Путь к входному файлу с текстом
    Returns:
        Строка последовательности
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read().strip()
            sequence = ''.join(c for c in content if c in '01')
            return sequence if sequence else None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None
    
def frequency_test(sequence: str) -> float:
    """
    Частотный побитовый тест
    Args:
        sequence: Строка последовательности
    Returns:
        P-значение
    """
    n = len(sequence)
    x_i = [1 if bit == '1' else -1 for bit in sequence]
    s_n = sum(x_i) / math.sqrt(n)
    p_value = math.erfc(abs(s_n) / math.sqrt(2))
    return p_value

def runs_test(sequence: str) -> float:
    """
    Тест на одинаковые подряд идущие биты
    Args:
        sequence: Строка последовательности
    Returns:
        P-значение
    """        
    n = len(sequence)
    ones = sequence.count("1")
    zeta = ones / n
        
    if abs(zeta - 0.5) >= 2.0 / math.sqrt(n):
        return 0.0
        
    v_n = 0
    for i in range(n - 1):
        if sequence[i] != sequence[i + 1]:
            v_n += 1
        
    numerator = abs(v_n - 2 * n * zeta * (1 - zeta))
    denominator = 2 * math.sqrt(2 * n) * zeta * (1 - zeta)
    p_value = math.erfc(numerator / denominator)
    return p_value
    
def longest_run_test(sequence: str) -> float:
    """
    Тест на самую длинную последовательность единиц в блоке
    Args:
        sequence: Строка последовательности
    Returns:
        P-значение
    """
    n = len(sequence)
    num_blocks = n // 8
        
    max_runs = []
    for i in range(num_blocks):
        block = sequence[i*8:(i+1)*8]
        max_run = 0
        current_run = 0
        for bit in block:
            if bit == '1':
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 0
        max_runs.append(max_run)
        
    v = [0, 0, 0, 0]
    for run in max_runs:
        if run <= 1:
            v[0] += 1
        elif run == 2:
            v[1] += 1
        elif run == 3:
            v[2] += 1
        else: 
            v[3] += 1
        
    chi_squared = 0
    for i in range(4):
        expected = num_blocks * constants.PI[i]
        if expected > 0:
            chi_squared += (v[i] - expected)**2 / expected

    p_value = gammainc(3/2, chi_squared/2)
           
    return p_value
    
def analyze_file(filename: str) -> Dict:
    """
    Анализ последовательности из файла
    Args:
        filename: Название файла с последовательностью
    Returns:
        Словарь с результатами анализа
    """
    sequence = read_sequence(filename)
        
    results = {}
        
    p1 = frequency_test(sequence)
    res1 = "pass" if p1 > constants.THRESHOLD else "fail"
    results['frequency'] = {'p_value': p1, 'result': res1}
        
    p2 = runs_test(sequence)
    res2 = "pass" if p2 > constants.THRESHOLD else "fail"
    results['runs'] = {'p_value': p2, 'result': res2}
        
    p3 = longest_run_test(sequence)
    res3 = "pass" if p3 > constants.THRESHOLD else "fail"
    results['longest_run'] = {'p_value': p3, 'result': res3}

    return results
    
def save_results(java_results: Dict, cpp_results: Dict, filename:str):
    """
    Сохранение результата в файл
    Args:
        java_results: Результаты анализа последовательности генератора Java
        cpp_results: Результаты анализа последоватеьности генератора C++
        filename: Имя файла для вывода
    """
    with open(filename, 'w', encoding='utf-8') as f:  
        f.write(f"Критерий случайности: P-значение >= {constants.THRESHOLD}")
        f.write("\nРезультаты анализа:\n")
        
        if java_results:
            java_passed = (java_results['frequency']['p_value'] >= 0.01 and
                            java_results['runs']['p_value'] >= 0.01 and
                            java_results['longest_run']['p_value'] >= 0.01)
            
            java_status = "СЛУЧАЙНАЯ" if java_passed else "НЕ СЛУЧАЙНАЯ"
            f.write(f"\nJava (java.util.Random): {java_status}\n")
            f.write(f"  - Частотный тест: P = {java_results['frequency']['p_value']:.6f}\n")
            f.write(f"  - Тест на одинаковые подряд идущие биты: P = {java_results['runs']['p_value']:.6f}\n")
            f.write(f"  - Тест на самую длинную последовательность единиц в блоке: P = {java_results['longest_run']['p_value']:.6f}\n")
        
        if cpp_results:
            cpp_passed = (cpp_results['frequency']['p_value'] >= 0.01 and
                            cpp_results['runs']['p_value'] >= 0.01 and
                            cpp_results['longest_run']['p_value'] >= 0.01)
            
            cpp_status = "СЛУЧАЙНАЯ" if cpp_passed else "НЕ СЛУЧАЙНАЯ"
            f.write(f"\nC++ (rand()): {cpp_status}\n")
            f.write(f"  - Частотный тест: P = {cpp_results['frequency']['p_value']:.6f}\n")
            f.write(f"  - Тест на одинаковые подряд идущие биты: P = {cpp_results['runs']['p_value']:.6f}\n")
            f.write(f"  - Тест на самую длинную последовательность единиц в блоке: P = {cpp_results['longest_run']['p_value']:.6f}\n")       

def main() -> None:
    print("="*70)
    print("Анализ последовательностей, сгенерированных Java и C++")
    print("="*70)
    
    java_file = "java_sequence.txt"
    cpp_file = "cpp_sequence.txt"
    result_file = "analysis.txt"
    
    java_results = None
    cpp_results = None
    
    if os.path.exists(java_file):
        print(f"\nНайден файл: {java_file}")
        java_results = analyze_file(java_file)
    else:
        print(f"\nФайл {java_file} не найден!")
        print("Пожалуйста, сначала запустите программу на Java для генерации последовательности.")
    
    if os.path.exists(cpp_file):
        print(f"\nНайден файл: {cpp_file}")
        cpp_results = analyze_file(cpp_file)
    else:
        print(f"\nФайл {cpp_file} не найден!")
        print("Пожалуйста, сначала запустите программу на C++ для генерации последовательности.")
    

    if java_results and cpp_results:
        save_results(java_results, cpp_results,result_file)
        print("\n" + "="*70)
        print("Анализ завершен!")
        print(f"Результаты сохранены в {result_file}")
        print("="*70)

if __name__ == "__main__":
    main()