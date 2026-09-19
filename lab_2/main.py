import math
from scipy.special import gammaincc


def bit_frequency_test(bits: str) -> float:
    """
    Частотный побитовый тест
    """
    sumn = (bits.count('1') - bits.count('0')) / math.sqrt(len(bits))
    pvalue = math.erfc(abs(sumn) / math.sqrt(2))
    return pvalue


def consecutive_bits_test(bits: str) -> float:
    """
    Тест на одинаковые подряд идущие биты
    """
    n = len(bits)
    if n == 0:
        return 0.0
    xi = bits.count('1') / n
    if abs(xi - 0.5) >= (2 / math.sqrt(n)):
        return 0.0
    if xi == 0.0 or xi == 1.0:
        return 0.0
    vn = 0
    for i in range(n - 1):
        if bits[i] != bits[i + 1]:
            vn += 1 
    numerator = abs(vn - 2 * n * xi * (1 - xi))
    denominator = 2 * math.sqrt(2 * n) * xi * (1 - xi)
    pvalue = math.erfc(numerator/denominator)
    return pvalue


def longest_sequence_test(bits: str) -> float:
    """
    Тест на самую длинную последовательность единиц в блоке
    """
    m = 8
    n = len(bits) // m
    blocks = [bits[i * m : (i + 1) * m] for i in range(n)]
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


def read_file(file_name: str) -> str:
    """
    Чтение содержимого текстового файла.
    """

    with open(file_name, "r", encoding="utf-8") as file:
        return file.read().strip()

    
def make_tests(lang: str, bits: str, filename: str, mode: str) -> None:
    """
    Сохранение результатов тестов
    """
    with open(filename, mode, encoding="utf-8") as f:
        f.write(lang + "\n")
        f.write("Частотный побитовый тест: " + str(bit_frequency_test(bits)) + "\n")
        f.write("Тест на одинаковые подряд идущие биты: " + str(consecutive_bits_test(bits)) + "\n")
        f.write("Тест на самую длинную последовательность единиц в блоке: " + str(longest_sequence_test(bits)) + "\n\n")


def main() -> None:
    """
    Загрузка ПСЧ и проведение тестов
    """
    bits = read_file("python.txt")
    make_tests("Python", bits, "result.txt", "w")
    bits = read_file("cpp.txt")
    make_tests("C++", bits, "result.txt", "a")
    bits = read_file("java.txt")
    make_tests("Java", bits, "result.txt", "a")


if __name__ == "__main__":
    main()