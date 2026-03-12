import math

from pathlib import Path
from const import BLOCK_SIZE, FILES, OUTPUT_FILE


def load_bits(path: str) -> str:
    """Считывает строку битов из файла."""
    with open(path, "r", encoding="utf-8") as file:
        return file.read().strip()


def frequency_test(bits: str) -> float:
    """Выполняет частотный (monobit) тест случайности."""
    n = len(bits)

    s = sum(1 if bit == "1" else -1 for bit in bits)
    s_obs = abs(s) / math.sqrt(n)

    return math.erfc(s_obs / math.sqrt(2))


def runs_test(bits: str) -> float:
    """Выполняет тест последовательностей (runs test)."""
    n = len(bits)
    pi = bits.count("1") / n

    if abs(pi - 0.5) >= 2 / math.sqrt(n):
        return 0.0

    v = 1
    for i in range(1, n):
        if bits[i] != bits[i - 1]:
            v += 1

    numerator = abs(v - 2 * n * pi * (1 - pi))
    denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)

    return math.erfc(numerator / denominator)


def longest_run_test(bits: str, block_size: int = BLOCK_SIZE) -> float:
    """Вычисляет среднюю длину максимальной серии единиц в блоках."""
    n = len(bits)
    num_blocks = n // block_size

    longest_runs = []

    for i in range(num_blocks):
        block = bits[i * block_size:(i + 1) * block_size]

        max_run = 0
        current_run = 0

        for bit in block:
            if bit == "1":
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 0

        longest_runs.append(max_run)

    return sum(longest_runs) / len(longest_runs)


def run_tests(file_path: str, output_path: str) -> None:
    """Запускает тесты случайности для файла с битовой последовательностью."""
    bits = load_bits(file_path)

    freq_result = frequency_test(bits)
    runs_result = runs_test(bits)
    longest_result = longest_run_test(bits)

    result = (
        f"File: {file_path}\n"
        f"Frequency test p-value: {freq_result}\n"
        f"Runs test p-value: {runs_result}\n"
        f"Longest run average: {longest_result}\n"
        + "-" * 40
        + "\n"
    )

    print(result)

    with open(output_path, "a", encoding="utf-8") as file:
        file.write(result)


def main() -> None:
    """Точка входа программы."""
    Path(OUTPUT_FILE).write_text("", encoding="utf-8")

    for file_path in FILES:
        run_tests(file_path, OUTPUT_FILE)


if __name__ == "__main__":
    main()