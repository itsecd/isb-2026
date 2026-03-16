import math
from scipy.special import erfc

def read_sequence(filename):
    """Читает последовательность из файла """
    with open(filename, 'r') as f:
        data = f.read().strip()
    return [int(bit) for bit in data if bit in '01']

def print_result(test_name, p_value, threshold=0.01):
    """Выводит результат теста в читаемом виде"""
    print(f"{test_name}:")
    print(f"  P-value = {p_value:.6f}")
    if p_value >= threshold:
        print(f"  Результат: последовательность случайна (p ≥ {threshold})")
    else:
        print(f"  Результат: последовательность не случайна (p < {threshold})")
    print()


def frequency_test(bits):
    n = len(bits)
    x = [1 if b == 1 else -1 for b in bits]
    s_sum = sum(x)
    s_n = abs(s_sum) / math.sqrt(n)
    p_value = erfc(s_n / math.sqrt(2))
    return p_value


def runs_test(bits):
    n = len(bits)
    ones = sum(bits)
    pi = ones / n
    
    condition = abs(pi - 0.5) < 2 / math.sqrt(n)
    if not condition:
        return 0.0
    
    v_n = 0
    for i in range(n - 1):
        if bits[i] != bits[i + 1]:
            v_n += 1
    
    numerator = abs(v_n - 2 * n * pi * (1 - pi))
    denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)
    
    if denominator == 0:
        return 0.0
    
    p_value = erfc(numerator / denominator)
    return p_value


def longest_run_test_calc_chi2(bits, m=8):
    """
    Тест на самую длинную последовательность единиц в блоке
    Возвращает χ² для последующего ручного расчета P-value
    """
    n = len(bits)
    num_blocks = n // m
    
    if num_blocks == 0:
        return 0.0
    
    max_runs = []
    for i in range(num_blocks):
        block = bits[i*m : (i+1)*m]
        max_run = 0
        current_run = 0
        for bit in block:
            if bit == 1:
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 0
        max_runs.append(max_run)
    
    v1 = sum(1 for r in max_runs if r <= 1)
    v2 = sum(1 for r in max_runs if r == 2)
    v3 = sum(1 for r in max_runs if r == 3)
    v4 = sum(1 for r in max_runs if r >= 4)
    
    pi = [0.2148, 0.3672, 0.2305, 0.1875]
    
    expected = [16 * p for p in pi]
    observed = [v1, v2, v3, v4]
    
    chi_square = 0
    for i in range(4):
        chi_square += (observed[i] - expected[i])**2 / expected[i]
    
    return chi_square, observed, expected


def test_sequence(filename, sequence_name):
    """Тестирует одну последовательность"""
    print(f"Тест послед-ти: {sequence_name}")

    bits = read_sequence(filename)
    print(f"Длина последовательности: {len(bits)} бит")
    print(f"Первые 67: {''.join(map(str, bits[:67]))}...")
    
    p1 = frequency_test(bits)
    print_result("Частотный побитовый тест", p1)
    
    p2 = runs_test(bits)
    print_result("Тест на одинаковые подряд идущие биты", p2)
    
    chi2, observed, expected = longest_run_test_calc_chi2(bits)
    
    print("Тест на самую длинную послед-ть единиц в блоке:")
    print(f"  v1 (≤1): {observed[0]}")
    print(f"  v2 (=2): {observed[1]}")
    print(f"  v3 (=3): {observed[2]}")
    print(f"  v4 (≥4): {observed[3]}")
    print(f"  Ожидаемые значения: {[round(e, 2) for e in expected]}")
    print(f"\n  χ^2 = {chi2:.6f}")
    print("\n    Для получения P-value:")
    print("     1. Перейдите на сайт: https://www.danielsoper.com/statcalc/calculator.aspx?id=34")
    print(f"     2. Введите s = 1.5 (это degrees of freedom/2)")
    print(f"     3. Введите x = {chi2/2:.6f} (это χ²/2)")
    print("     4. Введите полученное P-value в программу")
    
    try:
        p3 = float(input("\n  Введите P-value из калькулятора: "))
        print_result("  Результат теста", p3)
    except:
        print("  P-value не введён. Тест не завершён.")
        p3 = None
    
    return p1, p2, p3, chi2, observed, expected

def main():
    sequences = [
        ("seq_cpp.txt", "C++ генератор"),
        ("seq_java.txt", "Java генератор"),
        ("seq_py.txt", "Python генератор")
    ]
    
    all_results = []
    
    for filename, name in sequences:
        try:
            results = test_sequence(filename, name)
            all_results.append((name, results))
        except FileNotFoundError:
            print(f"\nФайл {filename} не найден.")
        except Exception as e:
            print(f"\nОшибка при обработке {filename}: {e}")
    
    with open("result.txt", "w", encoding="utf-8") as f:
        f.write("Отчет:\n")
        f.write("\n\n")
        
        for name, (p1, p2, p3, chi2, observed, expected) in all_results:
            f.write(f"Генератор: {name}\n")
            f.write("\n")
            
            f.write("Тест 1. Частотный побитовый тест\n")
            f.write(f"  P-value = {p1:.6f}\n")
            f.write(f"  Результат: {'Случайна' if p1 >= 0.01 else 'Предсказуема'}\n\n")
            
            f.write("Тест 2. Тест на одинаковые подряд идущие биты\n")
            f.write(f"  P-value = {p2:.6f}\n")
            f.write(f"  Результат: {'Случайна' if p2 >= 0.01 else 'Предсказуема'}\n\n")
            
            f.write("Тест 3. Тест на самую длинную последовательность единиц\n")
            f.write(f"  v1 (≤1): {observed[0]}\n")
            f.write(f"  v2 (=2): {observed[1]}\n")
            f.write(f"  v3 (=3): {observed[2]}\n")
            f.write(f"  v4 (≥4): {observed[3]}\n")
            f.write(f"  Ожидаемые значения: {[round(e, 2) for e in expected]}\n")
            f.write(f"  χ² = {chi2:.6f}\n")
            if p3 is not None:
                f.write(f"  P-value = {p3:.6f}\n")
                f.write(f"  Результат: {'Случайна' if p3 >= 0.01 else 'Предсказуема'}\n")
            else:
                f.write(f"  P-value: не введён\n")
            f.write("\n\n")
    
    print("\nОтчёт сохранён в файл 'result.txt'")

if __name__ == "__main__":
    main()