import argparse
import math


from scipy import special as sci


def parse_arguments() -> list:
    """
    Парсинг аргументов из командной строки
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-l1", "--pr_language_1", default="cpp", type=str, help="programming language 1")
    parser.add_argument("-l2", "--pr_language_2", default="py", type=str, help="programming language 2")
    parser.add_argument("-l3", "--pr_language_3", default="java", type=str, help="programming language 3")
    args = parser.parse_args()
    return [args.pr_language_1, args.pr_language_2, args.pr_language_3]


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


def bit_freq_test(seq: str) -> float:
    """
    Частотный побитовый тест
    """
    s = 0
    for i in seq:
        s += (2 * int(i) - 1)
    arg = abs(s/math.sqrt(len(seq)))
    return math.erfc(arg/math.sqrt(2))


def cont_bit_line_test(seq: str) -> float:
    """
    Тест на одинаковые подряд идущие биты
    """
    #Вычисление доли единиц
    n = len(seq)
    fr = 0
    for i in seq:
        fr+=int(i)
    fr/=n
    if abs(fr-0.5) >= 2/math.sqrt(n):
        return 0

    # Вычисление числа знакоперемен
    vn = 0
    for i in range(n-1):
        if seq[i] != seq[i+1]:
            vn+=1
    arg = abs(vn-2*n*fr*(1-fr))/(2*math.sqrt(2*n)*fr*(1-fr))
    return math.erfc(arg)


def longest_line_block_test(seq: str) -> float:
    """
    Тест на самую длинную последовательность единиц в блоке
    """
    # Составление списка макс. длин последовательностей единиц в блоках
    blocks_len = 8
    max_lens = []
    max_len = 0
    cur_len = 0
    for i in range(len(seq)):
        if seq[i] == "1":
            cur_len+=1
        else:
            max_len = max(max_len, cur_len)
            cur_len = 0
        if i % blocks_len == blocks_len-1:
            max_len = max(max_len, cur_len)
            max_lens.append(max_len)
            cur_len = 0
            max_len = 0

    # Составление статистики по разным длинам из списка
    v1 = sum(1 for i in max_lens if i < 2)
    v2 = max_lens.count(2)
    v3 = max_lens.count(3)
    v4 = sum(1 for i in max_lens if i > 3)

    vis = [v1, v2, v3, v4]
    pis = [0.2148, 0.3672, 0.2305, 0.1875]

    # Вычисление Хи-квадрата
    xi = 0
    for i in range(len(vis)):
        xi += (vis[i] - 16*pis[i]) ** 2 / (16 * pis[i])
    return float(sci.gammainc(1.5, xi/2))


def NIST_tests(seq: str, lang: str) -> str:
    """
    Тест на самую длинную последовательность единиц в блоке
    """
    p1 = round(bit_freq_test(seq), 4)
    p2 = round(cont_bit_line_test(seq), 4)
    p3 = round(longest_line_block_test(seq), 4)
    p_values = [p1, p2, p3]

    data = lang + "\n" + seq + "\np1:     p2:     p3:\n"
    for p in p_values:
        data += str(p) + "  "
    passes = sum(1 for p in p_values if p >= 0.01)
    if passes == len(p_values):
        data += "\nsequence is random\n\n"
        return data
    else:
        data += "\nsequence is not random\n\n"
        return data


def main() -> None:
    try:
        langs = parse_arguments()
        data = ""
        for l in langs:
            nums_sequence = read_file(l + "_random_vec.txt")
            data += NIST_tests(nums_sequence, l)
        print(data)
        save_file("data.txt", data)
    except Exception as exc:
        print(f"Возникла ошибка: {exc}")


if __name__ == "__main__":
    main()