import math
from scipy.special import gammaincc

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
    """
    Битовый тест
    """
    bit_str = read_from_file(filename)
    n = len(bit_str)
    
    p_i = bit_str.count("1") / n

    if abs(p_i - 0.5) >= (2 / math.sqrt(n)):
        return 0.0
    
    Vn = 1
    for i in range(n - 1):
        if (bit_str[i] != bit_str[i + 1]):
            Vn += 1;

    num = abs(Vn - 2 * n * p_i * (1 - p_i))
    num_2 = 2 * math.sqrt(2 * n) * p_i * (1 - p_i)
    
    P_value = math.erfc(num / num_2)

    return P_value


def create_v(filename : str) -> dict:
    bit_str = read_from_file(filename)
    step = 8

    v = {1:0, 2:0, 3:0, 4:0}

    
    for i in range(0, 128, step):
        block =  bit_str[i:i+step]

        max_run = 0
        cur_run = 0

        for bit in block:
            if bit == "1":
                cur_run += 1
                if cur_run > max_run:
                    max_run = cur_run
            else:
                cur_run = 0

        if max_run <= 1:
            v[1] += 1
        elif max_run == 2:
            v[2] += 1
        elif max_run == 3:
            v[3] += 1
        elif max_run >= 4:
            v[4] += 1
    
    return v

def calc_xi_square(v : int) -> float:
    pi = {1 : 0.2148, 2 : 0.3672, 3 : 0.2305, 4 : 0.1875}
    xi_sq = 0
    
    for i in range(1, 5):
        value = 16 * pi[i]
        xi_sq += ((v[i] - value) ** 2) / value

    return xi_sq

def len_one_test(filename : str) -> None:
    
    v = create_v(filename)
    xi_sq =  calc_xi_square(v)

    p_value = gammaincc(3 / 2.0, xi_sq / 2.0)

    return p_value

def main() -> None:
    filename_1 = "output_cpp.txt"
    filename_2 = "output_py.txt"
    filename_3 = "output_java.txt"

    print("Тесты:\n")
    print("ГПСЧ C++:\n")
    print(f"Частотный: {frequency_test(filename_1)}\n")
    print(f"Битовый: {bit_test(filename_1)}\n")
    print(f"Тест на длину единиц: {len_one_test(filename_1)}\n\n")

    print("ГПСЧ Python:\n")
    print(f"Частотный: {frequency_test(filename_2)}\n")
    print(f"Битовый: {bit_test(filename_2)}\n")
    print(f"Тест на длину единиц: {len_one_test(filename_2)}\n\n")

    print("ГПСЧ Java:\n")
    print(f"Частотный: {frequency_test(filename_3)}\n")
    print(f"Битовый: {bit_test(filename_3)}\n")
    print(f"Тест на длину единиц: {len_one_test(filename_3)}\n\n")
if __name__ == "__main__":
    main()