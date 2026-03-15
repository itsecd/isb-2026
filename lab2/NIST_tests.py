import argparse
import math
from scipy.special import gammaincc
from constants import PI0, PI1, PI2, PI3


def read_file (file_name: str) -> list[int]:
    """
    читает последовательность из файла и превращает её в список чисел
    """
    sequence = []

    with open(file_name, "r", encoding="utf-8") as file:
        text_sequence = file.read()

        for element in text_sequence:
            sequence.append(int(element))
    
    return sequence


def frequency_bitwise_test (sequence: list[int]) -> float:
    """
    частотный побитовый тест
    """
    N = len(sequence)
    sum = 0

    for element in sequence:
        if element == 1:
            sum += 1
        else:
            sum += -1
    
    S_n = abs(sum) / math.sqrt(N)
    P_value = math.erfc(S_n / math.sqrt(2))

    return P_value


def identical_consecutive_bits_test (sequence: list[int]) -> float:
    """
    тест на одинаковые подряд идущие биты
    """
    N = len(sequence)
    sum = 0

    for element in sequence:
        sum += element
    
    zeta = sum / N

    if abs(zeta - 0.5) >= (2 / math.sqrt(N)):
        return 0.0

    V_n = 0
    for i in range(N-1):
        if sequence[i] != sequence[i+1]:
            V_n += 1

    P_value = math.erfc((abs(V_n - 2 * N * zeta * (1 - zeta))) / (2 * math.sqrt(2 * N) * zeta * (1 - zeta)))
    return P_value


def longest_sequence_ones_test (sequence: list[int]) -> float:
    """
    тест на самую длинную последовательность единиц в блоке
    """
    N = len(sequence)
    M = 8
    
    blocks = []

    for i in range (0, N, M):
        block = sequence[i : i + M]
        blocks.append(block)

    v0 = v1 = v2 = v3 = 0

    for block in blocks:
        max_quantity_ones = 0
        current_quantity_ones = 0

        for number in block:
            if number == 1:
                current_quantity_ones += 1
                if current_quantity_ones > max_quantity_ones:
                    max_quantity_ones = current_quantity_ones
            else:
                current_quantity_ones = 0

        if max_quantity_ones <= 1:
            v0 += 1
        elif max_quantity_ones == 2:
            v1 += 1
        elif max_quantity_ones == 3:
            v2 += 1
        elif max_quantity_ones >= 4:
            v3 += 1
        
    summand0 = ((v0 - 16 * PI0) ** 2) / (16 * PI0)
    summand1 = ((v1 - 16 * PI1) ** 2) / (16 * PI1)
    summand2 = ((v2 - 16 * PI2) ** 2) / (16 * PI2)
    summand3 = ((v3 - 16 * PI3) ** 2) / (16 * PI3)

    hi_square = summand0 + summand1 + summand2 + summand3

    P_value = gammaincc(3 / 2, hi_square / 2)
    return P_value


def write_file (sequence_file_name: str, P_value1: float, P_value2: float, P_value3: float, output_file: str) -> None:
    """
    записывает результаты тестов в файл
    """
    if P_value1 >= 0.01:
        result1 = "Тест пройден"
    else:
        result1 = "Тест не пройден"

    if P_value2 >= 0.01:
        result2 = "Тест пройден"
    else:
        result2 = "Тест не пройден"

    if P_value3 >= 0.01:
        result3 = "Тест пройден"
    else:
        result3 = "Тест не пройден"

    with open(output_file, "a", encoding="utf-8") as file:
        file.write(f"Файл с последовательностью: {sequence_file_name}\n")
        file.write(f"Тест 1: P_value = {P_value1} - {result1}\n")
        file.write(f"Тест 2: P_value = {P_value2} - {result2}\n")
        file.write(f"Тест 3: P_value = {P_value3} - {result3}\n\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", '--python_sequence_file', type=str, default='python_sequence.txt', help='name of python file with sequence')
    parser.add_argument("-c", '--cpp_sequence_file', type=str, default='c++_sequence.txt', help='name of c++ file with sequence')
    parser.add_argument("-j", '--java_sequence_file', type=str, default='java_sequence.txt', help='name of java file with sequence')
    parser.add_argument("-o", '--output_file_name', type=str, default='results.txt', help='name of output file')
    args = parser.parse_args()

    print(f"The name of python file with sequence: {args.python_sequence_file}")
    print(f"The name of c++ file with sequence: {args.cpp_sequence_file}")
    print(f"The name of java file with sequence: {args.java_sequence_file}")
    print(f"The name of output file: {args.output_file_name}")

    with open(args.output_file_name, "w", encoding="utf-8") as file:
        pass

    try:
        python_sequence = read_file(args.python_sequence_file)
        P1_python = frequency_bitwise_test(python_sequence)
        P2_python = identical_consecutive_bits_test(python_sequence)
        P3_python = longest_sequence_ones_test(python_sequence)
        write_file(args.python_sequence_file, P1_python, P2_python, P3_python, args.output_file_name)

        cpp_sequence = read_file(args.cpp_sequence_file)
        P1_cpp = frequency_bitwise_test(cpp_sequence)
        P2_cpp = identical_consecutive_bits_test(cpp_sequence)
        P3_cpp = longest_sequence_ones_test(cpp_sequence)
        write_file(args.cpp_sequence_file, P1_cpp, P2_cpp, P3_cpp, args.output_file_name)

        java_sequence = read_file(args.java_sequence_file)
        P1_java = frequency_bitwise_test(java_sequence)
        P2_java = identical_consecutive_bits_test(java_sequence)
        P3_java = longest_sequence_ones_test(java_sequence)
        write_file(args.java_sequence_file, P1_java, P2_java, P3_java, args.output_file_name)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__" :
    main()