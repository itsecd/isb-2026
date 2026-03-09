# -*- coding: utf-8 -*-
import math
from scipy.special import gammaincc

def erfc(x):
    """Дополнительная функция ошибок."""
    return math.erfc(x)

def frequency_test(bits):
    """
    Частотный побитовый тест.
    
    bits: бинарная последовательность
    return: P-value теста
    """
    try:
        n = len(bits)
        s = 0
        for bit in bits:
            s += 1 if bit == '1' else -1
        s_obs = abs(s) / math.sqrt(n)
        p_value = erfc(s_obs / math.sqrt(2))
        return p_value
    except Exception as e:
        print(f"Error in frequency_test: {e}")
        return 0.0

def runs_test(bits):
    """
    Тест на одинаковые подряд идущие биты.
    
    bits: бинарная последовательность
    return: P-value теста или 0.0 если тест неприменим
    """
    try:
        n = len(bits)
        ones = bits.count('1')
        pi = ones / n
        
        if abs(pi - 0.5) >= 2.0 / math.sqrt(n):
            return 0.0
        
        v_obs = 0
        for i in range(n - 1):
            if bits[i] != bits[i + 1]:
                v_obs += 1
        
        numerator = abs(v_obs - 2.0 * n * pi * (1.0 - pi))
        denominator = 2.0 * math.sqrt(2.0 * n) * pi * (1.0 - pi)
        p_value = erfc(numerator / denominator)
        return p_value
    except Exception as e:
        print(f"Error in runs_test: {e}")
        return 0.0

def longest_run_test(bits):
    """
    Тест на самую длинную последовательность единиц в блоке.
    bits: бинарная последовательность
    return: P-value теста
    """
    try:
        v = [0]*4
        temp = 0
        m = 0
        k = 0

        for i in bits:
            if i == '1':
                temp += 1
            else:
                m = max(m, temp)
                temp = 0
            k += 1

            if k == 8:
                if m <= 1:
                    v[0] += 1
                elif m == 2:
                    v[1] += 1
                elif m == 3:
                    v[2] += 1
                else:
                    v[3] += 1
                m = k = temp = 0

        p = [0.2148, 0.3672, 0.2305, 0.1875]
        chi_sq = 0.0

        for i in range(4):
            chi_sq += ((v[i] - 16 * p[i]) ** 2) / (16 * p[i])

        p_value = gammaincc(3/2, chi_sq/2)
        return p_value
    except Exception as e:
        print(f"Error in longest_run_test: {e}")
        return 0.0

def read_sequence(filename):
    """
    Читает последовательность из файла.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            bits = f.read().strip().replace(' ', '').replace('\n', '')
        return bits
    except FileNotFoundError:
        print(f"File {filename} not found")
        return ""
    except Exception as e:
        print(f"Error reading the file {filename}: {e}")
        return ""

def main():
    """Основная функция."""
    files = ["cpp_posled.txt", "java_posled.txt", "python_posled.txt"]
    
    try:
        with open("nist_results.txt", "w", encoding="utf-8") as result_file:
            result_file.write("РЕЗУЛЬТАТЫ ТЕСТОВ NIST\n\n")
            
            for filename in files:
                print(f"\nОбработка файла: {filename}")
                bits = read_sequence(filename)
                
                if not bits:
                    result_file.write(f"Файл {filename} не обработан\n\n")
                    continue
                
                if len(bits) != 128:
                    msg = f"{filename}: длина {len(bits)} (нужно 128)"
                    print(msg)
                    result_file.write(msg + "\n\n")
                    continue
                
                result_file.write(f"Файл: {filename}\n")
                
                p1 = frequency_test(bits)
                status1 = "ПРОЙДЕН" if p1 >= 0.01 else "НЕ ПРОЙДЕН"
                line1 = f"1. Частотный тест: P-value = {p1:.6f} -> {status1}"
                print(line1)
                result_file.write(line1 + "\n")
                
                p2 = runs_test(bits)
                if p2 == 0.0:
                    line2 = "2. Тест на последовательности: тест неприменим"
                    print(line2)
                    result_file.write(line2 + "\n")
                else:
                    status2 = "ПРОЙДЕН" if p2 >= 0.01 else "НЕ ПРОЙДЕН"
                    line2 = f"2. Тест на последовательности: P-value = {p2:.6f} -> {status2}"
                    print(line2)
                    result_file.write(line2 + "\n")
                
                p3 = longest_run_test(bits)
                status3 = "ПРОЙДЕН" if p3 >= 0.01 else "НЕ ПРОЙДЕН"
                line3 = f"3. Тест на длинную серию: P-value = {p3:.6f} -> {status3}"
                print(line3)
                result_file.write(line3 + "\n\n")
            
            print("\nРезультаты сохранены в nist_results.txt")
    
    except Exception as e:
        print(f"Ошибка при записи файла результатов: {e}")

if __name__ == "__main__":
    main()