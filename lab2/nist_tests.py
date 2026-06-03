import math
from collections import Counter
from scipy.special import gammaincc


def read_bits(filename: str) -> str:
    """
    Чтение бинарной последовательности из файла.

    Args:
        filename (str): путь к файлу

    Returns:
        str: строка из 0 и 1

    Raises:
        FileNotFoundError: если файл не найден
        ValueError: если файл пустой
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = f.read().strip()

        if not data:
            raise ValueError(f"Файл {filename} пустой")

        return data

    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {filename} не найден")


def frequency_test(bits: str) -> float:
    """
    Частотный побитовый тест NIST.

    Проверяет баланс нулей и единиц.

    Returns:
        float: p-value
    """
    n = len(bits)
    ones = bits.count("1")
    zeros = bits.count("0")

    s = abs(ones - zeros) / math.sqrt(n)
    return math.erfc(s / math.sqrt(2))


def runs_test(bits: str) -> float:
    """
    Тест серий (runs test).

    Проверяет количество переходов между 0 и 1.

    Returns:
        float: p-value
    """
    n = len(bits)
    pi = bits.count("1") / n

    if abs(pi - 0.5) >= 2 / math.sqrt(n):
        return 0.0

    runs = 1

    for i in range(1, n):
        if bits[i] != bits[i - 1]:
            runs += 1

    num = abs(runs - 2 * n * pi * (1 - pi))
    den = 2 * math.sqrt(2 * n) * pi * (1 - pi)

    return math.erfc(num / den)


def longest_run_test(bits: str) -> float:
    """
    Тест на самую длинную серию единиц в блоках по 8 бит.

    Returns:
        float: p-value
    """
    block_size = 8
    blocks = [bits[i:i + block_size] for i in range(0, len(bits), block_size)]

    longest = []

    for block in blocks:
        current = 0
        best = 0

        for b in block:
            if b == "1":
                current += 1
                best = max(best, current)
            else:
                current = 0

        longest.append(best)

    categories = []

    for x in longest:
        if x <= 1:
            categories.append(0)
        elif x == 2:
            categories.append(1)
        elif x == 3:
            categories.append(2)
        else:
            categories.append(3)

    counts = Counter(categories)
    observed = [counts.get(i, 0) for i in range(4)]

    probs = [0.2148, 0.3672, 0.2305, 0.1875]

    n_blocks = len(blocks)

    chi = 0.0

    for o, p in zip(observed, probs):
        chi += ((o - n_blocks * p) ** 2) / (n_blocks * p)

    return gammaincc(1.5, chi / 2)


def analyze(filename: str) -> str:
    """
    Выполняет все NIST тесты для файла
    и формирует отчёт.

    Args:
        filename (str): имя файла

    Returns:
        str: результат анализа
    """
    try:
        bits = read_bits(filename)

        freq = frequency_test(bits)
        runs = runs_test(bits)
        longest = longest_run_test(bits)

        return (
            f" {filename} \n"
            f"Длина последовательности: {len(bits)}\n"
            f"Частотный побитовый тест (p-value): {freq}\n"
            f"Тест на одинаковые подряд идущие биты (p-value): {runs}\n"
            f"Тест на самую длинную последовательность единиц в блоке (p-value): {longest}\n\n"
        )

    except Exception as e:
        return f"Ошибка при обработке {filename}: {str(e)}\n\n"


if __name__ == "__main__":

    files = [
        "cpp_sequence.txt",
        "java_sequence.txt",
        "py_sequence.txt"
    ]

    result = ""

    for f in files:
        text = analyze(f)
        print(text)
        result += text

    try:
        with open("results.txt", "w", encoding="utf-8") as out:
            out.write(result)
    except Exception as e:
        print(f"Ошибка записи результата: {e}")

    print("Готово: results.txt создан")
