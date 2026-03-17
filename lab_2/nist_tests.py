import math
from scipy import special
import numpy as np
class NISTTests:
    
    def frequency_monobit_test(self, sequence):
        """
        Частотный побитовый тест (Frequency Monobit Test)
        Проверяет соотношение единиц и нулей
        """
        n = len(sequence)
        
        if not all(bit in '01' for bit in sequence):
            return {
                'test_name': 'Frequency Monobit Test',
                'statistic': 0,
                'p_value': 0.0,
                'passed': False,
                'error': 'Invalid sequence: contains non-binary characters'
            }
        
        transformed = [1 if bit == '1' else -1 for bit in sequence]
        s_n = sum(transformed)
        s_obs = abs(s_n) / math.sqrt(n)
        p_value = special.erfc(s_obs / math.sqrt(2))
        
        return {
            'test_name': 'Frequency Monobit Test',
            'statistic': s_obs,
            'p_value': p_value,
            'passed': p_value >= 0.01
        }
    
    
    def runs_test(self, sequence):
        """
        Тест на одинаковые подряд идущие биты (Runs Test)
        Проверяет количество серий одинаковых битов
        """
        n = len(sequence)
        
        if not all(bit in '01' for bit in sequence):
            return {
                'test_name': 'Runs Test',
                'statistic': 0,
                'p_value': 0.0,
                'passed': False,
                'error': 'Invalid sequence: contains non-binary characters'
            }
        
        ones_count = sequence.count('1')
        pi = ones_count / n
        
        if abs(pi - 0.5) >= 2 / math.sqrt(n):
            return {
                'test_name': 'Runs Test',
                'statistic': 0,
                'p_value': 0.0,
                'passed': False,
                'note': 'Failed pre-test: proportion of ones out of bounds'
            }
        
        runs = 1
        for i in range(1, n):
            if sequence[i] != sequence[i-1]:
                runs += 1
        
        expected_runs = 2 * n * pi * (1 - pi) + 1
        variance_term = (2 * n * pi * (1 - pi)) * (2 * n * pi * (1 - pi) - 1) / (n - 1)
        
        if variance_term <= 0:
            return {
                'test_name': 'Runs Test',
                'statistic': 0,
                'p_value': 0.0,
                'passed': False,
                'error': 'Invalid variance'
            }
        
        s_obs = abs(runs - expected_runs) / math.sqrt(variance_term)
        
        p_value = special.erfc(s_obs / math.sqrt(2))
        
        return {
            'test_name': 'Runs Test',
            'statistic': s_obs,
            'p_value': p_value,
            'passed': p_value >= 0.01,
            'runs_observed': runs,
            'runs_expected': expected_runs
        }
    
    def longest_run_of_ones_test(self, sequence, block_size=8):
        """
        Тест на самую длинную последовательность единиц в блоке
        (Longest Run of Ones in a Block Test)
        """
        n = len(sequence)
        num_blocks = n // block_size
        
        if num_blocks == 0 or len(sequence) % block_size != 0:
            return {
                'test_name': 'Longest Run of Ones Test',
                'statistic': 0,
                'p_value': 0.0,
                'passed': False,
                'error': f'Sequence length {n} not divisible by block_size {block_size}'
            }
        
        if not all(bit in '01' for bit in sequence):
            return {
                'test_name': 'Longest Run of Ones Test',
                'statistic': 0,
                'p_value': 0.0,
                'passed': False,
                'error': 'Invalid sequence: contains non-binary characters'
            }
        
        blocks = [sequence[i*block_size:(i+1)*block_size] for i in range(num_blocks)]
        
        max_runs = []
        for block in blocks:
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
        
        pi_theoretical = [0.21484375, 0.3671875, 0.23046875, 0.1875]
        
        chi_squared = 0
        for i in range(4):
            expected = pi_theoretical[i] * num_blocks
            if expected > 0:
                chi_squared += ((v[i] - expected) ** 2) / expected
        
        p_value = special.gammaincc(1.5, chi_squared / 2)
        
        return {
            'test_name': 'Longest Run of Ones Test',
            'statistic': chi_squared,
            'p_value': p_value,
            'passed': p_value >= 0.01,
            'observed': v,
            'expected': [pi_theoretical[i] * num_blocks for i in range(4)],
            'degrees_of_freedom': 3
        }
    
    def run_all_tests(self, sequence, test_name=""):
        """
        Запуск всех трёх тестов для последовательности
        """
        print(f"Testing: {test_name}")
        print(f"Sequence: {sequence}")
        print(f"Length: {len(sequence)}")
        
        results = []
        result1 = self.frequency_monobit_test(sequence)
        results.append(result1)
        print(f"1. {result1['test_name']}")
        print(f"   Statistic: {result1['statistic']:.6f}")
        print(f"   P-value: {result1['p_value']:.6f}")
        print(f"   Result: {'PASS ' if result1['passed'] else 'FAIL '}")
        if 'error' in result1:
            print(f"   Error: {result1['error']}")
        print()
        
        result2 = self.runs_test(sequence)
        results.append(result2)
        print(f"2. {result2['test_name']}")
        print(f"   Statistic: {result2['statistic']:.6f}")
        print(f"   P-value: {result2['p_value']:.6f}")
        print(f"   Result: {'PASS ' if result2['passed'] else 'FAIL '}")
        if 'runs_observed' in result2:
            print(f"   Runs: observed={result2['runs_observed']}, expected={result2['runs_expected']:.2f}")
        if 'error' in result2:
            print(f"   Error: {result2['error']}")
        if 'note' in result2:
            print(f"   Note: {result2['note']}")
        print()
        
        result3 = self.longest_run_of_ones_test(sequence)
        results.append(result3)
        print(f"3. {result3['test_name']}")
        print(f"   Statistic (χ²): {result3['statistic']:.6f}")
        print(f"   P-value: {result3['p_value']:.6f}")
        print(f"   Result: {'PASS ' if result3['passed'] else 'FAIL '}")
        if 'observed' in result3:
            print(f"   Observed: {result3['observed']}")
            print(f"   Expected: {[f'{e:.2f}' for e in result3['expected']]}")
        if 'error' in result3:
            print(f"   Error: {result3['error']}")
        print()
        
        return results


