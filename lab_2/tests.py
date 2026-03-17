import math

from scipy.special import gammaincc
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
    """Выполняет Runs Test (тест последовательностей)."""
    bit_list = [int(b) for b in bits]
    avg = sum(bit_list) / len(bit_list)

    if abs(avg - 0.5) > 2 / math.sqrt(len(bit_list)):
        return 0.0

    transitions = 0
    for i in range(len(bit_list) - 1):
        if bit_list[i] != bit_list[i + 1]:
            transitions += 1

    p_val = math.erfc(
        abs(transitions - 2 * len(bit_list) * avg * (1 - avg)) /
        (2 * math.sqrt(2 * len(bit_list)) * avg * (1 - avg))
    )

    return p_val


def longest_run_test(bits: str, block_size: int = 8) -> float:
    """Вычисляет среднюю длину максимальной серии единиц в блоках."""
    n = len(bits)
    num_blocks = n // block_size

    counts = [0, 0, 0, 0]

    for i in range(num_blocks):
        block = bits[i * block_size:(i + 1) * block_size]

        longest = 0
        current = 0

        for bit in block:
            if bit == "1":
                current += 1
                longest = max(longest, current)
            else:
                current = 0

        if longest <= 1:
            counts[0] += 1
        elif longest == 2:
            counts[1] += 1
        elif longest == 3:
            counts[2] += 1
        else:
            counts[3] += 1

    probabilities = [0.2148, 0.3672, 0.2305, 0.1875]

    chi_square = 0
    for i in range(4):
        expected = num_blocks * probabilities[i]
        chi_square += ((counts[i] - expected) ** 2) / expected

    df = 3
    p_value = gammaincc(df / 2, chi_square / 2)

    return p_value

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