import math
from scipy.special import gammaincc


def bit_frequency_test(bitstring: str) -> float:
    """
    Функция для частотного побитового теста
    """
    sumn = (bitstring.count('1')-bitstring.count('0'))/math.sqrt(len(bitstring))
    pvalue = math.erfc(abs(sumn)/math.sqrt(2))
    return pvalue


def consecutive_bits_test(bitstring: str) -> float:
    """
    Функция для теста на одинаковые подряд идущие биты
    """
    n = len(bitstring)
    if n == 0:
        return 0.0
    xi = bitstring.count('1') / n
    if abs(xi - 0.5) >= (2 / math.sqrt(n)):
        return 0.0
    if xi == 0.0 or xi == 1.0:
        return 0.0
    vn = 1
    for i in range(n - 1):
        if bitstring[i] != bitstring[i+1]:
            vn += 1 
    numerator = abs(vn - 2*n*xi*(1 - xi))
    denominator = 2 * math.sqrt(2*n)*xi*(1 - xi)
    pvalue = math.erfc(numerator/denominator)
    return pvalue


def longest_sequence_test(bitstring: str) -> float:
    """
    Функция для теста на самую длинную последовательность единиц в блоке
    """
    m = 8
    n = len(bitstring) // m
    blocks = [bitstring[i*m : (i+1)*m] for i in range(n)]
    v1, v2, v3, v4 = 0, 0, 0, 0
    for block in blocks:
        lmax = 0
        lcurrent = 0
        for bit in block:
            if bit == '1':
                lcurrent += 1
                lmax = max(lmax, lcurrent)
            else:
                lcurrent = 0
        if lmax <= 1:
            v1 += 1
        elif lmax == 2:
            v2 += 1
        elif lmax == 3:
            v3 += 1
        else:
            v4 += 1
    pi0, pi1, pi2, pi3 = 0.2148, 0.3672, 0.2305, 0.1875
    chi = (
        ((v1 - n * pi0)**2) / (n * pi0) +
        ((v2 - n * pi1)**2) / (n * pi1) +
        ((v3 - n * pi2)**2) / (n * pi2) +
        ((v4 - n * pi3)**2) / (n * pi3)
    )
    pvalue = gammaincc(1.5, chi / 2)
    return pvalue


def run_tests(bitstring: str) -> tuple[float, float, float]:
    """
    Функция для проведения тестов над псч
    """
    frequency = bit_frequency_test(bitstring)
    consecutive = consecutive_bits_test(bitstring)
    sequence = longest_sequence_test(bitstring)
    return frequency, consecutive, sequence


def write_results(prng_name: str, filename: str, bitstring: str, mode: str) -> None:
    """
    Функция для записи результатов тестов
    """
    test_results = run_tests(bitstring)
    with open(filename, mode, encoding="utf-8") as f:
        f.write("ГПСЧ языка: "+prng_name+"\n")
        f.write("Частотный побитовый тест "+str(test_results[0])+"\n")
        f.write("Тест на одинаковые подряд идущие биты: "+str(test_results[1])+"\n")
        f.write("Тест на самую длинную последовательность единиц в блоке "+str(test_results[2])+"\n\n")


def write_results_nooverwrite(prng_name: str, filename: str, bitstring: str) -> None:
    """
    Функция для записи результатов тестов
    """
    test_results = run_tests(bitstring)
    with open(filename, "a", encoding="utf-8") as f:
        f.write("ГПСЧ языка: "+prng_name+"\n")
        f.write("Частотный побитовый тест "+str(test_results[0])+"\n")
        f.write("Тест на одинаковые подряд идущие биты: "+str(test_results[1])+"\n")
        f.write("Тест на самую длинную последовательность единиц в блоке "+str(test_results[2])+"\n\n")


def main() -> None:
    """
    Главная фунцкия, осуществляющая загрузку псч, проведение тестов и запись результатов
    """
    with open("python_string.txt", "r", encoding="utf-8") as fp:
        py_string = fp.read().strip()
    write_results("Python", "results.txt", py_string, "w")
    with open("cpp_string.txt", "r", encoding="utf-8") as fc:
        cpp_string = fc.read().strip()
    write_results("C++", "results.txt", cpp_string, "a")
    with open("java_string.txt", "r", encoding="utf-8") as fj:
        java_string = fj.read().strip()
    write_results("Java", "results.txt", java_string, "a")


if __name__ == "__main__":
    main()