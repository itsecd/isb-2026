import math
import sys
import datetime

def frequency_test(bit_string):
    """
    Частотный побитовый тест
    """
    n = len(bit_string)
    sum_x = 0
    
    for bit in bit_string:
        sum_x += 1 if bit == '1' else -1
    
    s_obs = abs(sum_x) / math.sqrt(n)
    p_value = math.erfc(s_obs / math.sqrt(2))
    
    return p_value

def runs_test(bit_string):
    """
    Тест на одинаковые подряд идущие биты 
    """
    n = len(bit_string)
    
    ones = bit_string.count('1')
    pi = ones / n
    
    zeros = bit_string.count('0')
    
    v_n = 0
    for i in range(n - 1):
        if bit_string[i] != bit_string[i + 1]:
            v_n = v_n + 1
    
    condition = abs(pi - 0.5) < (2 / math.sqrt(n))
    
    if condition:
        numerator = abs(v_n - 2 * n * pi * (1 - pi))
        denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)
        p_value = math.erfc(numerator / denominator)
    else:
        p_value = 0.0
    
    return p_value

def incomplete_gamma_lower(a, x, epsilon=1e-10, max_iter=1000):
    """
    Нижняя неполная гамма-функция через ряд
    """
    if x < 0:
        return 0.0
    
    term = 1.0 / a
    result = term
    n = 1
    
    while n < max_iter:
        term *= x / (a + n)
        result += term
        if term < epsilon:
            break
        n += 1
    
    return (x ** a) * math.exp(-x) * result

def longest_run_test(bit_string):
    """
    Тест на самую длинную последовательность единиц в блоке
    """
    n = len(bit_string)
    M = 8  
    N = n // M 
    
    if N < 3:
        return 0.0
    
    pi = [0.2148, 0.3672, 0.2305, 0.1875]
    v = [0, 0, 0, 0]
    
    for i in range(N):
        block = bit_string[i*M:(i+1)*M]
        
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
    
    chi_square = 0
    for i in range(4):
        expected = N * pi[i]
        chi_square += ((v[i] - expected) ** 2) / expected
    
    a = 1.5
    x = chi_square / 2
    
    gamma_lower = incomplete_gamma_lower(a, x)
    gamma_full = math.gamma(a)
    p_value = 1 - (gamma_lower / gamma_full)
    
    return p_value

