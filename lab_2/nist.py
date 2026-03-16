import math
from scipy import special
import numpy as np
from datetime import datetime

class NISTTests:
    
    def frequency_test(self, sequence):
        n = len(sequence)
        sum_bits = sum(1 if bit == '1' else -1 for bit in sequence)
        s_obs = abs(sum_bits) / math.sqrt(n)
        p_value = special.erfc(s_obs / math.sqrt(2))
        
        return {
            'test_name': 'Frequency (Monobit) Test',
            'statistic': s_obs,
            'p_value': p_value,
            'result': 'PASS' if p_value >= 0.01 else 'FAIL'
        }
    
    def runs_test(self, sequence):
        n = len(sequence)
        pi = sum(1 for bit in sequence if bit == '1') / n
        
        if abs(pi - 0.5) >= 2 / math.sqrt(n):
            return {
                'test_name': 'Runs Test',
                'statistic': 0,
                'p_value': 0.0,
                'result': 'FAIL'
            }
        
        v_n = 0
        for i in range(n - 1):
            if sequence[i] != sequence[i + 1]:
                v_n += 1
        
        numerator = abs(v_n - 2 * n * pi * (1 - pi))
        denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)
        
        if denominator == 0:
            return {
                'test_name': 'Runs Test',
                'statistic': 0,
                'p_value': 0.0,
                'result': 'FAIL'
            }
        
        statistic = numerator / denominator
        p_value = special.erfc(statistic / math.sqrt(2))
        
        return {
            'test_name': 'Runs Test',
            'statistic': statistic,
            'p_value': p_value,
            'result': 'PASS' if p_value >= 0.01 else 'FAIL'
        }
    
    def longest_run_of_ones_test(self, sequence):
        n = len(sequence)
        block_size = 8
        num_blocks = n // block_size
        
        blocks = []
        for i in range(num_blocks):
            block = sequence[i * block_size:(i + 1) * block_size]
            blocks.append(block)
        
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
        
        pi = [0.21484375, 0.36718750, 0.23046875, 0.18750000]
        
        chi_squared = 0
        for i in range(4):
            expected = pi[i] * num_blocks
            if expected > 0:
                chi_squared += ((v[i] - expected) ** 2) / expected
        
        p_value = special.gammaincc(3/2, chi_squared/2)
        
        return {
            'test_name': 'Longest Run of Ones in Block Test',
            'statistic': chi_squared,
            'p_value': p_value,
            'result': 'PASS' if p_value >= 0.01 else 'FAIL',
            'block_counts': v,
            'max_runs_per_block': max_runs
        }
    
    def additional_test_serial(self, sequence, m=2):
        n = len(sequence)
        
        freq = {}
        for i in range(n - m + 1):
            subseq = sequence[i:i+m]
            freq[subseq] = freq.get(subseq, 0) + 1
        
        expected = (n - m + 1) / (2 ** m)
        
        chi_squared = sum((count - expected) ** 2 / expected for count in freq.values())
        
        df = 2 ** m - 1
        p_value = special.gammaincc(df / 2, chi_squared / 2)
        
        return {
            'test_name': f'Serial Test (m={m})',
            'statistic': chi_squared,
            'p_value': p_value,
            'result': 'PASS' if p_value >= 0.01 else 'FAIL'
        }


