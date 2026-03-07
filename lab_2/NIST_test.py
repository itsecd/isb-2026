import argparse
import math
from scipy.special import gammaincc
import csv


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_file_c", nargs="?", help="Путь к файлу для обработки c++"
    )
    parser.add_argument(
        "input_file_python", nargs="?", help="Путь к файлу для обработки python"
    )
    parser.add_argument(
        "input_file_java", nargs="?", help="Путь к файлу для обработки java"
    )
    return parser.parse_args()


def read_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print("Ошибка: Файл не найден")
        return None
    except Exception as e:
        print("Ошибка при чтении файла:", e)
        return None


def Frequency_bitwise_test(data):
    n = len(data)
    sum = 0
    for num in data:
        if num == 1:
            sum += 1
        else:
            sum -= 1
    s_obs = abs(sum) / math.sqrt(n)
    P = math.erfc(s_obs / math.sqrt(2))
    return P


def Test_consecutive_identical_bits(data):
    n = len(data)
    ones = sum(data)

    percentage_units = ones / n
    if abs(percentage_units - 0.5) >= (2 / math.sqrt(n)):
        return 0.0
    V_n = 1
    for i in range(n - 1):
        if data[i] != data[i + 1]:
            V_n += 1
    numerator = abs(V_n - 2 * n * percentage_units * (1 - percentage_units))
    denominator = 2 * math.sqrt(2 * n) * percentage_units * (1 - percentage_units)
    P = math.erfc(numerator / denominator)
    return P


def create_v(data):
    step = 8
    v = {0: 0, 1: 0, 2: 0, 3: 0}

    for i in range(0, 128, step):
        block = data[i : i + step]

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
            v[0] += 1
        elif max_run == 2:
            v[1] += 1
        elif max_run == 3:
            v[2] += 1
        elif max_run >= 4:
            v[3] += 1

    return v


def calculate_chi_square(v):

    pi = [0.2148, 0.3672, 0.2305, 0.1875]
    n_blocks = 16

    chi_square = 0
    for i in range(4):
        expected = n_blocks * pi[i]
        chi_square += ((v[i] - expected) ** 2) / expected

    return chi_square


def calculate_p_value(chi_square):
    a = 3 / 2
    x = chi_square / 2
    p_value = gammaincc(a, x)
    return p_value


def check_result(p_value):
    if p_value >= 0.01:
        return True
    else:
        return False


def to_bit_list(text):
    if text is None:
        return []
    clean = "".join(c for c in text if c in "01")
    return [int(bit) for bit in clean]


def write_results_to_csv(results, filename="test_results.csv"):

    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Язык", "Тест", "P-значение", "Результат"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print(f"\nРезультаты сохранены в файл: {filename}")


def run_tests_for_language(bits, lang_name):
    results = []

    if len(bits) == 0:
        print(f"{lang_name}: нет данных для тестирования")
        return results

    # Тест 1: Частотный тест
    p1 = Frequency_bitwise_test(bits)
    passed1 = check_result(p1)
    status1 = "ПРОЙДЕН" if passed1 else "НЕ ПРОЙДЕН"
    results.append(
        {
            "Язык": lang_name,
            "Тест": "Частотный тест",
            "P-значение": p1,
            "Результат": status1,
        }
    )

    # Тест 2: Тест на последовательности одинаковых битов
    p2 = Test_consecutive_identical_bits(bits)
    passed2 = check_result(p2)
    status2 = "ПРОЙДЕН" if passed2 else "НЕ ПРОЙДЕН"
    results.append(
        {
            "Язык": lang_name,
            "Тест": "Тест на серии",
            "P-значение": p2,
            "Результат": status2,
        }
    )

    # Тест 3: Тест на самую длинную последовательность
    bits_str = "".join(str(b) for b in bits[:128])
    v = create_v(bits_str)
    chi2 = calculate_chi_square(v)
    p3 = calculate_p_value(chi2)
    passed3 = check_result(p3)
    status3 = "ПРОЙДЕН" if passed3 else "НЕ ПРОЙДЕН"
    results.append(
        {
            "Язык": lang_name,
            "Тест": "Тест на макс. последовательность",
            "P-значение": p3,
            "Результат": status3,
        }
    )

    return results


if __name__ == "__main__":
    arg = parse_arguments()

    output_c = read_file(arg.input_file_c)
    output_python = read_file(arg.input_file_python)
    output_java = read_file(arg.input_file_java)

    bits_c = to_bit_list(output_c)
    bits_python = to_bit_list(output_python)
    bits_java = to_bit_list(output_java)

    all_results = []

    all_results.extend(run_tests_for_language(bits_c, "C++"))
    all_results.extend(run_tests_for_language(bits_python, "Python"))
    all_results.extend(run_tests_for_language(bits_java, "Java"))

    write_results_to_csv(all_results, "test_results.csv")
