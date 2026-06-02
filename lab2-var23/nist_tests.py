import math
from scipy.special import gammaincc
from const import P_VALUE, BLOCK_SIZE, PI, SOURCE_FILES, OUTPUT_FILE


def bit_frequency_check(sequence: str) -> float:
    length = len(sequence)
    count_ones = sequence.count('1')
    count_zeros = length - count_ones

    statistic = abs(count_ones - count_zeros) / math.sqrt(length)
    return math.erfc(statistic / math.sqrt(2))


def consecutive_runs_check(sequence: str) -> float:
    length = len(sequence)
    count_ones = sequence.count('1')
    ratio = count_ones / length

    if abs(ratio - 0.5) > (2 / math.sqrt(length)):
        return 0.0

    transitions = sequence.count('01') + sequence.count('10')

    numerator = abs(transitions - 2 * length * ratio * (1 - ratio))
    denominator = 2 * math.sqrt(2 * length) * ratio * (1 - ratio)

    return math.erfc(numerator / denominator)


def max_run_check(sequence: str) -> float:
    counters = [0, 0, 0, 0]

    for block_index in range(len(sequence) // BLOCK_SIZE):
        block = sequence[
            BLOCK_SIZE * block_index:
            BLOCK_SIZE * block_index + BLOCK_SIZE
        ]

        longest = 0
        current = 0

        for bit in block:
            if bit == '1':
                current += 1
                longest = max(longest, current)
            else:
                current = 0

        if longest <= 1:
            counters[0] += 1
        elif longest == 2:
            counters[1] += 1
        elif longest == 3:
            counters[2] += 1
        else:
            counters[3] += 1

    chi_value = 0

    for i in range(4):
        chi_value += ((counters[i] - 16 * PI[i]) ** 2) / (16 * PI[i])

    return gammaincc(3 / 2, chi_value / 2)


def load_sequence(file_name: str) -> str:
    try:
        with open(file_name, encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Не удалось найти файл {file_name}")
        exit(1)


def check_status(values):
    return (
        "УСПЕШНО"
        if all(value >= P_VALUE for value in values[1:])
        else "НЕУСПЕШНО"
    )


def run_tests():
    cpp_data = load_sequence(SOURCE_FILES[0])
    java_data = load_sequence(SOURCE_FILES[1])
    python_data = load_sequence(SOURCE_FILES[2])

    cpp_stats = [
        "C++",
        bit_frequency_check(cpp_data),
        consecutive_runs_check(cpp_data),
        max_run_check(cpp_data)
    ]

    java_stats = [
        "Java",
        bit_frequency_check(java_data),
        consecutive_runs_check(java_data),
        max_run_check(java_data)
    ]

    py_stats = [
        "Python",
        bit_frequency_check(python_data),
        consecutive_runs_check(python_data),
        max_run_check(python_data)
    ]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write(
            "Язык     | Частота битов | Серии битов | Макс. серия | Итог\n"
        )
        file.write("-" * 80 + "\n")

        for result in [cpp_stats, java_stats, py_stats]:
            file.write(
                f"{result[0]:<8} | "
                f"{result[1]:.7f} | "
                f"{result[2]:.7f} | "
                f"{result[3]:.12f} | "
                f"{check_status(result)}\n"
            )

    print("\n" + "=" * 60)
    print("ОТЧЕТ ПО ТЕСТИРОВАНИЮ")
    print("=" * 60)
    print(
        f"{'Язык':<8} "
        f"{'Частота':<12} "
        f"{'Серии':<12} "
        f"{'Макс. серия':<18} "
        f"Статус"
    )
    print("-" * 60)

    for result in [cpp_stats, java_stats, py_stats]:
        print(
            f"{result[0]:<8} "
            f"{result[1]:.7f}   "
            f"{result[2]:.7f}   "
            f"{result[3]:.12f}   "
            f"{check_status(result)}"
        )

    print(f"\nОтчет записан в файл {OUTPUT_FILE}")


if __name__ == "__main__":
    run_tests()