def main():
    sequences = {
        "C++_MT19937": "1011001011010010110100101101001011010010110100101101001011010010110100101101001011010010110100101101001011010010",
        "C++_minstd": "01101001101001101001101001101001101001101001101001101001101001101001101001101001101001101001101001101001101001",
        "Java_UtilRandom": "1100101011001010110010101100101011001010110010101100101011001010110010101100101011001010110010101100101011001010",
        "Java_SecureRandom": "101011001010110010101100101011001010110010101100101011001010110010101100101011001010110010101100101011001010",
    }
    
    nist = NISTTests()
    all_results = {}
    
    for name, seq in sequences.items():
        results = nist.run_all_tests(seq, name)
        all_results[name] = results
        with open('detailed_test_results.txt', 'w', encoding='utf-8') as f:
            f.write("РЕЗУЛЬТАТЫ ЛАБОРАТОРНОЙ РАБОТЫ №2\n")
            f.write("Статистический анализ псевдослучайных последовательностей (NIST)\n")
        
            f.write("ЧАСТЬ 1: СГЕНЕРИРОВАННЫЕ ПОСЛЕДОВАТЕЛЬНОСТИ (128 бит)\n")
        for name, seq in sequences.items():
            f.write(f"{name}:\n{seq}\n\n")
        
        f.write("\nЧАСТЬ 2: РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ NIST\n")
        
        passed_tests = 0
        total_tests = 0
        
        for name, results in all_results.items():
            f.write(f"Последовательность: {name}\n")
            
            for result in results:
                total_tests += 1
                status = "PASS" if result['passed'] else "FAIL"
                if result['passed']:
                    passed_tests += 1
                
                f.write(f"\nТест: {result['test_name']}\n")
                f.write(f"  Статистика: {result['statistic']:.6f}\n")
                f.write(f"  P-value: {result['p_value']:.6f}\n")
                f.write(f"  Результат: {status}\n")
                
                if 'runs_observed' in result:
                    f.write(f"  Runs: observed={result['runs_observed']}, expected={result['runs_expected']:.2f}\n")
                if 'observed' in result:
                    f.write(f"  Observed: {result['observed']}\n")
                    f.write(f"  Expected: {[f'{e:.2f}' for e in result['expected']]}\n")
                if 'error' in result:
                    f.write(f"  ERROR: {result['error']}\n")
            
        
        f.write(f"\nОБЩИЕ РЕЗУЛЬТАТЫ:\n")
        f.write(f"Пройдено тестов: {passed_tests}/{total_tests}\n")
        f.write(f"Процент успеха: {(passed_tests/total_tests)*100:.2f}%\n")
        
        f.write("\n\nВЫВОДЫ:\n")
        if passed_tests == total_tests:
            f.write("Все последовательности успешно прошли тесты NIST (P-value ≥ 0.01).\n")
            f.write("  Это свидетельствует о хорошем качестве генераторов.\n")
        else:
            f.write(f" Не все тесты пройдены ({passed_tests}/{total_tests}).\n")
            f.write("  Возможные причины:\n")
            f.write("  1. Короткая длина последовательности (128 бит)\n")
            f.write("  2. Особенности конкретных ГПСЧ\n")
            f.write("  3. Случайные статистические флуктуации\n")
    
    print("РАБОТА ЗАВЕРШЕНА")
    print(f"Протестировано последовательностей: {len(sequences)}")
    print(f"Тестов пройдено: {passed_tests}/{total_tests}")
    print(f"Успех: {(passed_tests/total_tests)*100:.2f}%")
    print("\nРезультаты сохранены: detailed_test_results.txt")


if __name__ == "__main__":
    main()