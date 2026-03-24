import math
from scipy.special import gammaincc


def read_sequence(filename: str) -> str:
    """
    Считывает бинарную последовательность из текстового файла.
    """
    with open(filename, 'r') as f:
        return f.readline().strip()


def monobit_test(seq: str):
    """
    Частотный побитовый тест
    """
    n = len(seq)
    s_sum = sum(1 if b == '1' else -1 for b in seq)
    s_n = abs(s_sum) / math.sqrt(n)
    p_value = math.erfc(s_n / math.sqrt(2))
    return p_value, p_value >= 0.01


def runs_test(seq: str):
    """
    Тест на серии
    """
    n = len(seq)
    ones = seq.count('1')
    zeta = ones / n

    if abs(zeta - 0.5) >= 2.0 / math.sqrt(n):
        return 0.0

    v_n = 0
    for i in range(n - 1):
        if seq[i] != seq[i + 1]:
            v_n += 1

    p_value = math.erfc(abs(v_n - 2 * n * zeta * (1 - zeta)) / (2 * math.sqrt(2 * n) * zeta * (1 - zeta)))
    return p_value, p_value >= 0.01


def longest_run_test(seq: str):
    """
    Тест на самую длинную последовательность единиц в блоке.
    """
    M, N = 8, 16
    blocks = [seq[i*M:(i+1)*M] for i in range(N)]

    longest = []
    for blk in blocks:
        cur = max_run = 0
        for b in blk:
            if b == '1':
                cur += 1
                max_run = max(max_run, cur)
            else:
                cur = 0
        longest.append(max_run)

    freq = [0, 0, 0, 0]
    for l in longest:
        if l <= 1:
            freq[0] += 1
        elif l == 2:
            freq[1] += 1
        elif l == 3:
            freq[2] += 1
        else:
            freq[3] += 1

    expected_prob = [0.2148, 0.3672, 0.2305, 0.1875]
    expected = [p * N for p in expected_prob]

    chi_sq = sum((f - e) ** 2 / e for f, e in zip(freq, expected))

    p_value = gammaincc(3/2, chi_sq / 2)
    return p_value, p_value >= 0.01


def build_report_lines(sequence_files: dict) -> list:
    """
    Формирует список строк с результатами тестирования для всех языков.
    """
    lines = []
    for lang, fname in sequence_files.items():
        lines.append(f"--- {lang} ---")
        try:
            seq = read_sequence(fname)

            p_mono, res_mono = monobit_test(seq)
            lines.append(f"Monobit test:      p-value = {p_mono:.6f} -> {'ПРОЙДЕН' if res_mono else 'НЕ ПРОЙДЕН'}")

            p_runs, res_runs = runs_test(seq)
            if p_runs == 0.0:
                lines.append("Runs test:         не применим (доля единиц далека от 0.5)")
            else:
                lines.append(f"Runs test:          p-value = {p_runs:.6f} -> {'ПРОЙДЕН' if res_runs else 'НЕ ПРОЙДЕН'}")

            p_long, res_long = longest_run_test(seq)
            lines.append(f"Longest run test:   p-value = {p_long:.6f} -> {'ПРОЙДЕН' if res_long else 'НЕ ПРОЙДЕН'}")

            lines.append("")

        except FileNotFoundError:
            lines.append(f"Файл {fname} не найден. Сгенерируйте последовательность.\n")
        except ValueError as e:
            lines.append(f"Ошибка: {e}\n")
    return lines


def main():

    SEQUENCE_FILES = {
        'C++': 'sequence_cpp.txt',
        'Java': 'sequence_java.txt',
        'Python': 'sequence_py.txt'
    }
    RESULT_FILE = 'results.txt'

    report_lines = build_report_lines(SEQUENCE_FILES)

    with open(RESULT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))


if __name__ == '__main__':
    main()
