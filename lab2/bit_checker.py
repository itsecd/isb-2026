import math
import argparse
import csv
from scipy.special import gammaincc
from settings import COEFF as ALPHA
import os

class BitTester:
    """Класс для проведения статистических тестов битовых последовательностей."""
    
    def __init__(self, bits):
        self.bits = bits
        self.n = len(bits)
    
    def _frequency(self):
        """Частотный тест."""
        mapped = [1 if b else -1 for b in self.bits]
        abs_sum = abs(sum(mapped))
        observed = abs_sum / math.sqrt(self.n)
        p_value = math.erfc(observed / math.sqrt(2))
        return p_value
    
    def _runs(self):
        """Тест на последовательности одинаковых битов."""
        ones = sum(self.bits)
        proportion = ones / self.n
        if abs(proportion - 0.5) >= 2.0 / math.sqrt(self.n):
            return 0.0
        runs_count = sum(1 for i in range(self.n - 1) if self.bits[i] != self.bits[i+1])
        numerator = abs(runs_count - 2 * self.n * proportion * (1 - proportion))
        denominator = 2 * math.sqrt(2 * self.n) * proportion * (1 - proportion)
        if denominator == 0:
            return 0.0
        p_value = math.erfc(numerator / denominator)
        return p_value
    
    def _longest_run(self, block_size=8):
        """Тест на самую длинную серию единиц в блоке."""
        blocks = self.n // block_size
        if blocks == 0:
            raise ValueError("Недостаточно битов для блочного анализа")
        expected_probs = [0.2148, 0.3672, 0.2305, 0.1875]
        category_counts = [0, 0, 0, 0]
        
        for b in range(blocks):
            block = self.bits[b * block_size : (b + 1) * block_size]
            max_run = 0
            current = 0
            for bit in block:
                if bit == 1:
                    current += 1
                    if current > max_run:
                        max_run = current
                else:
                    current = 0
            if max_run <= 1:
                category_counts[0] += 1
            elif max_run == 2:
                category_counts[1] += 1
            elif max_run == 3:
                category_counts[2] += 1
            else:
                category_counts[3] += 1
        
        chi_square = 0.0
        for i in range(4):
            expected = blocks * expected_probs[i]
            chi_square += (category_counts[i] - expected) ** 2 / expected
        p_value = gammaincc(1.5, chi_square / 2.0)
        return p_value
    
    def run_all(self):
        """Запускает все три теста и возвращает список p-значений."""
        return [
            self._frequency(),
            self._runs(),
            self._longest_run()
        ]


def load_bits_from_file(filepath):
    """Читает файл и возвращает список целых битов."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        return [int(c) for c in content if c in '01']
    except FileNotFoundError:
        print(f"Ошибка: файл {filepath} не найден.")
        return None


def write_csv_result(output_file, source_file, p_values, is_valid):
    """Записывает результат в CSV-файл (разделитель ;). Если файл не существует, добавляет заголовок."""
    file_exists = os.path.isfile(output_file)
    with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        if not file_exists:
            writer.writerow(['Source file', 'Frequency test p-value', 'Runs test p-value', 'Longest run p-value', 'Valid'])
        writer.writerow([source_file, p_values[0], p_values[1], p_values[2], is_valid])

def main():
    parser = argparse.ArgumentParser(description="Анализ битовых последовательностей")
    parser.add_argument("input", help="Имя файла с битами")
    parser.add_argument("output", help="Имя выходного CSV-файла")
    args = parser.parse_args()
    
    bits = load_bits_from_file(args.input)
    if bits is None:
        return
    
    tester = BitTester(bits)
    p_vals = tester.run_all()
    suitable = all(p >= ALPHA for p in p_vals)
    
    write_csv_result(args.output, args.input, p_vals, suitable)
    print(f"Результаты записаны в {args.output}")

if __name__ == "__main__":
    main()