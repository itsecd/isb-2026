import math
from scipy.special import gammaincc
from const import P_VALUE, BLOCK_SIZE, PI, SOURCE_FILES, OUTPUT_FILE


def read_sequence(filename: str) -> str:
    """Чтение последовательности из файла"""
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().strip()


def frequency_test(sequence: str) -> float:
    """Частотный побитовый тест"""
    n = len(sequence)
    ones = sequence.count("1")
    zeros = n - ones
    s_obs = abs(ones - zeros) / math.sqrt(n)
    return math.erfc(s_obs / math.sqrt(2))


def runs_test(sequence: str) -> float:
    """Тест на одинаковые подряд идущие '0' и '1'"""
    n = len(sequence)
    proportion = sequence.count("1") / n
    if abs(proportion - 0.5) > (2 / math.sqrt(n)):
        return 0.0
    transitions = sequence.count("01") + sequence.count("10")
    numerator = abs(transitions - (2 * n * proportion * (1 - proportion)))
    denominator = 2 * math.sqrt(2 * n) * proportion * (1 - proportion)
    return math.erfc(numerator / denominator)


def max_count_in_block(sequence: str) -> float:
    """Тест на самую длинную последовательность единиц в блоке"""
    counters = [0, 0, 0, 0]
    num_blocks = len(sequence) // BLOCK_SIZE

    for i in range(num_blocks):
        block = sequence[i * BLOCK_SIZE:(i + 1) * BLOCK_SIZE]
        longest = max(len(s) for s in block.split("0"))
        if longest <= 1:
            counters[0] += 1
        elif longest == 2:
            counters[1] += 1
        elif longest == 3:
            counters[2] += 1
        else:
            counters[3] += 1

    chi_sq = sum(((counters[i] - 16 * PI[i]) ** 2) / (16 * PI[i]) for i in range(4))
    return gammaincc(3 / 2, chi_sq / 2)


def analyze(name: str, seq: str):
    """Анализ последовательности по трем тестам"""
    return name, frequency_test(seq), runs_test(seq), max_count_in_block(seq)


def main() -> None:
    results = []
    for file in SOURCE_FILES:
        seq = read_sequence(file)
        name = file.split("_")[0].upper()
        results.append(analyze(name, seq))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write("Language | Frequency Test | Runs Test | Longest Run Test | Result\n")
        for name, p1, p2, p3 in results:
            status = "Passed" if all(x >= P_VALUE for x in [p1, p2, p3]) else "Failed"
            out.write(f"{name:<9}| {p1:<15.6f}| {p2:<10.6f}| {p3:<17.6f}| {status}\n")


if __name__ == "__main__":
    main()