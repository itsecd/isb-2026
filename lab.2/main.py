import math
from typing import List
from scipy.special import gammaincc

from const import P_VALUE, BLOCK_SIZE, PI, SOURCE_FILES, OUTPUT_FILE


def frequency_test(seq: str) -> float:
    """
    Частотный побитовый тест ()
    """
    n = len(seq)
    
    
    ones = seq.count('1')
    zeros = n - ones
    
    # Вычисляем сумму: (1 для '1', -1 для '0')
    sum_x = ones - zeros  # ones*(+1) + zeros*(-1)
    
    s_obs = abs(sum_x) / math.sqrt(n)
    p_value = math.erfc(s_obs / math.sqrt(2))
    return p_value


def count_same_bits(seq: str) -> float:
    """
    Тест на одинаковые подряд идущие "0" и "1"
    """
    one_ratio = seq.count("1") / len(seq)

    if abs(one_ratio - 0.5) > (2 / math.sqrt(len(seq))):
        return 0.0

    switch_count = seq.count("01") + seq.count("10")

    return math.erfc(
        abs(switch_count - (2 * len(seq) * one_ratio * (1 - one_ratio)))
        / (2 * math.sqrt(2 * len(seq)) * one_ratio * (1 - one_ratio))
    )


def max_count_in_block(seq: str) -> float:
    """
    Тест на определение самой длинной последовательности из "1"
    """
    v = [0, 0, 0, 0]
    for i in range(len(seq) // BLOCK_SIZE):
        block = seq[BLOCK_SIZE * i : BLOCK_SIZE * i + BLOCK_SIZE]
        count_of_one = max(len(s) for s in block.split("0"))

        if count_of_one <= 1:
            v[0] += 1
        elif count_of_one == 2:
            v[1] += 1
        elif count_of_one == 3:
            v[2] += 1
        else:
            v[3] += 1

    xi = 0
    for i in range(4):
        xi += ((v[i] - 16 * PI[i]) ** 2) / (16 * PI[i])
    return gammaincc(3 / 2, xi / 2)


def read_file(filename: str) -> str:
    """
    Чтение файла
    """
    try:
        with open(filename, encoding="utf-8") as f:
            return f.read()

    except FileExistsError:
        print(f"Failed to open file {filename}")
        exit(2)
    except PermissionError:
        print(f"Permission denied for {filename}")
        exit(2)
    except Exception as e:
        print(e)
        exit(2)


def main() -> None:
    
    cpp_seq = read_file(SOURCE_FILES[0])
    java_seq = read_file(SOURCE_FILES[1])
    py_seq = read_file(SOURCE_FILES[2])


    cpp_values = [
        "CPP",
        frequency_test(cpp_seq),
        count_same_bits(cpp_seq),
        max_count_in_block(cpp_seq),
    ]
    java_values = [
        "JAVA",
        frequency_test(java_seq),
        count_same_bits(java_seq),
        max_count_in_block(java_seq),
    ]
    py_values = [
        "PYTHON",
        frequency_test(py_seq),
        count_same_bits(py_seq),
        max_count_in_block(py_seq),
    ]
    try:
        with open(OUTPUT_FILE, "w") as f:
            f.write("Lang:|  1 test  |  2 test  | 3 test     | result \n")
            f.write(
                f"{cpp_values[0]:<8}|  {cpp_values[1]:.7f}  |  {cpp_values[2]:.7f}  | {cpp_values[3]:.12f}| {'Good' if all(x >= P_VALUE for x in cpp_values[1:]) else 'Bad'}\n"
            )
            f.write(
                f"{java_values[0]:<8}|  {java_values[1]:.7f}  |  {java_values[2]:.7f}  | {java_values[3]:.12f}| {'Good' if all(x >= P_VALUE for x in java_values[1:]) else 'Bad'}\n"
            )
            f.write(
                f"{py_values[0]:<8}|  {py_values[1]:.7f}  |  {py_values[2]:.7f}  | {py_values[3]:.12f}| {'Good' if all(x >= P_VALUE for x in py_values[1:]) else 'Bad'}\n"
            )
    except Exception as e:
        print(f"Error: {e}\n")


if __name__ == "__main__":
    main()