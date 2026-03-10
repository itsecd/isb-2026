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

# b) Тест на одинаковые подряд идущие биты
def runs_test(sequence):
    N = len(sequence)
    
    if N == 0:
        return 0.0
    
    ones_count = sum(int(bit) for bit in sequence)
    Z = ones_count / N
    
    condition_check = abs(Z - 0.5)
    threshold = 2.0 / math.sqrt(N)
    
    if condition_check >= threshold:
        print("Условие однородности НЕ выполнено! Возвращаем P-value = 0")
        return 0.0
    
    V_N = 0
    for i in range(N - 1):
        if sequence[i] != sequence[i + 1]:
            V_N += 1
    
    expected_value = 2 * N * Z * (1 - Z)
    numerator = abs(V_N - expected_value)
    denominator = 2 * math.sqrt(2 * N) * Z * (1 - Z)
    
    if denominator == 0:
        print("Знаменатель равен 0! Возвращаем P-value = 0")
        return 0.0
    
    z_score = numerator / denominator
    p_value = math.erfc(z_score / math.sqrt(2))
    
    return p_value

# c) Тест на самую длинную последовательность единиц в блоке
def longest_run_ones_test(sequence):
    n_total = len(sequence)
    M = 8
    
    if n_total % M != 0:
        # Обрезаем до кратного, если вдруг длина не идеальна
        n_total = (n_total // M) * M
        sequence = sequence[:n_total]
        
    N_blocks = n_total // M
    
    if N_blocks == 0:
        return 0.0

    # Теоретические вероятности для M=8 (из стандарта NIST для M=8)
    # Сумма должна быть ровно 1.0
    # pi_0 (<=1), pi_1 (=2), pi_2 (=3), pi_3 (>=4)
    probs = [
        0.2148,   # P(K <= 1)
        0.3672,   # P(K = 2)
        0.2305,   # P(K = 3)
        0.1875    # P(K >= 4) -> 1 - (0.2148 + 0.3672 + 0.2305)
    ]
    
    # Счетчики категорий v_0, v_1, v_2, v_3
    counts = [0] * 4

    for i in range(N_blocks):
        block_start = i * M
        block_end = block_start + M
        block = sequence[block_start:block_end]
        
        max_run = 0
        current_run = 0
        
        # Поиск самой длинной серии единиц в блоке
        for bit in block:
            if bit == '1':
                current_run += 1
                if current_run > max_run:
                    max_run = current_run
            else:
                current_run = 0
        
        if max_run <= 1:
            counts[0] += 1
        elif max_run == 2:
            counts[1] += 1
        elif max_run == 3:
            counts[2] += 1
        else: # max_run >= 4
            counts[3] += 1
    
    # Расчет Хи-квадрат (стр. 12)
    # chi_sq = sum( (v_i - N*pi_i)^2 / (N*pi_i) )
    chi_sq = 0.0
    for i in range(4):
        expected = N_blocks * probs[i]
        observed = counts[i]
        term = ((observed - expected) ** 2) / expected
        chi_sq += term
    df = 3
    
    try:
        p_value = 1.0 - stats.chi2.cdf(chi_sq, df)
    except Exception as e:
        print(f"Ошибка расчета P-value: {e}")
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