def run_all_tests(sequences, output_file='final_test_results.txt'):
    """
    Запуск всех тестов для всех последовательностей с автоматическими выводами
    """
    tester = NISTTests()
    total_sequences = len(sequences)
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    test_stats = {
        'Frequency': {'pass': 0, 'fail': 0},
        'Runs': {'pass': 0, 'fail': 0},
        'Longest Run': {'pass': 0, 'fail': 0},
        'Serial': {'pass': 0, 'fail': 0}
    }
    
    passed_sequences = []
    failed_sequences = []
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ NIST\n")
        
        for idx, seq in enumerate(sequences, 1):
            f.write(f"ПОСЛЕДОВАТЕЛЬНОСТЬ {idx}\n")
            f.write(f"Длина: {len(seq)} бит\n")
            f.write(f"Последовательность: {seq}\n")
            
            seq_passed = True
            
            result = tester.frequency_test(seq)
            f.write(f"\n{result['test_name']}\n")
            f.write(f"  Статистика: {result['statistic']:.6f}\n")
            f.write(f"  P-value: {result['p_value']:.6f}\n")
            f.write(f"  Результат: {result['result']}\n")
            
            total_tests += 1
            if result['result'] == 'PASS':
                passed_tests += 1
                test_stats['Frequency']['pass'] += 1
            else:
                failed_tests += 1
                test_stats['Frequency']['fail'] += 1
                seq_passed = False
            
            result = tester.runs_test(seq)
            f.write(f"\n{result['test_name']}\n")
            f.write(f"  Статистика: {result['statistic']:.6f}\n")
            f.write(f"  P-value: {result['p_value']:.6f}\n")
            f.write(f"  Результат: {result['result']}\n")
            
            total_tests += 1
            if result['result'] == 'PASS':
                passed_tests += 1
                test_stats['Runs']['pass'] += 1
            else:
                failed_tests += 1
                test_stats['Runs']['fail'] += 1
                seq_passed = False
            
            result = tester.longest_run_of_ones_test(seq)
            f.write(f"\n{result['test_name']}\n")
            f.write(f"  Статистика: {result['statistic']:.6f}\n")
            f.write(f"  P-value: {result['p_value']:.6f}\n")
            f.write(f"  Результат: {result['result']}\n")
            f.write(f"  Максимальные серии в блоках: {result['max_runs_per_block']}\n")
            f.write(f"  Распределение по категориям: {result['block_counts']}\n")
            
            total_tests += 1
            if result['result'] == 'PASS':
                passed_tests += 1
                test_stats['Longest Run']['pass'] += 1
            else:
                failed_tests += 1
                test_stats['Longest Run']['fail'] += 1
                seq_passed = False
            
            result = tester.additional_test_serial(seq, m=2)
            f.write(f"\n{result['test_name']} [ОПЦИОНАЛЬНО]\n")
            f.write(f"  Статистика: {result['statistic']:.6f}\n")
            f.write(f"  P-value: {result['p_value']:.6f}\n")
            f.write(f"  Результат: {result['result']}\n")
            
            total_tests += 1
            if result['result'] == 'PASS':
                passed_tests += 1
                test_stats['Serial']['pass'] += 1
            else:
                failed_tests += 1
                test_stats['Serial']['fail'] += 1
            
            if seq_passed:
                passed_sequences.append(idx)
            else:
                failed_sequences.append(idx)
            
        f.write("\n")
        f.write("ВЫВОДЫ ПО РЕЗУЛЬТАТАМ ТЕСТИРОВАНИЯ (АВТОМАТИЧЕСКИ)\n")
        
        f.write("1. ОБЩАЯ СТАТИСТИКА:\n")
        f.write(f"   Всего последовательностей: {total_sequences}\n")
        f.write(f"   Прошли все тесты: {len(passed_sequences)} ({len(passed_sequences)/total_sequences*100:.1f}%)\n")
        f.write(f"   Не прошли тесты: {len(failed_sequences)} ({len(failed_sequences)/total_sequences*100:.1f}%)\n")
        f.write(f"   Всего тестов выполнено: {total_tests}\n")
        f.write(f"   Успешных тестов: {passed_tests} ({passed_tests/total_tests*100:.1f}%)\n")
        f.write(f"   Неуспешных тестов: {failed_tests} ({failed_tests/total_tests*100:.1f}%)\n\n")
        
        f.write("2. СТАТИСТИКА ПО ТЕСТАМ:\n")
        for test_name, stats in test_stats.items():
            total = stats['pass'] + stats['fail']
            pass_rate = stats['pass']/total*100 if total > 0 else 0
            f.write(f"   {test_name}: {stats['pass']}/{total} PASS ({pass_rate:.1f}%)\n")
        f.write("\n")
        
        f.write("3. ДЕТАЛИЗАЦИЯ ПО ПОСЛЕДОВАТЕЛЬНОСТЯМ:\n")
        f.write(f"   Прошли все тесты: {passed_sequences if passed_sequences else 'нет'}\n")
        f.write(f"   Не прошли тесты: {failed_sequences if failed_sequences else 'нет'}\n\n")
        
        f.write("4. ОЦЕНКА КАЧЕСТВА ГЕНЕРАТОРОВ:\n")
        success_rate = len(passed_sequences)/total_sequences*100
        if success_rate >= 80:
            f.write("   Отличное качество генераторов\n")
        elif success_rate >= 50:
            f.write("   Удовлетворительное качество генераторов\n")
        else:
            f.write("   Низкое качество генераторов\n")
        f.write("\n")
        
    print(f"Результаты сохранены в {output_file}")
    print(f"Пройдено тестов: {passed_tests}/{total_tests} ({passed_tests/total_tests*100:.1f}%)")
    print(f"Последовательностей прошло все тесты: {len(passed_sequences)}/{total_sequences}")


if __name__ == "__main__":
    run_all_tests(sequences)