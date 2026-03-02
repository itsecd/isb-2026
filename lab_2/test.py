import math

def read_from_file(filename : str) -> str:
    """
    Функция для чтения из файла
    """
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()
    
def frequency_analysis(bit_str : str) -> float:
    """
    Частотный побитовый тест
    """
    n = len(bit_str)
    if n == 0:
        return 0.0
    
    count_one = bit_str.count("1")
    count_zero = bit_str.count("0")

    x_i = count_one - count_zero
    Sn = x_i / math.sqrt(n)

    P_value = math.erfc(Sn/math.sqrt(2))
    return P_value


def main() -> None:
    filename_1 = "output_cpp.txt"
    filename_2 = "output_py.txt"
    filename_3 = "output_java.txt"

    print(frequency_analysis(filename_1))
    print(frequency_analysis(filename_2))
    print(frequency_analysis(filename_3))