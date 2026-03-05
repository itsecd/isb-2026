import math
import os
import config


def read_sequence_from_file(filepath):
    """Читает последовательность из файла"""
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"Файл не найден: {filepath}\n"
            f"Сначала запустите генератор для создания файла!"
        )

    with open(filepath, 'r', encoding='utf-8') as file:
        sequence = file.read().strip()

    return sequence


def frequency_test(sequence):
    """Выполняет частотный побитовый тест"""
    n = len(sequence)
    sn = 0

    for bit in sequence:
        if bit == '1':
            sn = sn + 1
        else:
            sn = sn - 1

    s_n = sn / math.sqrt(n)
    p_value = math.erfc(abs(s_n) / math.sqrt(2))

    return {
        'sn': sn,
        's_n': s_n,
        'p_value': p_value
    }


def runs_test(sequence):
    """Выполняет тест на одинаковые подряд идущие биты"""
    n = len(sequence)

    ones = sequence.count('1')
    pi = ones / n

    zeros = sequence.count('0')

    v_n = 0
    for i in range(n - 1):
        if sequence[i] != sequence[i + 1]:
            v_n = v_n + 1

    condition = abs(pi - 0.5) < (2 / math.sqrt(n))

    if condition:
        numerator = abs(v_n - 2 * n * pi * (1 - pi))
        denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)
        p_value = math.erfc(numerator / denominator)
    else:
        p_value = 0.0

    return {
        'ones': ones,
        'zeros': zeros,
        'pi': pi,
        'v_n': v_n,
        'condition': condition,
        'p_value': p_value
    }


def longest_run_test(sequence):
    """Выполняет тест на самую длинную последовательность единиц в блоке"""
    n = len(sequence)
    m = config.BLOCK_SIZE
    num_blocks = n // m

    v = [0, 0, 0, 0]
    block_max_runs = []

    for i in range(num_blocks):
        start = i * m
        end = (i + 1) * m
        block = sequence[start:end]

        max_run = 0
        current_run = 0

        for bit in block:
            if bit == '1':
                current_run = current_run + 1
                if current_run > max_run:
                    max_run = current_run
            else:
                current_run = 0

        block_max_runs.append(max_run)

        if max_run <= 1:
            v[0] = v[0] + 1
        elif max_run == 2:
            v[1] = v[1] + 1
        elif max_run == 3:
            v[2] = v[2] + 1
        else:
            v[3] = v[3] + 1

    chi2 = 0.0
    chi2_terms = []
    expected_values = []

    for i in range(4):
        expected = num_blocks * config.PI_VALUES[i]
        expected_values.append(expected)
        term = ((v[i] - expected) ** 2) / expected
        chi2_terms.append(term)
        chi2 = chi2 + term

    return {
        'num_blocks': num_blocks,
        'block_max_runs': block_max_runs,
        'distribution': v,
        'expected': expected_values,
        'chi2_terms': chi2_terms,
        'chi2': chi2
    }


def calculate_p_value_for_longest_run(chi2):
    """Возвращает инструкцию для вычисления P-значения через онлайн калькулятор"""
    x_value = chi2 / 2
    return (
        f"Для получения P-значения:\n"
        f"   1. Откройте: https://www.danielsoper.com/statcalc/calculator.aspx?id=34\n"
        f"   2. Выберите 'Lower Incomplete Gamma Function'\n"
        f"   3. Введите: a = 1.5, x = {x_value:.6f}\n"
        f"   4. Полученное значение должно быть >= {config.ALPHA}"
    )


