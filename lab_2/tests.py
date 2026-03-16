import argparse
import math 
import os
from scipy.special import gammaincc


def parse() -> argparse.Namespace:
    """Данная функция получает аргументы из командной строки"""
    parser = argparse.ArgumentParser()

    parser.add_argument('--folder_path', 
                        '-fp', 
                        help='Пусть к директории с последовательностями')
    
    parser.add_argument('--test_results', 
                        '-tr', 
                        help='Название файла с результатами исследований')

    return parser.parse_args()


def read_sequence(path: str) -> str:
    """Чтение файла с последовательностью"""
    with open(path, 'r', encoding='utf-8') as file:
        return file.read().strip()


def freq_test(sequence: str) -> float:
    """Частотный побитовый тест"""
    n = len(sequence)
    s_n = abs(sum([int(sequence[i]) if int(sequence[i]) == 1 else -1 for i in range(n)]) * (1 / math.sqrt(n)))
    p_val = math.erfc(s_n / math.sqrt(2))
    return p_val
    

def same_bits_test(sequence: str) -> float:
    """Тест на одинаковые подряд идущие биты"""
    n = len(sequence)
    ones_ratio = sequence.count("1") / n

    if abs(ones_ratio - 0.5) >= (2 / math.sqrt(n)):
        return 0
    
    v_n = sum([1 if sequence[i] != sequence[i + 1] else 0 for i in range(n - 1)])
    
    numerator = abs(v_n - 2 * n * ones_ratio * (1 - ones_ratio))
    denominator = 2 * math.sqrt(2 * n) * ones_ratio * (1 - ones_ratio)
    p_val = math.erfc(numerator / denominator)

    return p_val


def longest_test(sequence: str) -> float:
    """Тест на самую длинную последовательность единиц в блоке"""
    n = len(sequence)
    m = 8
    p = [0.2148, 0.3672, 0.2305, 0.1875]
    v = [0, 0, 0, 0]

    for i in range(0, n - m, m):
        block = sequence[i:i+m]
        max_len = 0 # максимальная длина подряд идущих единиц 
        temp = 0

        for bit in block:
            if bit == "1":
                temp += 1
                if temp > max_len:
                    max_len = temp
            else:
                temp = 0

        if max_len <= 1:
            v[0] += 1
        elif max_len == 2:
            v[1] += 1
        elif max_len == 3:
            v[2] += 1
        else:
            v[3] += 1
        
    chi_square = 0

    for i in range(len(v)):
        numerator = math.pow((v[i] - 16 * p[i]), 2)
        denominator = 16 * p[i]
        chi_square += numerator / denominator
    
    p_val = gammaincc(3 / 2, chi_square / 2)

    return p_val


def check_p_val(p_val: float) -> str:
    """Проверяет значение p_val"""
    if p_val >= 0.01:
        return "+"
    return "-"


def get_analysis(sequence: str) -> str:
    """Функция анализирует значение p переданной последовательности"""
    p_freq = freq_test(sequence)
    p_same_bits = same_bits_test(sequence)
    p_longest = longest_test(sequence)

    test = (
        f"Последовательность: {sequence}\n"
        f"Частотный анализ: {p_freq} -> [{check_p_val(p_freq)}]\n"
        f"Тест серий: {p_same_bits} -> [{check_p_val(p_same_bits)}]\n"
        f"Длинная серия единиц: {p_longest} -> [{check_p_val(p_longest)}]\n\n"
    )
    
    return test


def main() -> None:
    folder_path, test_results = parse().folder_path, parse().test_results
    sequences = [f"{folder_path}/{s}" for s in ["cpp_seq.txt", "java_seq.txt", "py_seq.txt"]]
    results = ""

    for file in sequences:
        seq = read_sequence(file)
        results += get_analysis(seq)

    with open(test_results, "w", encoding="utf-8") as file:
        file.write(results)
    

if __name__ == "__main__":
    main()