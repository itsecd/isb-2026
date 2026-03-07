import math
from scipy.special import gammaincc
from typing import List
import argparse
from const import COEFF


def frequency_test(bits: List[int]) -> float:
    """
    Частотный побитовый тест
    """
    n = len(bits)
    x = [1 if b == 1 else -1 for b in bits]
    sum_x = abs(sum(x))
    s_obs = sum_x / math.sqrt(n)
    p_value = math.erfc(s_obs / math.sqrt(2))
    return p_value


def runs_test(bits: List[int]) -> float:
    """
    Тест на одинаковые подряд идущие биты
    """
    n = len(bits)
    ones = bits.count(1)
    zeta = ones / n
    if abs(zeta - 0.5) >= 2.0 / math.sqrt(n):
        return 0.0
    v_n = 0
    for i in range(n - 1):
        if bits[i] != bits[i + 1]:
            v_n += 1

    numerator = abs(v_n - 2 * n * zeta * (1 - zeta))
    denominator = 2 * math.sqrt(2 * n) * zeta * (1 - zeta)
    if denominator == 0:
        return 0.0
    p_value = math.erfc(numerator / denominator)
    return p_value


def longest_run_test(bits: List[int], block_size: int = 8) -> float:
    """
    Тест на самую длинную последовательность единиц в блоке.
    """
    n = len(bits)
    num_blocks = n // block_size
    if num_blocks == 0:
        raise ValueError("Такое количество битов невозможно")
    pi = [0.2148, 0.3672, 0.2305, 0.1875]

    v = [0, 0, 0, 0]
    for block_idx in range(num_blocks):
        block = bits[block_idx * block_size: (block_idx + 1) * block_size]
        max_run = 0
        current_run = 0
        for b in block:
            if b == 1:
                current_run += 1
                if current_run > max_run:
                    max_run = current_run
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

    chi_sq = 0.0
    for i in range(4):
        expected = num_blocks * pi[i]
        chi_sq += (v[i] - expected) ** 2 / expected

    p_value = gammaincc(1.5, chi_sq / 2.0)
    return p_value


def input_file(filename: str) -> List[int]:
    """Функция для считывания файла
    На вход принимается имя необходимого файла
    Если файл не найден будет выброшено исключение
    """
    try:
        file = open(filename, "r", encoding="utf-8")
        print(f"File {filename} ready to work")
        text = file.read()
        file.close()
        bits = []
        for bit in text:
            bits.append(int(bit))
        return bits
    except FileNotFoundError:
        print("Sorry, this file impossible to detect")
        return ""

def check_resualt(result: List) -> bool:
    """
    Функция для проверки результатов теста
    """
    for res in result[0]:
        if res<COEFF:
            return False
    return True


def output_file(filename: str, result: List, filename_bits: str, check_res: bool) -> None:
    """Функция для дозаписи данных в файл"""
    with open(filename, "a", encoding="utf-8") as file:
        line = f"{filename_bits}    {result[0][0]}  {result[0][1]}  {result[0][2]}        {check_res}\n"
        file.write(line)


def parse_command_line():
    """Разбор аргументов командной строки с помощью argparse."""
    parser = argparse.ArgumentParser(
        description="Шифрование/дешифрование текста с использованием квадрата Полибия и сдвига по строкам/столбцам."
    )
    parser.add_argument(
        "bits_file",
        help="Файл для считывания последовательности бит"
    )
    parser.add_argument(
        "result_file",
        help="Файл для записи результатов тестирования"
    )
    args = parser.parse_args()
    return args.bits_file,args.result_file


def main():
    bits_file,result_file = parse_command_line()
    bits = input_file(bits_file)
    if not bits:
        print("Ошибка: не удалось прочитать файл или файл пуст.")
        return
    result = []
    p_value1 = frequency_test(bits)
    p_value2 = runs_test(bits)
    p_value3 = float(longest_run_test(bits))
    result.append([p_value1, p_value2, p_value3])
    check_res=check_resualt(result)
    output_file(result_file,result,bits_file,check_res)


if __name__ == "__main__":
    main()