def save_results_to_file(results, filename):
    """Сохраняет результаты тестирования в файл"""
    with open(filename, 'w', encoding='utf-8') as file:
        file.write("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ ПСЕВДОСЛУЧАЙНЫХ ПОСЛЕДОВАТЕЛЬНОСТЕЙ\n\n")
        file.write(f"Длина последовательности: {config.SEQUENCE_LENGTH} бит\n")
        file.write(f"Уровень значимости (α): {config.ALPHA}\n")

        for gen_name, res in results.items():
            file.write(f"\nГЕНЕРАТОР: {gen_name}\n")
            file.write(f"Длина: {len(res['sequence'])} бит\n")
            file.write(f"Полная последовательность: {res['sequence']}\n\n")

            file.write("1. ЧАСТОТНЫЙ ПОБИТОВЫЙ ТЕСТ\n")
            freq = res['frequency']
            file.write(f"   SN (сумма, где 1=+1, 0=-1) = {freq['sn']}\n")
            file.write(f"   S_n (нормированная сумма) = SN/√n = {freq['s_n']:.6f}\n")
            file.write(f"   P-value = erfc(|S_n|/√2) = {freq['p_value']:.6f}\n")

            if freq['p_value'] >= config.ALPHA:
                file.write(f"   РЕЗУЛЬТАТ: ПРОЙДЕН (P-value >= {config.ALPHA})\n\n")
            else:
                file.write(f"   РЕЗУЛЬТАТ: НЕ ПРОЙДЕН (P-value < {config.ALPHA})\n\n")

            file.write("2. ТЕСТ НА ОДИНАКОВЫЕ ПОДРЯД ИДУЩИЕ БИТЫ (RUNS TEST)\n")
            runs = res['runs']
            file.write(f"   Количество единиц = {runs['ones']}\n")
            file.write(f"   Количество нулей = {runs['zeros']}\n")
            file.write(f"   π (доля единиц) = {runs['pi']:.6f}\n")
            file.write(f"   Проверка условия |π - 1/2| < 2/√n: ")
            file.write(f"|{runs['pi']:.6f} - 0.5| = {abs(runs['pi'] - 0.5):.6f} < {2 / math.sqrt(len(res['sequence'])):.6f}? ")

            if runs['condition']:
                file.write(f"ДА\n")
            else:
                file.write(f"НЕТ\n")

            file.write(f"   V_n (число знакоперемен) = {runs['v_n']}\n")
            file.write(f"   P-value = {runs['p_value']:.6f}\n")

            if runs['p_value'] >= config.ALPHA:
                file.write(f"   РЕЗУЛЬТАТ: ПРОЙДЕН (P-value >= {config.ALPHA})\n\n")
            else:
                file.write(f"   РЕЗУЛЬТАТ: НЕ ПРОЙДЕН (P-value < {config.ALPHA})\n\n")

            file.write("3. ТЕСТ НА САМУЮ ДЛИННУЮ ПОСЛЕДОВАТЕЛЬНОСТЬ ЕДИНИЦ В БЛОКЕ\n")
            longest = res['longest']
            file.write(f"   Длина блока M = {config.BLOCK_SIZE}\n")
            file.write(f"   Количество блоков = {longest['num_blocks']}\n\n")

            file.write("   Максимальные длины единиц в каждом блоке:\n")
            file.write(f"   {longest['block_max_runs']}\n\n")

            file.write("   Распределение блоков по категориям:\n")
            file.write(f"   Категория 1 (макс. длина <= 1): {longest['distribution'][0]} блоков\n")
            file.write(f"   Категория 2 (макс. длина = 2): {longest['distribution'][1]} блоков\n")
            file.write(f"   Категория 3 (макс. длина = 3): {longest['distribution'][2]} блоков\n")
            file.write(f"   Категория 4 (макс. длина >= 4): {longest['distribution'][3]} блоков\n\n")

            file.write("   Ожидаемые значения:\n")
            for i in range(4):
                file.write(f"   E{i + 1} = 16 * {config.PI_VALUES[i]} = {longest['expected'][i]:.2f}\n")
            file.write("\n")

            file.write("   Вычисление хи-квадрат:\n")
            file.write(f"   χ² = Σ((наблюдаемое - ожидаемое)² / ожидаемое)\n")
            for i in range(4):
                file.write(
                    f"   Член {i + 1}: (({longest['distribution'][i]} - {longest['expected'][i]:.2f})² / {longest['expected'][i]:.2f}) = {longest['chi2_terms'][i]:.6f}\n"
                )
            file.write(f"   χ² = {longest['chi2']:.6f}\n\n")

            file.write("   " + calculate_p_value_for_longest_run(longest['chi2']) + "\n\n")


def main():
    """Основная функция"""
    results = {}

    if not os.path.exists("sequences"):
        os.makedirs("sequences")

    for gen_name, filepath in config.SEQUENCE_FILES.items():
        print(f"\n {gen_name} ")

        try:
            sequence = read_sequence_from_file(filepath)
            print(f"Файл загружен: {filepath}")
            print(f"Последовательность: {sequence[:32]}...{sequence[-32:]}")

            freq_result = frequency_test(sequence)
            runs_result = runs_test(sequence)
            longest_result = longest_run_test(sequence)

            ones_count = 0
            for bit in sequence:
                if bit == '1':
                    ones_count = ones_count + 1
            ones_pct = (ones_count / len(sequence)) * 100

            results[gen_name] = {
                'sequence': sequence,
                'frequency': freq_result,
                'runs': runs_result,
                'longest': longest_result,
                'ones_percent': ones_pct
            }

        except FileNotFoundError as e:
            print(f"Ошибка: {e}")
        except Exception as e:
            print(f"Неожиданная ошибка при обработке {gen_name}: {e}")

    if results:
        save_results_to_file(results, "results.txt")
        print(f"\nРезультаты сохранены в файл 'results.txt'")
        print(f"Сгенерированные последовательности сохранены в папке 'sequences/'")
    else:
        print("\nНет результатов для сохранения")


if __name__ == "__main__":
    main()