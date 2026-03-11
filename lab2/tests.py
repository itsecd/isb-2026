import math 
import os
from scipy.special import erfc, gammainc

def load_sequence(filepath):
    """Загружает файл с очередью"""
    with open(filepath, 'r') as f:
        return f.read().strip()
    

def frequency_test(seq):
    """Частотный побитовый тест"""
    n = len(seq)
    s = sum(1 if bit =='1' else -1 for bit in seq)
    s_n = abs(s) / math.sqrt(n)
    p_value = erfc(s_n / math.sqrt(2))
    return p_value


def runs_test(seq):
    """Тест на одинаковые подряд идущие биты"""
    n = len(seq)
    xi = seq.count('1') / n

    if abs(xi - 0.5) >= 2.0 / math.sqrt(n):
        return 0.0
    
    v_obs = 0
    for i in range(n-1):
        if seq[i] != seq[i+1]:
            v_obs += 1

    numerator = abs(v_obs - 2 * n * xi * (1 - xi))
    denominator = 2 * math.sqrt(2*n) * xi * (1 -xi)

    if denominator == 0: return 0.0

    p_value = erfc(numerator / denominator)
    return p_value


def longest_run_ones_test(seq):
    """Тест на самую длинную последовательность едениц в блоке"""
    n = len(seq)
    M = 8
    N = n // M
    pi = [0.2148, 0.3672, 0.2305, 0.1875]
    K = 4
    counts = [0] * K
    for i in range(N):
        block = seq[i*M: (i+1)*M]
        max_run = 0
        current_run = 0
        for bit in block:
            if bit =='1':
                current_run += 1
                if current_run > max_run:
                    max_run = current_run
            else:
                current_run = 0
        if max_run <=1: counts[0] += 1
        elif max_run == 2: counts[1] += 1
        elif max_run == 3: counts[2] += 1
        else: counts[3] += 1

    chi2 = 0
    for i in range(K):
        expected = N *pi[i]
        if expected > 0:
            chi2 += ((counts[i] - expected)**2)/expected
    p_value = gammainc(3/2.0, chi2/2.0)
    return 1.0-p_value


def run_all_tests(filepath):
    """Проводит последовательность из файла через все тесты"""
    print(f"--- Анализ файла: {filepath} ---")
    if not os.path.exists(filepath):
        print("Файл не найден!")
        return

    seq = load_sequence(filepath)
    print(f"Длина последовательности: {len(seq)} бит")
    
    alpha = 0.01
    
    tests = [
        ("Частотный тест (Frequency)", frequency_test),
        ("Тест серий (Runs)", runs_test),
        ("Длинная серия единиц (Longest Run)", longest_run_ones_test)
    ]
    
    results = []
    
    for name, func in tests:
        try:
            p_val = func(seq)
            status = "УСПЕХ" if p_val >= alpha else "ПРОВАЛ"
            print(f"{name}: P-value = {p_val:.6f} [{status}]")
            results.append(f"{name}: {p_val:.6f} [{status}]")
        except Exception as e:
            print(f"{name}: Ошибка выполнения - {e}")
            results.append(f"{name}: Ошибка")
            
    return results


if __name__ == "__main__":
    base_path = "sequences/"
    files = ["sequence_py.txt", "sequence_cpp.txt", "sequence_java.txt"]
    
    all_results = []
    
    for f in files:
        full_path = os.path.join(base_path, f)
        res = run_all_tests(full_path)
        all_results.append(f"\nФайл: {f}\n" + "\n".join(res))
        
    with open("test_results.txt", "w", encoding="utf-8") as out:
        out.write("\n".join(all_results))
        
    print("\nРезультаты сохранены в ../test_results.txt")
