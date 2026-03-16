import argparse
import math 
import os
from scipy.special import erfc, gammainc


def parse() -> argparse.Namespace:
    """Данная функция получает аргументы из командной строки"""
    parser = argparse.ArgumentParser()

    parser.add_argument('--folder_path', 
                        '-fp', 
                        help='Пусть к директории с последовательностями')
    
    return parser.parse_args()


def read_sequence(path: str) -> str:
    """Чтение файла с последовательностью"""
    with open(path, 'r', encoding='utf-8') as file:
        return file.read().strip()


def freq_test(sequence: str) -> float:
    """Частотный побитовый тест"""
    n = len(sequence)
    s_n = abs(sum([int(sequence[i]) if int(sequence[i]) == 1 else -1 for i in range(n)]) * (1 / math.sqrt(n)))
    p_val = erfc(s_n / math.sqrt(2))
    return p_val
    

def main() -> None:
    folder_path = parse().folder_path
    sequences = [f"{folder_path}/{s}" for s in ["cpp_seq.txt", "java_seq.txt", "py_seq.txt"]]

    for i in sequences:
        seq = read_sequence(i)
        print(freq_test(seq))


if __name__ == "__main__":
    main()