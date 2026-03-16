import argparse
import math


import scipy


def parse_arguments() -> list:
    """
    Парсинг аргументов из командной строки
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--alphabet_file", default="alphabet.txt", type=str, help="alphabet file")
    parser.add_argument("-i", "--input_file", default="base_text.txt", type=str, help="input file")
    parser.add_argument("-o", "--output_cipher", default="cipher.txt",  type=str, help="output file name")
    parser.add_argument("-k", "--key_file", default="key.txt",  type=str, help="key for the cipher")
    args = parser.parse_args()
    return [args.input_file, args.output_cipher, args.key_file]


def read_file(file_name: str) -> str:
    """
    Чтение файла
    """
    with open(file_name, "r", encoding="utf-8") as file:
        text = file.read().lower()
    return text


def save_file(file_name: str, text: str) -> None:
    """
    Сохранение файла
    """
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(text)
    return


def bit_freq_test(nums: str) -> float:
    """
    Частотный побитовый тест
    """
    s = 0
    for i in nums:
        s -= (1 - 2 * int(i))
    arg = s/math.sqrt(len(nums))
    return math.erfc(arg/math.sqrt(2))


def cont_bit_line_test(nums: str) -> float:
    """
    Тест на одинаковые подряд идущие биты
    """
    #Вычисление доли единиц
    n = len(nums)
    fr = 0
    for i in nums:
        fr+=int(i)
    fr/=n
    if abs(fr-0.5) >= 2/math.sqrt(n):
        return 0

    # Вычисление числа знакоперемен
    vn = 0
    for i in range(n-1):
        if nums[i] != nums[i+1]:
            vn+=1
    arg = abs(vn-2*n*fr*(1-fr))/(2*math.sqrt(2*n)*fr*(1-fr))
    return math.erfc(arg)


def longest_line_block_test(nums: str) -> float:
    """
    Тест на самую длинную последовательность единиц в блоке
    """
    # Составление списка макс. длин последовательностей единиц в блоках
    blocks_len = 8
    max_lines = []
    max_line = 0
    cur_line = 0
    for i in range(len(nums)):
        if nums[i] == "1":
            cur_line+=1
        else:
            max_line = max(max_line, cur_line)
            cur_line = 0
        if i % blocks_len == blocks_len-1:
            max_line = max(max_line, cur_line)
            max_lines.append(max_line)
            cur_line = 0
            max_line = 0

    # Составление статистики по разным длинам из списка
    v1 = sum(1 for i in max_lines if i < 2)
    v2 = max_lines.count(2)
    v3 = max_lines.count(3)
    v4 = sum(1 for i in max_lines if i > 3)

    vis = [v1, v2, v3, v4]
    pis = [0.2148, 0.3672, 0.2305, 0.1875]

    # Вычисление Хи-квадрата
    xi = 0
    for i in range(len(vis)):
        xi += (vis[i] - 16*pis[i]) ** 2 / (16 * pis[i])
    return scipy.special.gammainc(1.5, xi/2)


def main() -> None:
    try:
        rand_nums = read_file("cpp_random_vec.txt")
        print(rand_nums)
        p1 = round(bit_freq_test(rand_nums), 4)
        print(p1)
        p2 = round(cont_bit_line_test(rand_nums), 4)
        print(p2)
        p3 = round(longest_line_block_test(rand_nums), 4)
        print(p3)
    except Exception as exc:
        print(f"Возникла ошибка: {exc}")


if __name__ == "__main__":
    main()