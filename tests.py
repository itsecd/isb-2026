import math
from scipy.special import erfc, gammaincc

class NISTTests:
    def __init__(self):
        self.sequences = {}
    def load_sequence_from_file(self, filename):
        """Загрузка последовательности из файла"""
        try:
            with open(filename, 'r') as f:
                sequence_str = f.read().strip()
                return [int(bit) for bit in sequence_str if bit in '01']
        except FileNotFoundError:
            print(f"Файл {filename} не найден")
            return None
    
    def frequency_test(self, sequence):
        """
        Тест 2.1: Частотный побитовый тест
        Проверяет, близка ли доля единиц к 0.5
        """
        n = len(sequence)
        if n == 0:
            return 0, 0, 0
        
        ones = sum(sequence)
        s_obs = abs(ones - (n - ones)) / math.sqrt(n)
        p_value = erfc(s_obs / math.sqrt(2))
        
        return p_value, ones, n - ones
    
    def runs_test(self, sequence):
        """
        Тест 2.2: Тест на одинаковые подряд идущие биты
        Проверяет, соответствует ли количество серий случайной последовательности
        """
        n = len(sequence)
        if n == 0:
            return 0.0, 0, {}

        ones_count = sum(sequence)
        ones_probability = ones_count / n
    
        # Добавлена проверка предварительного условия
        if abs(ones_probability - 0.5) >= (2 / math.sqrt(n)):
            return 0.0, 0, {"error": "Предварительное условие не выполнено"}

        transitions_count = 0
        for i in range(n - 1):
            if sequence[i] != sequence[i + 1]:
                transitions_count += 1
    
        numerator = abs(transitions_count - 2 * n * ones_probability * (1 - ones_probability))
        denominator = 2 * math.sqrt(2 * n) * ones_probability * (1 - ones_probability)
    
        if denominator == 0:
            return 0.0, transitions_count, {"ones_prob": ones_probability}
    
        p_value = math.erfc(numerator / denominator)    

        runs_info = {
            "transitions": transitions_count,
            "ones_probability": ones_probability,
            "expected_transitions": 2 * n * ones_probability * (1 - ones_probability)
        }

        return p_value, transitions_count, runs_info
    
    
    def longest_run_test(self, sequence, block_size=8):
        """
        Тест 2.3: Тест на самую длинную последовательность единиц в блоке
        Проверяет распределение максимальных длин серий единиц в блоках
        """
        n = len(sequence)
        if n < block_size:
            return 0, {}, "Последовательность слишком короткая"
        
        num_blocks = n // block_size
        blocks = [sequence[i*block_size:(i+1)*block_size] for i in range(num_blocks)]
        
        max_runs = []
        for block in blocks:
            max_run = 0
            current_run = 0
            for bit in block:
                if bit == 1:
                    current_run += 1
                    max_run = max(max_run, current_run)
                else:
                    current_run = 0
            max_runs.append(max_run)
        
        categories = {1: 0, 2: 0, 3: 0, 4: 0}
        for run in max_runs:
            if run <= 1:
                categories[1] += 1
            elif run == 2:
                categories[2] += 1
            elif run == 3:
                categories[3] += 1
            else:  # run >= 4
                categories[4] += 1
        
        expected_probs = {1: 0.2148, 2: 0.3672, 3: 0.2305, 4: 0.1875}
        
        chi_square = 0
        for i in range(1, 5):
            expected = expected_probs[i] * num_blocks
            observed = categories[i]
            chi_square += ((observed - expected) ** 2) / expected
        
        p_value = gammaincc(3/2, chi_square/2)
        
        
        return p_value, categories, chi_square
    
    def test_all_sequences(self):
        for lang in ["java", "cpp"]:
            filename = f"{lang}_sequence.txt"
            seq = self.load_sequence_from_file(filename)
            if seq:
                self.sequences[lang] = seq
                print(f"Загружена последовательность из {filename}")
        
        results = {}
        
        for lang, sequence in self.sequences.items():
            # Тест 2.1
            p_val_freq, ones, zeros = self.frequency_test(sequence)
            
            # Тест 2.2
            p_val_runs, runs, info = self.runs_test(sequence)
        
            # Тест 2.3
            p_val_long, categories, chi2 = self.longest_run_test(sequence)
            
            results[lang] = {
                'frequency': p_val_freq,
                'runs': p_val_runs,
                'longest': p_val_long
            }
        
        return results
    
    def generate_report(self, results):
        report = []
        report.append("="*70)
        report.append("ОТЧЕТ ПО ТЕСТИРОВАНИЮ СЛУЧАЙНЫХ ПОСЛЕДОВАТЕЛЬНОСТЕЙ")
        report.append("="*70)
        report.append(f"{'Язык':<10} {'Частотный':<15} {'Серии':<15} {'Макс. серия':<15}")
        
        for lang in results:
            report.append(f"{lang.upper():<10} {results[lang]['frequency']:<15.6f} "
                         f"{results[lang]['runs']:<15.6f} {results[lang]['longest']:<15.6f}")
        
        
        with open("nist_test_report.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(report))
        

def main():
    tester = NISTTests()
    results = tester.test_all_sequences()
    tester.generate_report(results)

if __name__ == "__main__":
    main()