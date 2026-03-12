import math
from scipy.special import gammaincc

def erfc(x):
    """Дополнительная функция ошибок."""
    return math.erfc(x)

def read_sequence(filename):
    """Чтение 128-битной последовательности из файла"""
    sequence = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                # Пропускаем пустые строки
                if not line:
                    continue
                # Читаем все биты из строки
                for ch in line:
                    if ch in ('0', '1'):
                        sequence.append(int(ch))
        
        # Проверяем, что получили ровно 128 бит
        if len(sequence) != 128:
            print(f"ВНИМАНИЕ: Ожидалось 128 бит, получено {len(sequence)} бит")
        
        return sequence
    except FileNotFoundError:
        print(f"Файл {filename} не найден!")
        return None

def find_max_run(sequence):
    """
    Поиск макси длины подряд идущих одинаковых символов
    Возвращает (max_zeros, max_ones)
    """
    if not sequence:
        return 0, 0
    
    max_zeros = 0
    max_ones = 0
    current_zero_run = 0
    current_one_run = 0
    
    for bit in sequence:
        if bit == 0:
            current_zero_run += 1
            current_one_run = 0
            max_zeros = max(max_zeros, current_zero_run)
        else:  # bit == 1
            current_one_run += 1
            current_zero_run = 0
            max_ones = max(max_ones, current_one_run)
    
    return max_zeros, max_ones

def frequency_test(sequence):
    """
    Частотный побитовый тест (Frequency Test)
    Формула из методички:
    S_N = (1/√N) * Σ x_i, где x_i = 1 для '1', -1 для '0'
    P_value = erfc(|S_N| / √2)
    """
    try:
        n = len(sequence)
        # Преобразование 0 -> -1, 1 -> 1
        s = 0
        for bit in sequence:
            s += 1 if bit == 1 else -1

        # Вычисление S_N = (1/√N) * Σ x_i
        s_obs = s / math.sqrt(n)

        # Вычисление P_value = erfc(|S_N| / √2)
        p_value = erfc(abs(s_obs) / math.sqrt(2))
        return p_value
    except Exception as e:
        print(f"Error in frequency_test: {e}")
        return 0.0

def runs_test(sequence):
    """
    Тест на одинаковые подряд идущие биты (Runs Test)
    Формула из методички
    ζ = (1/N) * Σ ε_i
    V_N = Σ r_i, где r_i = 0 если ε_i = ε_{i+1}, 1 если ε_i ≠ ε_{i+1}
    P_value = erfc( |V_N - 2Nζ(1-ζ)| / (2√(2N) ζ(1-ζ)) )
    """
    try:
        n = len(sequence)
        
        # Вычисление ζ (доля единиц)
        ones = 0
        for bit in sequence:
            if bit == 1:
                ones += 1
        pi = ones / n
        
        # Проверка условия применимости теста |ζ - 1/2| < 2/√N
        if abs(pi - 0.5) >= (2 / math.sqrt(n)):
            print(f"Предупреждение: условие применимости теста не выполнено")
            print(f"|ζ - 0.5| = {abs(pi - 0.5):.4f} >= {2/math.sqrt(n):.4f}")
            return 0.0
        # Вычисление V_N - числа знакоперемен (количество смен битов)
        v_obs = 0
        for i in range(n - 1):
            if sequence[i] != sequence[i + 1]:
                v_obs += 1
        
        # Вычисление P-value по формуле
        numerator = abs(v_obs - 2 * n * pi * (1 - pi))
        denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)
        
        if denominator == 0:
            return 0.0
        
        p_value = erfc(numerator / denominator)
        return p_value
    except Exception as e:
        print(f"Error in runs_test: {e}")
        return 0.0

def longest_run_test(sequence):
    """
    Тест на самую длинную последовательность единиц в блоке
    Для N = 128 бит, M = 8
    χ² = Σ (v_i - 16π_i)² / (16π_i)
    P_value = gammaincc(3/2, χ²/2)
    """
    try:
        # Проверяем, что последовательность содержит 128 бит
        if len(sequence) != 128:
            print(f"Ошибка: для теста нужно 128 бит, получено {len(sequence)}")
            return 0.0
        
        counter = [0, 0, 0, 0]  # v₀, v₁, v₂, v₃
        
        for start in range(0, 128, 8):
            current_block = sequence[start:start+8]
            
            max_series = 0
            current_series = 0
            
            for bit in current_block:
                if bit == 1:
                    current_series += 1
                    if current_series > max_series:
                        max_series = current_series
                else:
                    current_series = 0
            
            # Классификация по длине максимальной серии (строго по методичке)
            if max_series <= 1:
                counter[0] += 1
            elif max_series == 2:
                counter[1] += 1
            elif max_series == 3:
                counter[2] += 1
            else:  # max_series >= 4
                counter[3] += 1
        
        print(f"Распределение блоков: v₁={counter[0]}, v₂={counter[1]}, v₃={counter[2]}, v₄={counter[3]}")
        # Теоретические вероятности из методички
        theory = [0.2148, 0.3672, 0.2305, 0.1875]
        
        # Вычисление статистики хихихи-квадрат
        chi_value = 0
        for k in range(3):
            expected = 16 * theory[k]
            chi_value += ((counter[k] - expected) ** 2) / expected
        
        print(f"   X² = {chi_value:.4f}")
        
        # Вычисление P-value с использованием gammaincc из scipy
        p_value = gammaincc(3/2, chi_value / 2)
        return p_value
    except Exception as e:
        print(f"Error in longest_run_test: {e}")
        return 0.0

