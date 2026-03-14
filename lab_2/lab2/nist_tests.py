import math
from scipy.special import gammaincc

def read_bits(filename):
    """Чтение из файла"""
    with open(filename) as f:
        return f.read().strip()


def frequency_test(bits):
    """Частотный анализ"""
    n = len(bits)
    s = sum(1 if b == '1' else -1 for b in bits)
    s_obs = abs(s) / math.sqrt(n)
    return math.erfc(s_obs / math.sqrt(2))


def runs_test(bits):
    """Одинаковые биты идущие подряд"""
    n = len(bits)
    pi = bits.count('1') / n

    if abs(pi - 0.5) >= 2 / math.sqrt(n):
        return 0.0

    v = 1
    for i in range(1, n):
        if bits[i] != bits[i-1]:
            v += 1

    num = abs(v - 2*n*pi*(1-pi))
    den = 2 * math.sqrt(2*n) * pi*(1-pi)

    return math.erfc(num / den)


def longest_run_test(bits):
    """Самая длинная последовательность единиц"""

    block_size = 8
    N = len(bits) // block_size

    blocks = [bits[i*block_size:(i+1)*block_size] for i in range(N)]

    v = [0,0,0,0]

    for block in blocks:
        max_run = 0
        cur = 0

        for b in block:
            if b == '1':
                cur += 1
                max_run = max(max_run, cur)
            else:
                cur = 0

        if max_run <= 1:
            v[0] += 1
        elif max_run == 2:
            v[1] += 1
        elif max_run == 3:
            v[2] += 1
        else:
            v[3] += 1

    pi = [0.2148, 0.3672, 0.2305, 0.1875]

    chi2 = sum((v[i] - N*pi[i])**2/(N*pi[i]) for i in range(4))

    return gammaincc(3/2, chi2/2)


def evaluate_test(name, p_value):
    """Оценочка"""
    status = "пройден" if p_value >= 0.01 else "НЕ пройден"
    return f"{name}: {p_value:.6f} - {status}"


def test_file(filename, out):
    """Тестирование и запись результатов"""
    bits = read_bits(filename)

    out.write(f"\nФАЙЛ: {filename}\n")
    out.write(evaluate_test("частотный тест", frequency_test(bits)) + "\n")
    out.write(evaluate_test("тест на подряд идущие биты", runs_test(bits)) + "\n")
    out.write(evaluate_test("тест на длинную последовательность", longest_run_test(bits)) + "\n")


def main():

    with open("result.txt", "w") as out:
        test_file("seq_cpp.txt", out)
        test_file("seq_java.txt", out)
        test_file("seq_py.txt", out)


if __name__ == "__main__":
    main()