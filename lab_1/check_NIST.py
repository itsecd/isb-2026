from math import sqrt, erfc
from scipy.special import gammaincc
import os


def check(P1: float, P2: float, P3: float):
    """Проверка каждого теста на успех"""

    result = ''

    if P1 >= 0.01:
        result += 'Частотный побитовый анализ пройден успешно\n'
    else:
        result += 'Частотный побитовый анализ не пройден\n'

    if P2 >= 0.01:
        result += 'Тест на одинаковые подряд идущие биты пройден успешно\n'
    else:
        result += 'Тест на одинаковые подряд идущие биты не пройден\n'

    if P3 >= 0.01:
        result += 'Тест на самую длинную последовательность единиц в блоке пройден успешно\n'
    else:
        result += 'Тест на самую длинную последовательность единиц в блоке не пройден\n'

    return result


def write_file(file: str, result1: str, result2: str, result3: str):
    """Запись результатов"""

    with open(file, "w", encoding="utf-8") as f:
        f.write("Результат гпсч python\n"+result1)
        f.write("\n\nРезультат гпсч C++\n"+result2)
        f.write("\n\nРезультат гпсч JAVA\n"+result3)


def read_file(file: str):
    """Чтение файла"""

    if not os.path.exists(file):
        raise FileNotFoundError(f"Файл не найден: {file}")

    with open(file, "r", encoding="utf-8") as f:
        bits = f.read().strip()

    if not bits:
        raise ValueError(f"Файл {file} не содержит битов")

    return bits


def frequency_bitwise_analysis(bits: str):
    """Частотный побитовый анализ"""

    s = sum(1 if b == '1' else -1 for b in bits)

    s = abs(s/sqrt(len(bits)))

    return erfc(s/sqrt(2))


def consecutive_identical_bits(bits: str):
    """Тест на одинаковые подряд идущие биты"""

    l = len(bits)

    s = sum(1 for b in bits if b == '1')

    freq = s/l

    if abs(freq-0.5) >= (2/sqrt(l)):
        return 0.0

    v = 0.0

    for i in range(1, l):
        if bits[i] != bits[i-1]:
            v += 1

    return erfc(abs(v-2*l*freq*(1-freq)) / (2*sqrt(2*l)*freq*(1-freq)))


def longest_sequence(bits):
    """Тест на самую длинную последовательность единиц в блоке"""
    v = [0]*4
    temp = 0
    m = 0
    k = 0

    for i in bits:

        if i == '1':
            temp += 1
        else:
            m = max(m, temp)
            temp = 0
        k += 1

        if k == 8:
            if m <= 1:
                v[0] += 1
            elif m == 2:
                v[1] += 1
            elif m == 3:
                v[2] += 1
            else:
                v[3] += 1
            m = k = temp = 0

    p = [0.2148, 0.3672, 0.2305, 0.1875]
    chi_sq = 0.0

    for i in range(0, 4):
        chi_sq += ((v[i]-16*p[i])**2)/(16*p[i])

    return gammaincc(3/2, chi_sq/2)


def main():
    bits_py = read_file("result_py.txt")
    bits_cpp = read_file("result_cpp.txt")
    bits_java = read_file("result_java.txt")

    write_file(
        'result.txt',
        check(frequency_bitwise_analysis(bits_py),
              consecutive_identical_bits(bits_py), longest_sequence(bits_py)),
        check(frequency_bitwise_analysis(bits_cpp), consecutive_identical_bits(
            bits_cpp), longest_sequence(bits_cpp)),
        check(frequency_bitwise_analysis(bits_java), consecutive_identical_bits(
            bits_java), longest_sequence(bits_java))
    )


if __name__ == "__main__":
    main()
