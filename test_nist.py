import math
import os
from scipy.special import gammaincc

def read_constants():
    """Читает числа из constants.txt и возвращает список."""
    values = []
    with open('constants.txt', 'r') as f:
        for line in f:
            line = line.split('#')[0].strip()
            if line:
                values.append(float(line))
    return values

vals = read_constants()
LENGTH = int(vals[0])
BLOCK_SIZE = int(vals[1])
PI = vals[2:6]
THRESHOLD = vals[6]

class NISTTests:
    """Реализует три статистических теста NIST для случайных последовательностей."""
    
    def __init__(self, bits):
        """Инициализирует тестер с битовой строкой."""
        self.bits = bits
        self.n = len(bits)
    
    def frequency_test(self):
        """Выполняет частотный побитовый тест."""
        s = sum(1 if b == '1' else -1 for b in self.bits)
        s_obs = abs(s) / math.sqrt(self.n)
        return math.erfc(s_obs / math.sqrt(2))
    
    def runs_test(self):
        """Выполняет тест на одинаковые подряд идущие биты."""
        ones = self.bits.count('1')
        pi = ones / self.n
        if abs(pi - 0.5) >= 2.0 / math.sqrt(self.n):
            return 0.0
        v = 0
        for i in range(self.n - 1):
            if self.bits[i] != self.bits[i + 1]:
                v += 1
        numerator = abs(v - 2 * self.n * pi * (1 - pi))
        denominator = 2 * math.sqrt(2 * self.n) * pi * (1 - pi)
        return math.erfc(numerator / denominator)
    
    def longest_run_test(self):
        """
        Тест на самую длинную последовательность единиц в блоке
        """
        data_parts = [self.bits[i:i+8] for i in range(0, 128, 8)]
        len_parts = []
        
        for i in range(len(data_parts)):
            max_len = 0
            current_len = 0
            for j in range(8):
                if data_parts[i][j] == '1':
                    current_len += 1
                    max_len = max(max_len, current_len)
                else:
                    current_len = 0
            len_parts.append(max_len)
        
        len_blocks = [0, 0, 0, 0]
        for i in len_parts:
            if i <= 1:
                len_blocks[0] += 1
            if i == 2:
                len_blocks[1] += 1
            if i == 3:
                len_blocks[2] += 1
            if i >= 4:
                len_blocks[3] += 1
        
        pi_list = [0.2148, 0.3672, 0.2305, 0.1875]
        x = 0
        for i in range(4):
            x += ((len_blocks[i] - 16 * pi_list[i]) ** 2) / (16 * pi_list[i])
        
        p = gammaincc(3/2, x/2)
        return x, p

def main():
    """Загружает последовательности из файлов, тестирует их и сохраняет результаты."""
    os.makedirs('results', exist_ok=True)
    
    files = [
        ('results/sequence_cpp.txt', 'C++'),
        ('results/sequence_java.txt', 'Java'),
        ('results/sequence_python.txt', 'Python')
    ]
    
    results = []
    for filename, name in files:
        try:
            with open(filename, 'r') as f:
                bits = f.read().strip()
                tester = NISTTests(bits)
                p1 = tester.frequency_test()
                p2 = tester.runs_test()
                chi2, p3 = tester.longest_run_test()
                results.append((name, bits, p1, p2, chi2, p3))
                print(f"[OK] {name}")
        except FileNotFoundError:
            print(f"[!] Файл не найден: {filename}")
            continue
    
    with open('results/test_results.txt', 'w', encoding='utf-8') as f:
        f.write("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ NIST\n")
        
        for name, bits, p1, p2, chi2, p3 in results:
            f.write(f"{name}\n")
            f.write(f"{bits}\n")
            f.write(f"Frequency test: {p1:.6f}\n")
            f.write(f"Runs test: {p2:.6f}\n")
            f.write(f"Longest run test: chi2={chi2:.6f}, P={p3:.6f}\n\n")
    
    print("\nГотово. Результаты сохранены в results/test_results.txt")

if __name__ == "__main__":
    main()