def test_sequence(filename):
    """Тестирование последовательности из файла"""
    print(f"\n{'='*60}")
    print(f"ТЕСТИРОВАНИЕ ФАЙЛА: {filename}")
    print(f"{'='*60}")
    
    sequence = read_sequence(filename)
    if sequence is None:
        return
    
    n = len(sequence)
    zeros = sequence.count(0)
    ones = sequence.count(1)
    
    print(f"Длина последовательности: {n} бит (должно быть 128)")
    print(f"Количество нулей: {zeros} ({zeros/n*100:.1f}%)")
    print(f"Количество единиц: {ones} ({ones/n*100:.1f}%)")
    
    # Поиск максимальных серий
    max_zeros, max_ones = find_max_run(sequence)
    print(f"\nМАКСИМАЛЬНЫЕ СЕРИИ:")
    print(f"   Максимальная серия нулей: {max_zeros}")
    print(f"   Максимальная серия единиц: {max_ones}")
    
    print(f"\n{'-'*60}")
    print("ТЕСТЫ NIST:")
    print(f"{'-'*60}")
    
    print(f"\n1. ЧАСТОТНЫЙ ПОБИТОВЫЙ ТЕСТ")
    print(f"   Формула: P_value = erfc(|S_N|/√2)")
    p_freq = frequency_test(sequence)
    print(f"   P_value = {p_freq:.6f}")
    print(f"   Результат: {'СЛУЧАЙНАЯ' if p_freq >= 0.01 else 'НЕ СЛУЧАЙНАЯ'}")
    
    print(f"\n2. ТЕСТ НА ОДИНАКОВЫЕ ПОДРЯД ИДУЩИЕ БИТЫ")
    print(f"   Формула: P_value = erfc(|V_N - 2Nζ(1-ζ)| / (2√(2N) ζ(1-ζ)))")
    p_runs = runs_test(sequence)
    if p_runs == 0.0 and abs(sum(sequence)/len(sequence) - 0.5) >= 2/math.sqrt(len(sequence)):
        print(f"   Тест неприменим (слишком большое отклонение доли единиц)")
    else:
        print(f"   P_value = {p_runs:.6f}")
        print(f"   Результат: {'СЛУЧАЙНАЯ' if p_runs >= 0.01 else 'НЕ СЛУЧАЙНАЯ'}")
    
    print(f"\n3. ТЕСТ НА САМУЮ ДЛИННУЮ ПОСЛЕДОВАТЕЛЬНОСТЬ ЕДИНИЦ В БЛОКЕ")
    print(f"   Формула: P_value = gammaincc(3/2, χ²/2)")
    p_long = longest_run_test(sequence)
    print(f"   P_value = {p_long:.6f}")
    print(f"   Результат: {'СЛУЧАЙНАЯ' if p_long >= 0.01 else 'НЕ СЛУЧАЙНАЯ'}")
    
    print(f"\n{'='*60}")
    print("ВЫВОД:")
    if p_freq >= 0.01 and (p_runs >= 0.01 or p_runs == 0.0) and p_long >= 0.01:
        print(" Последовательность прошла все три теста NIST")
        print(" Может считаться случайной с уровнем значимости 0.01")
    else:
        print(" Последовательность НЕ прошла некоторые тесты")
        print(" Не может считаться случайной")
    print(f"{'='*60}")

def main():
    """Главная функция"""
    print(" ПРОГРАММА СТАТИСТИЧЕСКОГО АНАЛИЗА ПСЕВДОСЛУЧАЙНЫХ ПОСЛЕДОВАТЕЛЬНОСТЕЙ")
    print(" Три теста линейки NIST")
    print(" Длина последовательности: 128 бит")
    print(" Критерий: последовательность случайна, если P_value ≥ 0.01")
    

files = ["D:\isb-2026\Lab2_20\sequence_cpp.txt", "D:\isb-2026\Lab2_20\sequence_java.txt"]
        
for file in files:
    try:
        with open(file, 'r') as f:
            test_sequence(file)
    except FileNotFoundError:
        print(f"\nФайл {file} не найден. Сначала запустите генераторы.")
        print("C++: ./generator.cpp")
        print("Java: java Generator")

if __name__ == "__main__":
    main()