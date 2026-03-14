import math
import config
from scipy.special import gammaincc
from datetime import datetime


def monobit_test(seq: str) -> tuple[bool, float]:
    """
    Частотный побитовый тест (Frequency Test).
    Проверяет соотношение единиц и нулей в последовательности.
    """
    n = len(seq)
    s_sum = sum(1 if bit == '1' else -1 for bit in seq)
    s_obs = abs(s_sum) / math.sqrt(n)
    p_value = math.erfc(s_obs / math.sqrt(2))
    return p_value >= config.ALPHA, p_value


def runs_test(seq: str) -> tuple[bool, float]:
    """
    Тест на одинаковые подряд идущие биты (Runs Test).
    Считает количество подряд идущих единиц и нулей.
    """
    n = len(seq)
    ones = seq.count('1')
    zeta = ones / n

    if abs(zeta - 0.5) >= 2.0 / math.sqrt(n):
        return False, 0.0

    v = 0.0
    for i in range(1, n):
        if seq[i] != seq[i-1]:
            v += 1

    expected = 2 * n * zeta * (1 - zeta)
    denom = 2 * math.sqrt(2 * n) * zeta * (1 - zeta)
    if denom == 0:
        return False, 0.0

    p_value = math.erfc(abs(v - expected) / denom)
    return p_value >= config.ALPHA, p_value


def longest_run_test(seq: str) -> tuple[bool, float]:
    """
    Тест на самую длинную последовательность единиц в блоке (Longest Run Test).
    """
    n = len(seq)
    m = config.M
    if n % m != 0:
        raise ValueError(f"Длина последовательности должна быть кратна {m}")

    num_blocks = n // m
    blocks = [seq[i*m:(i+1)*m] for i in range(num_blocks)]
    v = [0, 0, 0, 0]  

    for block in blocks:
        max_run = 0
        current = 0
        for bit in block:
            if bit == '1':
                current += 1
                max_run = max(max_run, current)
            else:
                current = 0
        if max_run <= 1:
            v[0] += 1
        elif max_run == 2:
            v[1] += 1
        elif max_run == 3:
            v[2] += 1
        else:
            v[3] += 1

    chi2 = 0.0
    for i in range(4):
        expected = num_blocks * config.PI[i]
        chi2 += (v[i] - expected) ** 2 / expected

    p_value = gammaincc(1.5, chi2 / 2)
    return p_value >= config.ALPHA, p_value


def load_sequence(filename: str) -> str:
    """Читает последовательность из файла (первая строка)."""
    with open(filename, 'r') as f:
        return f.readline().strip()


def print_result(name: str, p_value: float, is_random: bool) -> None:
    """Выводит результат одного теста на экран."""
    status = "СЛУЧАЙНА" if is_random else "НЕ СЛУЧАЙНА"
    print(f"{name:35} P-value = {p_value:.6f}  -> {status}")


def save_results_to_file(all_results: list, output_filename: str) -> str:
    """
    Сохраняет результаты всех тестов в файл отчёта.

    """
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("          ОТЧЁТ О СТАТИСТИЧЕСКИХ ТЕСТАХ NIST\n")
        f.write(f"          Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")

        total_tests = 0
        passed_tests = 0

        for file_label, tests in all_results:
            f.write(f"ФАЙЛ: {file_label}\n")
            f.write("-" * 50 + "\n")

            file_passed = 0
            for test_name, (passed, value) in tests:
                total_tests += 1
                if passed:
                    passed_tests += 1
                    file_passed += 1
                status = "УСПЕХ" if passed else "ПРОВАЛ"
                f.write(f"  {test_name:<30}  P-value = {value:.6f}  [{status}]\n")

            f.write(f"\n  Итого по файлу: {file_passed}/{len(tests)} тестов пройдено\n\n")

        f.write("=" * 60 + "\n")
        f.write("ИТОГОВАЯ СТАТИСТИКА\n")
        f.write("=" * 60 + "\n")
        f.write(f"Всего протестировано файлов: {len(all_results)}\n")
        f.write(f"Всего выполнено тестов: {total_tests}\n")
        f.write(f"Успешно пройдено: {passed_tests}\n")
        f.write(f"Неудачно: {total_tests - passed_tests}\n")
        if total_tests > 0:
            f.write(f"Общий процент успеха: {passed_tests/total_tests*100:.1f}%\n")

        if passed_tests == total_tests and total_tests > 0:
            f.write("\nВЫВОД: Все протестированные последовательности признаны случайными.\n")
        else:
            f.write("\nВЫВОД: Некоторые последовательности не прошли проверку на случайность.\n")

    return output_filename


def main() -> None:
    """Основная функция: загружает последовательности, запускает тесты, выводит и сохраняет результаты."""
    sequences = [
        ("C++ генератор", config.FILE_C),
        ("Java генератор", config.FILE_JAVA),
        ("Python генератор", config.FILE_PY)
    ]

    all_results = [] 

    print("=" * 75)
    print("РЕЗУЛЬТАТЫ СТАТИСТИЧЕСКОГО АНАЛИЗА (ТЕСТЫ NIST)")
    print("=" * 75)

    for name, filename in sequences:
        try:
            bits = load_sequence(filename)
        except FileNotFoundError:
            print(f"\n{name}: файл {filename} не найден. Пропускаем.")
            continue

        print(f"\n{name}:")
        print(f"Последовательность ({len(bits)} бит): {bits}")

        tests_for_file = []

        is_rand, p_freq = monobit_test(bits)
        print_result("  Частотный тест", p_freq, is_rand)
        tests_for_file.append(("Частотный тест", (is_rand, p_freq)))

        is_rand, p_runs = runs_test(bits)
        print_result("  Тест на подряд идущие биты", p_runs, is_rand)
        tests_for_file.append(("Тест на подряд идущие биты", (is_rand, p_runs)))

        if len(bits) % config.M == 0:
            is_rand, p_long = longest_run_test(bits)
            print_result("  Тест на самую длинную серию в блоке", p_long, is_rand)
            tests_for_file.append(("Тест на самую длинную серию в блоке", (is_rand, p_long)))
        else:
            print("  Тест на самую длинную серию: длина не кратна блоку, пропущен.")

        all_results.append((name, tests_for_file))

    print("\n" + "=" * 75)
    print("ВЫВОД: последовательность считается случайной, если все тесты вернули True.")
    print("=" * 75)

    if all_results:
        report_file = save_results_to_file(all_results, config.REPORT_FILE)
        print(f"\nПодробный отчёт сохранён в файл: {report_file}")
    else:
        print("\nНет данных для сохранения отчёта.")


if __name__ == "__main__":
    main()