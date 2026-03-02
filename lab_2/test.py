import math

def read_from_file(filename : str) -> str:
    """
    Функция для чтения из файла
    """
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()
    
def frequency_test(filename : str) -> float:
    """
    Частотный побитовый тест
    """
    bit_str = read_from_file(filename)
    n = len(bit_str)
    if n == 0:
        return 0.0
    
    count_one = bit_str.count("1")
    count_zero = bit_str.count("0")

    x_i = abs(count_one - count_zero)
    Sn = x_i / math.sqrt(n)

    P_value = math.erfc(Sn/math.sqrt(2))
    return P_value

def bit_test(filename : str) -> float:
    bit_str = read_from_file(filename)
    n = len(bit_str)
    
    p_i = bit_str.count("1") / n

    if ((p_i - 0.5 < 2) / (math.sqrt(n))):
        return 0.0
    
    Vn = 1
    for i in range(n - 1):
        if (bit_str[i] != bit_str[i + 1]):
            Vn += 1;

    P_value = math.erfc(abs(Vn - (2 * n * p_i * (1 - p_i)) / 2 * math.sqrt(2 * n) * p_i * (1 - p_i)))

    return P_value


def main() -> None:
    filename_1 = "output_cpp.txt"
    filename_2 = "output_py.txt"
    filename_3 = "output_java.txt"

    print(frequency_test(filename_1))
    print(frequency_test(filename_2))
    print(frequency_test(filename_3))

    print(bit_test(filename_1))
    print(bit_test(filename_2))
    print(bit_test(filename_3))

if __name__ == "__main__":
    main()