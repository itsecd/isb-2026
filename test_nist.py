import math
import os

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
        """Выполняет тест на самую длинную последовательность единиц в блоке."""
        num_blocks = self.n // BLOCK_SIZE
        blocks = [self.bits[i*BLOCK_SIZE:(i+1)*BLOCK_SIZE] for i in range(num_blocks)]
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
        chi2 = 0
        for i in range(4):
            expected = num_blocks * PI[i]
            chi2 += (v[i] - expected) ** 2 / expected
        p = math.exp(-chi2 / 2)
        return chi2, p

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
        except FileNotFoundError:
            continue
    
    with open('results/test_results.txt', 'w') as f:
        for name, bits, p1, p2, chi2, p3 in results:
            f.write(f"{name}\n")
            f.write(f"{bits}\n")
            f.write(f"{p1:.6f}\n")
            f.write(f"{p2:.6f}\n")
            f.write(f"{chi2:.6f} {p3:.6f}\n\n")

if __name__ == "__main__":
    main()