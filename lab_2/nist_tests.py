import math
from scipy.special import gammaincc
from const import P_VALUE, BLOCK_SIZE, PI, SOURCE_FILES, OUTPUT_FILE


def frequency_test(seq: str) -> float:
    """частотный побитовый тест"""
    n = len(seq)
    ones = seq.count('1')
    zeros = n - ones
    
    s_obs = abs(ones - zeros) / math.sqrt(n)
    p_value = math.erfc(s_obs / math.sqrt(2))
    return p_value


def runs_test(seq: str) -> float:
    """тест на одинаковые подряд биты"""
    n = len(seq)
    ones = seq.count('1')
    ones_ratio = ones / n
    
    if abs(ones_ratio - 0.5) > (2 / math.sqrt(n)):
        return 0.0
    
    runs = seq.count('01') + seq.count('10')
    
    numerator = abs(runs - 2 * n * ones_ratio * (1 - ones_ratio))
    denominator = 2 * math.sqrt(2 * n) * ones_ratio * (1 - ones_ratio)
    
    p_value = math.erfc(numerator / denominator)
    return p_value


def longest_run_test(seq: str) -> float:
    """тест на самую длинную последовательность единиц в блоке"""
    v = [0, 0, 0, 0]
    
    for i in range(len(seq) // BLOCK_SIZE):
        block = seq[BLOCK_SIZE * i: BLOCK_SIZE * i + BLOCK_SIZE]
        
        max_run = 0
        current_run = 0
        for bit in block:
            if bit == '1':
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 0
        
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
        chi_square += ((v[i] - 16 * PI[i]) ** 2) / (16 * PI[i])
    
    p_value = gammaincc(3 / 2, chi_square / 2)
    return p_value


def read_file(filename: str) -> str:
    """чтение последовательности из файла"""
    try:
        with open(filename, encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"Файл {filename} не найден!")
        exit(1)


def main():
    cpp_seq = read_file(SOURCE_FILES[0])
    java_seq = read_file(SOURCE_FILES[1])
    py_seq = read_file(SOURCE_FILES[2])
    
    cpp_results = [
        "C++",
        frequency_test(cpp_seq),
        runs_test(cpp_seq),
        longest_run_test(cpp_seq),
    ]
    
    java_results = [
        "Java",
        frequency_test(java_seq),
        runs_test(java_seq),
        longest_run_test(java_seq),
    ]
    
    python_results = [
        "Python",
        frequency_test(py_seq),
        runs_test(py_seq),
        longest_run_test(py_seq),
    ]
    
    def is_passed(results):
        return "ПРОЙДЕН" if all(p >= P_VALUE for p in results[1:]) else "НЕ ПРОЙДЕН"
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("Язык     | Частотный тест | Тест на серии | Тест на длинные серии | Результат\n")
        f.write("-" * 80 + "\n")
        
        f.write(f"{cpp_results[0]:<8} | {cpp_results[1]:.7f}       | {cpp_results[2]:.7f}      | {cpp_results[3]:.12f}        | {is_passed(cpp_results)}\n")
        f.write(f"{java_results[0]:<8} | {java_results[1]:.7f}       | {java_results[2]:.7f}      | {java_results[3]:.12f}        | {is_passed(java_results)}\n")
        f.write(f"{python_results[0]:<8} | {python_results[1]:.7f}       | {python_results[2]:.7f}      | {python_results[3]:.12f}        | {is_passed(python_results)}\n")
    
    print("\n" + "=" * 60)
    print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print("=" * 60)
    print(f"{'Язык':<8} {'Частотный':<12} {'Серии':<12} {'Длинные серии':<18} Вердикт")
    print("-" * 60)
    print(f"{cpp_results[0]:<8} {cpp_results[1]:.7f}   {cpp_results[2]:.7f}   {cpp_results[3]:.12f}   {is_passed(cpp_results)}")
    print(f"{java_results[0]:<8} {java_results[1]:.7f}   {java_results[2]:.7f}   {java_results[3]:.12f}   {is_passed(java_results)}")
    print(f"{python_results[0]:<8} {python_results[1]:.7f}   {python_results[2]:.7f}   {python_results[3]:.12f}   {is_passed(python_results)}")
    print(f"\nРезультаты сохранены в файл {OUTPUT_FILE}")


if __name__ == "__main__":
    main()