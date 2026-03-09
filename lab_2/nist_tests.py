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
        
        ones_count = sequence.count('1')
        pi = ones_count / n
        
        if abs(pi - 0.5) >= 2 / math.sqrt(n):
            return {
                'test_name': 'Runs Test',
                'statistic': 0,
                'p_value': 0.0,
                'passed': False
            }
        
        runs = 1
        for i in range(1, n):
            if sequence[i] != sequence[i-1]:
                runs += 1
        
        numerator = runs - 2 * n * pi * (1 - pi)
        denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)
        
        if denominator == 0:
            return {
                'test_name': 'Runs Test',
                'statistic': 0,
                'p_value': 0.0,
                'passed': False
            }
        
        s_obs = numerator / denominator
        
        p_value = special.erfc(abs(s_obs) / math.sqrt(2))
        
        return {
            'test_name': 'Runs Test',
            'statistic': s_obs,
            'p_value': p_value,
            'passed': p_value >= 0.01
        }
    
    def longest_run_of_ones_test(self, sequence, block_size=8):
        """
        Тест на самую длинную последовательность единиц в блоке
        (Longest Run of Ones in a Block Test)
        """
        n = len(sequence)
        num_blocks = n // block_size
        
        if num_blocks == 0:
            return {
                'test_name': 'Longest Run of Ones Test',
                'statistic': 0,
                'p_value': 0.0,
                'passed': False
            }
        
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
        
        pi = [0.21484375, 0.3671875, 0.23046875, 0.1875]
        
        chi_squared = 0
        for i in range(4):
            expected = pi[i] * num_blocks
            if expected > 0:
                chi_squared += ((v[i] - expected) ** 2) / expected
        
        p_value = special.gammaincc(3/2, chi_squared/2)
        
        return {
            'test_name': 'Longest Run of Ones Test',
            'statistic': chi_squared,
            'p_value': p_value,
            'passed': p_value >= 0.01,
            'observed': v,
            'expected': [pi[i] * num_blocks for i in range(4)]
        }
    
    def run_all_tests(self, sequence, test_name=""):
        """
        Запуск всех трех тестов для последовательности
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
        print(f"   Result: {'PASS' if result1['passed'] else 'FAIL'}\n")
        
        result2 = self.runs_test(sequence)
        results.append(result2)
        print(f"2. {result2['test_name']}")
        print(f"   Statistic: {result2['statistic']:.6f}")
        print(f"   P-value: {result2['p_value']:.6f}")
        print(f"   Result: {'PASS' if result2['passed'] else 'FAIL'}\n")
        
        result3 = self.longest_run_of_ones_test(sequence)
        results.append(result3)
        print(f"3. {result3['test_name']}")
        print(f"   Statistic: {result3['statistic']:.6f}")
        print(f"   P-value: {result3['p_value']:.6f}")
        print(f"   Observed: {result3.get('observed', 'N/A')}")
        print(f"   Expected: {result3.get('expected', 'N/A')}")
        print(f"   Result: {'PASS' if result3['passed'] else 'FAIL'}\n")
        
        return results


def main():
    sequences = {
        "C++ MT19937": "1011001011010010110100101101001011010010110100101101001011010010110100101101001011010010110100101101001011010010",
        "Java SecureRandom": "01101001101001101001101001101001101001101001101001101001101001101001101001101001101001101001101001101001101001",
        "Custom": "1100101011001010110010101100101011001010110010101100101011001010110010101100101011001010110010101100101011001010"
    }
    
    nist = NISTTests()
    all_results = {}
    
    for name, seq in sequences.items():
        results = nist.run_all_tests(seq, name)
        all_results[name] = results
    
    with open('test_results.txt', 'w') as f:
        f.write("NIST Statistical Test Results\n")
        
        for name, results in all_results.items():
            f.write(f"Sequence: {name}\n")
            for result in results:
                f.write(f"Test: {result['test_name']}\n")
                f.write(f"  Statistic: {result['statistic']:.6f}\n")
                f.write(f"  P-value: {result['p_value']:.6f}\n")
                f.write(f"  Result: {'PASS' if result['passed'] else 'FAIL'}\n\n")
            f.write("\n")
    
    print("\nResults saved to test_results.txt")


if __name__ == "__main__":
    main()
