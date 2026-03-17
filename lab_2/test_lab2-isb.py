import math
import path_file as fp
from scipy import stats

def load_sequence(filename):
    """Загружает битовую последовательность из файла."""
    with open(filename, 'r') as f:
        return f.read().strip()

def monobit_test(seq):
    """Частотный тест. Проверяет соотношение единиц и нулей в последовательности."""
    n = len(seq)
    s_obs = abs(2 * seq.count('1') - n) / math.sqrt(n)
    p_value = math.erfc(s_obs / math.sqrt(2))
    return p_value >= 0.01, p_value

def runs_test(seq):
    """Тест на одинаковые подряд идущие биты.
    Считает количество подряд идущих единиц и нулей"""
    n = len(seq)
    
    ones = sum(1 for b in seq if b == '1')
    pi = ones / n
    
    # Проверяем, что последовательность сбалансирована
    if abs(pi - 0.5) >= 2 / math.sqrt(n):
        return False, 0.0
    
    # Считаем количество переходов (runs)
    v = 1.0  # Начинаем с 1, т.к. первая серия уже есть
    for i in range(1, n):
        if seq[i] != seq[i-1]:
            v += 1
    
    # Ожидаемое количество серий и стандартное отклонение
    expected = 2 * n * pi * (1 - pi) + 1
    variance = 2 * n * pi * (1 - pi) * (2 * n * pi * (1 - pi) - 1) / (n - 1)
    
    if variance <= 0:
        return False, 0.0
    
    # Вычисляем p-value через нормальное распределение
    z_obs = abs(v - expected) / math.sqrt(variance)
    p_value = math.erfc(z_obs / math.sqrt(2))
    
    return p_value >= 0.01, p_value

def longest_run_test(seq):
    """Тест на самую длинную последовательность единиц в блоке."""
    n = len(seq)
    
    BLOCK_SIZE = 8
    # Ожидаемые вероятности для M=8 (из NIST SP 800-22)
    PI = [0.21484375, 0.36718750, 0.23046875, 0.18750000]
    
    num_blocks = n // BLOCK_SIZE
    
    if num_blocks < 3:
        return True, 1.0
    
    # Разбиваем на блоки
    blocks = [
        seq[i*BLOCK_SIZE:(i+1)*BLOCK_SIZE] 
        for i in range(num_blocks)
    ]
    
    # Подсчитываем распределение максимальных длин серий
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
        
        # Классифицируем блок по максимальной длине серии
        if max_run <= 1:
            v[0] += 1
        elif max_run == 2:
            v[1] += 1
        elif max_run == 3:
            v[2] += 1
        else:  # max_run >= 4
            v[3] += 1
    
    # Вычисляем хи-квадрат статистику
    chi2 = 0.0
    for i in range(4):
        expected = num_blocks * PI[i]
        if expected > 0:
            chi2 += (v[i] - expected) ** 2 / expected
    
    # Используем sf (survival function) вместо 1 - cdf для численной стабильности
    p_value = stats.chi2.sf(chi2, 3)
    
    # Гарантируем, что p_value в допустимом диапазоне [0, 1]
    # Это не костыль, а защита от численных ошибок floating point
    if p_value < 0:
        p_value = 0.0
    elif p_value > 1:
        p_value = 1.0
    
    return p_value >= 0.01, p_value

def test_file(filename):
    """Запускает все три теста для одного файла."""
    seq = load_sequence(filename)
    
    # Валидация последовательности
    if not all(c in '01' for c in seq):
        raise ValueError(f"File {filename} contains non-binary characters")
    
    if len(seq) < 100:  # Минимальная длина для статистических тестов
        raise ValueError(f"File {filename} sequence too short (min 100 bits)")
    
    tests = [
        ("Monobit Test", monobit_test(seq)),
        ("Runs Test", runs_test(seq)),
        ("Longest Run Test", longest_run_test(seq)),
    ]
    
    return tests

def save_results_to_file(all_results, output_filename):
    """Сохраняет результаты всех тестов в файл отчёта."""
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write("ОТЧЕТ О СТАТИСТИЧЕСКИХ ТЕСТАХ NIST\n")
        f.write("=" * 60 + "\n\n")
        
        total_tests = 0
        passed_tests = 0
        
        for filename, tests in all_results:
            f.write(f"ФАЙЛ: {filename}\n")
            f.write("-" * 40 + "\n")
            
            file_passed = 0
            for test_name, (passed, value) in tests:
                total_tests += 1
                if passed:
                    passed_tests += 1
                    file_passed += 1
                
                status = "УДАЧНО" if passed else "НЕУДАЧНО"
                f.write(f"  {test_name:<30} P-value: {value:<12.6f} [{status}]\n")
            
            f.write(f"  Результат файла: {file_passed}/{len(tests)} тестов пройдено\n\n")
        
        f.write("=" * 60 + "\n")
        f.write("ИТОГ\n")
        f.write("=" * 60 + "\n")
        f.write(f"Количество протестированных файлов: {len(all_results)}\n")
        f.write(f"Количество успешных тестов: {passed_tests}/{total_tests}\n")
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        f.write(f"Показатель успеха: {success_rate:.1f}%\n")
        
        if passed_tests == total_tests:
            f.write("\n✓ Все тесты пройдены успешно - последовательности случайны\n")
        else:
            f.write(f"\n✗ {total_tests - passed_tests} тестов не пройдены\n")
    
    return output_filename

def main():
    """Основная функция. Тестирует файлы с последовательностями и сохраняет результат."""
    
    all_results = []
    
    for filename in fp.TEST_FILES:
        try:
            print(f"Тестирование {filename}...")
            tests = test_file(filename)
            all_results.append((filename, tests))
            
            # Вывод результатов в консоль
            for test_name, (passed, value) in tests:
                status = "PASS" if passed else "FAIL"
                print(f"  {test_name}: {status} (p={value:.6f})")
            
        except FileNotFoundError:
            print(f"\n✗ Файл '{filename}' не найден.")
        except Exception as e:
            print(f"\n✗ Ошибка тестирования '{filename}': {str(e)}")
    
    if all_results:
        output_file = save_results_to_file(all_results, fp.OUTPUT_FILE)
        print(f"\n✓ Результаты сохранены в: {output_file}\n")

if __name__ == "__main__":
    main()
