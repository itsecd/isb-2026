import math
import const_lab2 as fp

def load_sequence(filename):
    """Загружает битовую последовательность из файла."""
    with open(filename, 'r') as f:
        return f.read().strip()

def monobit_test(seq):
    """Частотный тест. Проверяет соотношение единиц и нулей в последовательности."""
    n = len(seq)
    s_obs = abs(2 * seq.count('1') - n) / math.sqrt(n)
    p_value = math.erfc(s_obs / math.sqrt(2))
    return p_value >= 0.01, p_value

def runs_test(seq):
    """Тест на одинаковые подряд идущие биты.
    Считает количество подряд идущих едениц и нулей"""
    n = len(seq)
    ones = seq.count('1')
    pi = ones / n
    
    if abs(pi - 0.5) >= 2 / math.sqrt(n):
        return False, 0.0
    
    runs = 1 + sum(1 for i in range(1, n) if seq[i] != seq[i-1])
    expected = 2 * n * pi * (1 - pi)
    denom = 2 * math.sqrt(2 * n) * pi * (1 - pi)
    v_obs = (runs - expected) / denom if denom != 0 else 0
    p_value = math.erfc(abs(v_obs) / math.sqrt(2))
    return p_value >= 0.01, p_value

def longest_run_test(seq):
    """Тест на самую длинную последовательность единиц в блоке."""
    n = len(seq)
    
    BLOCK_SIZE = 8
    PI = [0.2148, 0.3672, 0.2305, 0.1875]
    
    num_blocks = n // BLOCK_SIZE
    
    if num_blocks < 3:
        return True, 1.0
    
    blocks = [
        seq[i*BLOCK_SIZE:(i+1)*BLOCK_SIZE] 
        for i in range(num_blocks)
    ]
    
    v = [0, 0, 0, 0]
    
    for block in blocks:
        max_run = 0
        current = 0
        for bit in block:
            if bit == '1':
                current += 1
                max_run = max(max_run, current)
            else:
                current = 0
        
        if max_run <= 1:
            v[0] += 1
        elif max_run == 2:
            v[1] += 1
        elif max_run == 3:
            v[2] += 1
        else:
            v[3] += 1
    
    chi2 = 0.0
    for i in range(4):
        expected = num_blocks * PI[i]
        if expected > 0:
            chi2 += (v[i] - expected) ** 2 / expected
    
    p_value = math.exp(-chi2 / 2)
    
    p_value = max(0.0, min(1.0, p_value))
    
    return p_value >= 0.01, p_value

def test_file(filename):
    """Запускает все три теста для одного файла."""
    seq = load_sequence(filename)
    
    tests = [
        ("Monobit Test", monobit_test(seq)),
        ("Runs Test", runs_test(seq)),
        ("Longest Run Test", longest_run_test(seq)),
    ]
    
    return tests

def save_results_to_file(all_results, output_filename):
    """Сохраняет результаты всех тестов в файл отчёта."""
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write("ОТЧЕТ О СТАТИСТИЧЕСКИХ ТЕСТАХ NIST\n")
        
        total_tests = 0
        passed_tests = 0
        
        for filename, tests in all_results:
            f.write(f"ФАЙЛ: {filename}\n")
            
            file_passed = 0
            for test_name, (passed, value) in tests:
                total_tests += 1
                if passed:
                    passed_tests += 1
                    file_passed += 1
                
                status = "УДАЧНО" if passed else "НЕУДАЧНО"
                f.write(f"  {test_name:<30} Значение: {value:<12.6f} [{status}]\n")
            
            f.write(f"  File Result: {file_passed}/{len(tests)} tests passed\n\n")
        
        f.write("ИТОГ\n")
        f.write(f"Количество протестированных файлов: {len(all_results)}\n")
        f.write(f"Количество успешных тестов: {passed_tests}/{total_tests}\n")
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        f.write(f"Показатель успеха: {success_rate:.1f}%\n")
        
        if passed_tests == total_tests:
            f.write("\nВсе тесты пройдены успешно - последовательности случайны\n")
        else:
            f.write(f"\n{total_tests - passed_tests} тестов неудачны\n")
    
    return output_filename

def main():
    """Основная функция. Тестирует 3 файла с последовательностями и сохраняет результат в файл."""
    
    all_results = []
    
    for filename in fp.TEST_FILES:
        try:
            tests = test_file(filename)
            all_results.append((filename, tests))
            
        except FileNotFoundError:
            print(f"\nFile '{filename}' not found.")
        except Exception as e:
            print(f"\nError testing '{filename}': {str(e)}")
    
    if all_results:
        save_results_to_file(all_results, fp.OUTPUT_FILE)
        print(f"\nResults saved to: {fp.OUTPUT_FILE}\n")

if __name__ == "__main__":
    main()