def save_results_to_file(results, filename="test_results.txt"):
    """
    Сохраняет результаты тестирования в файл
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("РЕЗУЛЬТАТЫ СТАТИСТИЧЕСКОГО ТЕСТИРОВАНИЯ ПСЕВДОСЛУЧАЙНЫХ ПОСЛЕДОВАТЕЛЬНОСТЕЙ\n")
        f.write(f"Дата и время тестирования: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 70 + "\n\n")
        
        for file_name, res in results.items():
            if res:
                f.write(f"\n{'=' * 60}\n")
                f.write(f"Файл: {file_name}\n")
                f.write(f"{'=' * 60}\n")
                
                f.write(f"Последовательность (первые 50 бит): {res['sequence'][:50]}...\n")
                f.write(f"Полная длина: {len(res['sequence'])} бит\n\n")
                
                f.write("1. ЧАСТОТНЫЙ ПОБИТОВЫЙ ТЕСТ\n")
                f.write(f"   P-value = {res['frequency']:.6f}\n")
                f.write(f"   Статус: {'ПРОЙДЕН' if res['frequency'] >= 0.01 else 'НЕ ПРОЙДЕН'}\n")
                f.write(f"   {'' if res['frequency'] >= 0.01 else '!'} Критерий: P-value >= 0.01\n\n")
                
                f.write("2. ТЕСТ НА ОДИНАКОВЫЕ ПОДРЯД ИДУЩИЕ БИТЫ (ТЕСТ НА СЕРИИ)\n")
                f.write(f"   P-value = {res['runs']:.6f}\n")
                f.write(f"   Статус: {'ПРОЙДЕН' if res['runs'] >= 0.01 else 'НЕ ПРОЙДЕН'}\n")
                f.write(f"   {'' if res['runs'] >= 0.01 else '!'} Критерий: P-value >= 0.01\n\n")
                
                f.write("3. ТЕСТ НА САМУЮ ДЛИННУЮ ПОСЛЕДОВАТЕЛЬНОСТЬ ЕДИНИЦ В БЛОКЕ\n")
                f.write(f"   P-value = {res['longest_run']:.6f}\n")
                f.write(f"   Статус: {'ПРОЙДЕН' if res['longest_run'] >= 0.01 else 'НЕ ПРОЙДЕН'}\n")
                f.write(f"   {'' if res['longest_run'] >= 0.01 else '!'} Критерий: P-value >= 0.01\n\n")
                
                all_passed = (res['frequency'] >= 0.01 and 
                             res['runs'] >= 0.01 and 
                             res['longest_run'] >= 0.01)
                
                f.write(f"ИТОГОВЫЙ ВЕРДИКТ: {'СЛУЧАЙНАЯ' if all_passed else 'НЕ СЛУЧАЙНАЯ'}\n")
                if all_passed:
                    f.write(f" Последовательность успешно прошла все три теста NIST\n")
                else:
                    f.write(f" Последовательность НЕ прошла один или несколько тестов\n")
        
        f.write("\n\n")
        f.write("=" * 80 + "\n")
        f.write("СВОДНАЯ ТАБЛИЦА РЕЗУЛЬТАТОВ\n")
        f.write("=" * 80 + "\n")
        f.write(f"{'Файл':<25} {'Частотный':<15} {'Серии':<15} {'Длинные серии':<15} {'Статус'}\n")
        f.write("-" * 80 + "\n")
        
        for file_name, res in results.items():
            if res:
                status = " Случайная" if (res['frequency']>=0.01 and res['runs']>=0.01 and res['longest_run']>=0.01) else " Не случайная"
                f.write(f"{file_name:<25} {res['frequency']:<15.6f} {res['runs']:<15.6f} {res['longest_run']:<15.6f} {status}\n")
        
        f.write("=" * 80 + "\n")
        
    
    print(f"\nРезультаты сохранены в файл: {filename}")

def test_sequence_from_file(filename):
    """
    Тестирование последовательности из файла
    """
    try:
        with open(filename, 'r') as f:
            sequence = f.read().strip()
        
        if len(sequence) < 128:
            print(f"Внимание: ожидалось 128 бит, получено {len(sequence)}")
        
        print(f"\nТестирование файла: {filename}")
        print(f"Последовательность: {sequence[:50]}...")
        print(f"Длина: {len(sequence)} бит")
        print("-" * 50)
        
        p1 = frequency_test(sequence)
        print(f"1. Частотный тест:")
        print(f"   P-value = {p1:.6f}")
        print(f"   Результат: {'ПРОЙДЕН' if p1 >= 0.01 else 'НЕ ПРОЙДЕН'}")
        
        p2 = runs_test(sequence)
        print(f"\n2. Тест на серии:")
        print(f"   P-value = {p2:.6f}")
        print(f"   Результат: {'ПРОЙДЕН' if p2 >= 0.01 else 'НЕ ПРОЙДЕН'}")
        
        p3 = longest_run_test(sequence)
        print(f"\n3. Тест на самую длинную последовательность единиц:")
        print(f"   P-value = {p3:.6f}")
        print(f"   Результат: {'ПРОЙДЕН' if p3 >= 0.01 else 'НЕ ПРОЙДЕН'}")
        
        print("\n" + "=" * 50)
        print(f"ИТОГ: Последовательность {'СЛУЧАЙНАЯ' if (p1>=0.01 and p2>=0.01 and p3>=0.01) else 'НЕ СЛУЧАЙНАЯ'}")
        
        return {
            'frequency': p1,
            'runs': p2,
            'longest_run': p3,
            'sequence': sequence
        }
        
    except FileNotFoundError:
        print(f"Ошибка: Файл {filename} не найден")
        return None
    except Exception as e:
        print(f"Ошибка при обработке файла: {e}")
        return None

def main():
    files = ['sequence_cpp.txt', 'sequence_java.txt', 'sequence_python.txt']
    results = {}
    
    for file in files:
        results[file] = test_sequence_from_file(file)
    
    save_results_to_file(results)
    print("\n" + "=" * 60)
    print("СВОДНАЯ ТАБЛИЦА РЕЗУЛЬТАТОВ")
    print("=" * 60)
    print(f"{'Файл':<25} {'Частотный':<15} {'Серии':<15} {'Длинные серии':<15} {'Статус'}")
    print("-" * 60)
    
    for file, res in results.items():
        if res:
            status = " Случайная" if (res['frequency']>=0.01 and res['runs']>=0.01 and res['longest_run']>=0.01) else " Не случайная"
            print(f"{file:<25} {res['frequency']:<15.6f} {res['runs']:<15.6f} {res['longest_run']:<15.6f} {status}")
    
    print("=" * 60)

if __name__ == "__main__":
    main()