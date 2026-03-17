import math

def read_sequence(filename):
    """Читает бинарную последовательность из файла"""
    with open(filename, 'r') as f:
        line = f.readline().strip()
    return [int(bit) for bit in line]


def frequency_test(seq):
    """Частотный побитовый тест"""
    n = len(seq)
    x_i = [1 if bit == 1 else -1 for bit in seq]
    x = abs(sum(x_i))
    s_n = x/math.sqrt(n)
    p_value = math.erfc(s_n / math.sqrt(2))

    print(f"\nЧастотный побитовый тест:")
    print(f"Единиц: {sum(seq)}, Нулей: {n - sum(seq)}")
    print(f"S_n = {s_n:.6f}")
    print(f"P_value = {p_value:.6f}")
    print(f"Результат: {'Случайна' if p_value >= 0.01 else 'НЕ случайна'}")


def runs_test(seq):
    """Тест на одинаковые подряд идущие биты"""
    n = len(seq)
    e = sum(seq)
    z = e / n

    print(f"\nТест на одинаковые подряд идущие биты:")

    if(abs(z - 1/2) < 2 / math.sqrt(n)):
        v_n = sum(1 for i in range(n-1) if seq[i] != seq[i+1])
        p_value = math.erfc(abs(v_n-2*n*z*(1-z)) / (2*math.sqrt(2*n)*z*(1-z)))

        print(f"Число знакоперемен: {v_n}")
        print(f"P_value = {p_value:.6f}")
    else:
        p_value = 0
        print("P_value = 0")

    print(f"Результат: {'Случайна' if p_value >= 0.01 else 'НЕ случайна'}")



def main():
    filename = input("Введите имя файла с последовательностью: ")
    seq = read_sequence(filename)
    print(f"Последовательность длиной n = {len(seq)} бит")

    frequency_test(seq)
    runs_test(seq)
    #longest_run_test(seq)


if __name__ == "__main__":
    main()