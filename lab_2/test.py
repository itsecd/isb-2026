import os
import math
import csv
from datetime import datetime
from scipy import stats

def get_script_dir():
    return os.path.dirname(os.path.abspath(__file__))

def read_sequence(filename):
    script_dir = get_script_dir()
    full_path = os.path.join(script_dir, filename)
    try:
        with open(full_path, 'r') as f:
            data = f.read().strip()
        if not data:
            print(f"Файл '{filename}' пуст!")
            return None
        if not all(c in '01' for c in data):
            print(f"Файл '{filename}' содержит не бинарные данные!")
            return None
        return data
    except Exception as e:
        print(f"Ошибка чтения файла {filename}: {e}")
        return None

# a) Частотный побитовый тест
def monobit_test(sequence):
    n = len(sequence)
    if n == 0:
        return 0.0
    transformed_sum = sum(1 if bit == '1' else -1 for bit in sequence)
    s_obs = abs(transformed_sum) / math.sqrt(n)
    p_value = math.erfc(s_obs / math.sqrt(2))
    return p_value

# b) Тест на серии (Runs Test)
def runs_test(sequence):
    n = len(sequence)
    if n == 0:
        return 0.0
    pi = sum(int(bit) for bit in sequence) / n
    
    # Предварительная проверка (упрощенная)
    if abs(pi - 0.5) >= (2.0 / math.sqrt(n)):
        return 0.0 

    v_obs = 1
    for i in range(n - 1):
        if sequence[i] != sequence[i+1]:
            v_obs += 1
            
    numerator = abs(v_obs - 2 * n * pi * (1 - pi))
    denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)
    
    if denominator == 0:
        return 0.0
        
    p_value = math.erfc(numerator / denominator)
    return p_value

# c) Тест на самую длинную последовательность единиц в блоке
def longest_run_ones_test(sequence):
    n = len(sequence)
    block_size = 16
    num_blocks = n // block_size
    
    if num_blocks == 0:
        return 0.0

    # Вероятности для M=16 (NIST SP 800-22)
    probs = [
        0.21484375,   # K=1
        0.36718750,   # K=2
        0.23046875,   # K=3
        0.11718750,   # K=4
        0.05468750,   # K=5
        0.01562500    # K>=6
    ]
    
    counts = [0] * 6 
    
    for i in range(num_blocks):
        block = sequence[i*block_size : (i+1)*block_size]
        max_run = 0
        current_run = 0
        
        for bit in block:
            if bit == '1':
                current_run += 1
                if current_run > max_run:
                    max_run = current_run
            else:
                current_run = 0
        
        # Маппинг длины серии на индекс категории
        if max_run == 0:
            idx = 0 
        elif max_run <= 5:
            idx = max_run - 1
        else:
            idx = 5
            
        counts[idx] += 1
            
    chi_sq = 0.0
    for i in range(6):
        expected = num_blocks * probs[i]
        if expected > 0:
            chi_sq += ((counts[i] - expected) ** 2) / expected
            
    try:
        p_value = 1.0 - stats.chi2.cdf(chi_sq, 5)
    except Exception:
        return 0.0
    
    return p_value

def run_single_test_set(filename, label, results_list, alpha=0.01):
    """Запускает тесты для одного файла и добавляет результаты в список"""
    print(f"\n--- Обработка: {label} ({filename}) ---")
    seq = read_sequence(filename)
    
    if seq is None:
        # Добавляет запись об ошибке в результаты
        results_list.append({
            "Source": label,
            "File": filename,
            "Test": "FILE_ERROR",
            "P-Value": "N/A",
            "Result": "FAIL",
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        return

    tests = [
        ("Monobit Frequency", monobit_test),
        ("Runs Test", runs_test),
        ("Longest Run of Ones", longest_run_ones_test)
    ]

    for test_name, test_func in tests:
        try:
            p_val = test_func(seq)
            status = "PASS" if p_val >= alpha else "FAIL"
            
            result_entry = {
                "Source": label,
                "File": filename,
                "Test": test_name,
                "P-Value": f"{p_val:.6f}",
                "Result": status,
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            results_list.append(result_entry)
            
            print(f"{test_name}: P-Value = {p_val:.6f} [{status}]")
            
        except Exception as e:
            print(f"Ошибка при выполнении теста {test_name}: {e}")
            results_list.append({
                "Source": label,
                "File": filename,
                "Test": test_name,
                "P-Value": "ERROR",
                "Result": "FAIL",
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

def save_results_to_csv(results_list, output_filename="nist_results.csv"):
    """Сохраняет список результатов в CSV файл"""
    script_dir = get_script_dir()
    full_path = os.path.join(script_dir, output_filename)
    
    if not results_list:
        print("\nНет данных для сохранения в CSV.")
        return

    fieldnames = ["Timestamp", "Source", "File", "Test", "P-Value", "Result"]
    
    try:
        with open(full_path, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results_list)
        
        print(f"\nРезультаты успешно сохранены в файл: {full_path}")
    except Exception as e:
        print(f"\nНе удалось сохранить CSV: {e}")

if __name__ == "__main__":
    all_results = []
    
    # Список файлов для проверки
    # Можно легко добавить новые генераторы, просто дописав строку сюда
    targets = [
        ("sequence_cpp.txt", "C++ Generator"),
        ("sequence_java.txt", "Java Generator")
    ]

    for filename, label in targets:
        run_single_test_set(filename, label, all_results)

    # Сохранение в CSV
    save_results_to_csv(all_results)
    
    print("\nРабота завершена.")