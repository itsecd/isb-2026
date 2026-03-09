import argparse
import math
from scipy.special import gammaincc
from constants import pi


def parsing() -> str:
    """передача аргументов через командную строку"""
    parser = argparse.ArgumentParser()
    parser.add_argument("python_gen", type=str)
    parser.add_argument("c_gen", type=str)
    parser.add_argument("java_gen", type=str)
    args = parser.parse_args()
    return args.python_gen,args.c_gen,args.java_gen


def get_text(filename_text: str) -> str:
    """считывание текста из файла"""
    with open(filename_text, "r", encoding="utf-8") as file:
        text = file.read()
    return text


def write_text(lang: str, p1: float, p2: float, p3: float) -> None:
    """создание отчета"""
    with open("report.txt", "a", encoding="utf-8") as file:
        file.write("-" * 40 + "\n")
        if lang == "py":
            file.write("Язык: Python\n")
        elif lang == "c":
            file.write("Язык: C++\n")
        elif lang == "java":
            file.write("Язык: Java\n")
        file.write(f"Частотный побитовый тест: {p1}\n")
        file.write(f"Тест на одинаковые подряд идущие биты: {p2}\n")
        file.write(f"Тест на самую длинную последовательность единиц в блоке: {p3}\n")
        if p1 >= 0.01 and p2 >= 0.01 and p3 >= 0.01:
            file.write("Вывод: тест NIST пройден\n")
        else:
            file.write("Вывод: тест NIST НЕ пройден\n")
        file.write("-" * 40 + "\n\n\n")


def bit_freq_test(gen: str) -> float:
    """частотный побитовый тест"""
    sum = 0
    for i in gen:
        if i == "1":
            sum += 1
            continue
        sum += -1
    s = abs(sum) / math.sqrt(len(gen))
    p = math.erfc(s / math.sqrt(2))
    return p


def identical_consecutive_bits_test(gen: str) -> float:
    """тест на одинаковые подряд идущие биты"""
    sum = 0
    n = len(gen)
    for i in gen:
        if i == "1":
            sum += 1
    zeta = sum / n
    if abs(zeta - 0.5) > 2 / math.sqrt(n):
        return 0
    v = 0
    for i in range(n - 1):
        if gen[i] != gen[i + 1]:
            v += 1
    p = math.erfc(
        abs(v - 2 * n * zeta * (1 - zeta)) / (2 * math.sqrt(2 * n) * zeta * (1 - zeta))
    )
    return p


def the_longest_sequence_test(gen: str) -> float:
    """тест на самую длинную последовательность единиц в блоке"""
    gen = [gen[i : i + 8] for i in range(0, 128, 8)]
    v = [0, 0, 0, 0]
    for i in gen:
        max_len = cur_len = 0
        for j in i:
            if j == "1":
                cur_len += 1
                max_len = max(max_len, cur_len)
                continue
            cur_len = 0
        if max_len <= 1:
            v[0] += 1
        elif max_len == 2:
            v[1] += 1
        elif max_len == 3:
            v[2] += 1
        else:
            v[3] += 1
    xi_sqare = 0
    for i in range(3):
        xi_sqare += pow((v[i] - 16 * pi[i]), 2) / (16 * pi[i])
    p = gammaincc(3 / 2, xi_sqare / 2)
    return p


def main():
    try:
        python_gen, c_gen, java_gen = map(get_text, parsing())
        write_text(
            "py",
            bit_freq_test(python_gen),
            identical_consecutive_bits_test(python_gen),
            the_longest_sequence_test(python_gen),
        )
        write_text(
            "c",
            bit_freq_test(c_gen),
            identical_consecutive_bits_test(c_gen),
            the_longest_sequence_test(c_gen),
        )
        write_text(
            "java",
            bit_freq_test(java_gen),
            identical_consecutive_bits_test(java_gen),
            the_longest_sequence_test(java_gen),
        )
    except Exception as ex:
        print("Ошибка: ", ex)


if __name__ == "__main__":
    main()
