import math
import os

from scipy.special import gammaincc

from consts import BLOCK_SIZE, PI, DIRECTORY, PVALUE, OUTPUT


def test_frequency(text: str) -> float:
    """
    Частотный побитовый тест NIST.
    Возвращает P-значение для переданного текста
    """
    text_length = len(text)
    ones_count = text.count("1")
    zeros_count = text_length - ones_count
    Sn = ones_count - zeros_count
    Sn = Sn / (text_length ** 0.5)

    return math.erfc(Sn / (2 ** 0.5))


def test_identical_bits(text: str) -> float:
    """
    Тест на одинаковые идущие подряд биты NIST.
    Возвращает P-значение для переданного текста
    """
    text_length = len(text)
    ksi = text.count("1") / text_length
    if not (abs(ksi - 0.5) < (2 / (text_length ** 0.5))):
        return 0.0
    
    Vn = text.count("01") + text.count("10")
    numerator = abs(Vn - 2 * text_length * ksi * (1 - ksi))
    denominator = 2 * ((2 * text_length) ** 0.5) * ksi * (1 - ksi)
    return math.erfc(numerator / denominator)


def test_longest_sequence(text: str) -> float:
    """
    Тест на самую длинную последовательность единиц в блоке NIST.
    Возвращает P-значение для переданного текста
    """
    v = [0, 0, 0, 0]
    block_count = len(text) // BLOCK_SIZE

    for i in range(block_count):
        block = text[i * BLOCK_SIZE:(i + 1) * BLOCK_SIZE]
        block_str = str(block)
        
        if block_str.count("1111") > 0:
            v[3] += 1
        elif block_str.count("111") > 0:
            v[2] += 1
        elif block_str.count("11") > 0:
            v[1] += 1
        else:
            v[0] += 1

    xi_value = 0.0
    for i in range(4):
        xi_value += ((v[i] - 16 * PI[i]) ** 2) / (16 * PI[i])

    return gammaincc(1.5, xi_value / 2)


def read_file(filename: str) -> str:
    """Читает файл по имени. Возвращает прочитанный текст"""
    try:
        with open(filename, 'r') as file_handle:
            return file_handle.read()
    except Exception as error:
        print(f"Ошибка при чтении файла: {error}")
        exit(-1)


def main() -> None:
    """Главная функция программы."""
    file_list = os.listdir(DIRECTORY)
    test_results = []
    
    print("Начало обработки файлов...")
    
    for filename in file_list:
        if ".txt" in filename and filename.lower() != "cmakelists.txt":
            print(f"Обрабатывается файл: {filename}")
            file_content = read_file(DIRECTORY + filename)
            freq_pvalue = test_frequency(file_content)
            identical_pvalue = test_identical_bits(file_content)
            longest_pvalue = test_longest_sequence(file_content)
            test_results.append([filename, freq_pvalue, identical_pvalue, longest_pvalue])

    for result_row in test_results:
        all_pvalues = result_row[1:]
        is_passed = all(p >= PVALUE for p in all_pvalues)
        result_row.append("Да" if is_passed else "Нет")

    
    with open(OUTPUT, "w") as output_file:
        output_file.write("Язык | Частотный тест | Тест на одинаковые биты | Тест на длинную последовательность | Результат\n\n")
        for result_row in test_results:
            output_file.write(f"{result_row[0]} ")
            output_file.write(f"{result_row[1]:.6f} ")
            output_file.write(f"{result_row[2]:.6f} ")
            output_file.write(f"{result_row[3]:.6f} ")
            output_file.write(f"{result_row[4]}\n")
    
    
    print("\nРезультаты тестирования:")
    print("-" * 80)
    for result_row in test_results:
        print(f"Файл: {result_row[0]}")
        print(f"  Частотный тест: {result_row[1]:.6f}")
        print(f"  Тест на одинаковые биты: {result_row[2]:.6f}")
        print(f"  Тест на длинную последовательность: {result_row[3]:.6f}")
        print(f"  Итог: {'ПРОЙДЕН' if result_row[4] == 'Да' else 'НЕ ПРОЙДЕН'}")
        print()


if __name__ == "__main__":
    main()