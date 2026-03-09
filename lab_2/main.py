import math
from pathlib import Path
import scipy.special as sp


import work_file


def frequency_bit_test(binary_str: str) -> float:
    """
    Выполняет тест частоты.

    Тест проверяет, приблизительно ли одинаково количество битов 0 и 1
    в двоичной последовательности, как это ожидается для случайной последовательности.
    """
    stat = 1 / math.sqrt(len(binary_str)) * (binary_str.count("1") - binary_str.count("0"))
    p_value = math.erfc(abs(stat) / math.sqrt(2))
    return p_value

def  identical_consecutive_bit_test(binary_str: str) -> float:
    """
    Выполняет тест серий.

    Тест проверяет, соответствует ли количество серий (последовательностей
    одинаковых подряд идущих битов) ожидаемому количеству для случайной
    последовательности.
    """
    n = len(binary_str)
    xi = binary_str.count("1") / n
    if abs(xi - 0.5) >= (2 / math.sqrt(n)):
        return 0
    V_n = 0
    for i in range(n - 1):
        if(binary_str[i] != binary_str[i + 1]):
            V_n += 1
    
    p_value = math.erfc(abs(V_n - 2 * n * xi * (1 - xi)) / (2 * math.sqrt(2 * n) * xi * (1 - xi)))

    return p_value


def  longest_sequence_in_block(binary_str: str, p: list) -> float:
    """
    Выполняет тест максимальной серии единиц в блоке

    Последовательность разбивается на блоки длиной 8 бит. Для каждого блока
    определяется максимальная длина серии единиц, после чего распределение
    этих длин сравнивается с ожидаемым распределением для случайной последовательности.
    """

    blocks = []
    n = len(binary_str)
    for i in range(0, n, 8):
        block = binary_str[i: i + 8]
        blocks.append(block)
    v = [0, 0, 0, 0]
    for block in blocks:
        max_run = 0
        cur_len = 0
        for j in block:
            if j == "1":
                cur_len += 1
                max_run = max(max_run, cur_len)
            else:
                cur_len = 0
        match max_run:
            case 0 | 1 : v[0] += 1
            case 2     : v[1] += 1
            case 3     : v[2] += 1
            case _ if max_run >= 4: v[3] += 1
    
    Xi_kv = sum(((v[i] - 16 * p[i]) ** 2) / (16 * p[i]) for i in range(len(v)))
    p_value = sp.gammainc((3 / 2), (Xi_kv / 2))
    return p_value

def main():
    """
    Основная функция программы.
    """
    base_dir = Path(__file__).resolve().parent
    input_files = ["seq_cpp", "seq_java"]
    p = [0.2148, 0.3672, 0.2305, 0.1875]

    result_text = ""
    for name in input_files:
        file_without_ext = str(base_dir / name)

        try:
            binary_str = work_file.read_file_txt(file_without_ext).strip()
        except FileNotFoundError:
            result_text += f"Не найден файл: {file_without_ext}.txt\n"
            continue

        result_text += f"\n===== {name}.txt =====\n"
        result_text += f"Длина последовательности: {len(binary_str)}\n"

        p1 = frequency_bit_test(binary_str)
        p2 = identical_consecutive_bit_test(binary_str)
        p3 = longest_sequence_in_block(binary_str, p)

        result_text += f"Frequency Bit Test p-value: {p1}\n"
        result_text += f"Runs Test p-value: {p2}\n"
        result_text += f"Longest Run of Ones in a Block p-value: {p3}\n"

        print(f"Результат {name}.txt можно посмотреть в файле result.txt.") 
    work_file.write_file_txt("result",result_text)
if __name__ == "__main__":
    main()