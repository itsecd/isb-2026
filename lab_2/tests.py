import math
from typing import List, Tuple


def read_sequence(filename: str) -> List[int]:
    """
    Читает бинарную последовательность из файла.

    Args:
        filename: Имя файла с последовательностью

    Returns:
        Список целых чисел (0 и 1)

    Raises:
        FileNotFoundError: Если файл не найден
        ValueError: Если данные в файле некорректны
    """
    try:
        with open(filename, 'r') as f:
            line = f.readline().strip()

        bits = []
        for char in line:
            if char == '0':
                bits.append(0)
            elif char == '1':
                bits.append(1)
            else:
                raise ValueError(f"Некорректный символ в файле: {char}")

        if not bits:
            raise ValueError("Файл пуст")

        return bits

    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {filename} не найден")


def frequency_test(seq: List[int]) -> None:
    """
    Частотный побитовый тест.

    Проверяет, соответствует ли доля единиц и нулей в последовательности
    ожидаемой для случайной последовательности.

    Args:
        seq: Последовательность битов
    """
    n = len(seq)
    x_i = [1 if bit == 1 else -1 for bit in seq]
    x = abs(sum(x_i))
    s_n = x / math.sqrt(n)
    p_value = math.erfc(s_n / math.sqrt(2))

    print(f"\nЧастотный побитовый тест:")
    print(f"Единиц: {sum(seq)}, Нулей: {n - sum(seq)}")
    print(f"S_n = {s_n:.6f}")
    print(f"P_value = {p_value:.6f}")
    print(f"Результат: {'Случайна' if p_value >= 0.01 else 'НЕ случайна'}")


def runs_test(seq: List[int]) -> None:
    """
    Тест на одинаковые подряд идущие биты.

    Проверяет, соответствует ли количество смен битов (знакоперемен)
    ожидаемому для случайной последовательности.

    Args:
        seq: Последовательность битов
    """
    n = len(seq)
    e = sum(seq)
    z = e / n

    print(f"\nТест на одинаковые подряд идущие биты:")

    if abs(z - 1/2) < 2 / math.sqrt(n):
        v_n = sum(1 for i in range(n - 1) if seq[i] != seq[i + 1])
        p_value = math.erfc(
            abs(v_n - 2 * n * z * (1 - z)) /
            (2 * math.sqrt(2 * n) * z * (1 - z))
        )

        print(f"Число знакоперемен: {v_n}")
        print(f"P_value = {p_value:.6f}")
    else:
        p_value = 0
        print("P_value = 0")

    print(f"Результат: {'Случайна' if p_value >= 0.01 else 'НЕ случайна'}")


def longest_run_test(seq: List[int]) -> None:
    """
    Тест на самую длинную последовательность единиц в блоке.

    Проверяет, соответствует ли распределение длин максимальных
    последовательностей единиц в блоках ожидаемому.

    Args:
        seq: Последовательность битов
    """
    n = len(seq)
    m = 8

    # Категории: ≤1, 2, 3, ≥4
    v = [0, 0, 0, 0]

    for i in range(n // m):
        block = seq[i * m:(i + 1) * m]
        max_run = _find_max_run_in_block(block)

        if max_run <= 1:
            v[0] += 1
        elif max_run == 2:
            v[1] += 1
        elif max_run == 3:
            v[2] += 1
        else:
            v[3] += 1

    pi = [0.2148, 0.3672, 0.2305, 0.1875]

    x_square = 0
    for i in range(4):
        expected = (n // m) * pi[i]
        x_square += ((v[i] - expected) ** 2) / expected

    s = (4 - 1) / 2  # параметр формы = 1.5
    x = x_square / 2  # нижний предел

    print(f"\nТест на самую длинную последовательность единиц в блоке:")
    print(f"Распределение по блокам: v_1:{v[0]}, v_2:{v[1]}, v_3:{v[2]}, v_4:{v[3]}")
    print(f"χ² = {x_square:.6f}")
    print(f"Параметр формы (s) = {s}")
    print(f"Нижний предел (x) = {x:.6f}")
    print(f"Калькулятор: https://www.danielsoper.com/statcalc/calculator.aspx?id=34")


def _find_max_run_in_block(block: List[int]) -> int:
    """
    Находит максимальную длину последовательности единиц в блоке.

    Args:
        block: Блок битов

    Returns:
        Максимальная длина последовательности единиц
    """
    max_run = 0
    current = 0

    for bit in block:
        if bit == 1:
            current += 1
            max_run = max(max_run, current)
        else:
            current = 0

    return max_run


def get_filename() -> str:
    """
    Ввод имени файла с консоли.

    Returns:
        Имя файла

    Raises:
        ValueError: Если введена пустая строка
    """
    filename = input("Введите имя файла с последовательностью: ").strip()
    if not filename:
        raise ValueError("Имя файла не может быть пустым")
    return filename


def main() -> None:
    """
    Основная функция программы.
    """
    try:
        filename = get_filename()
        seq = read_sequence(filename)
        print(f"Последовательность длиной n = {len(seq)} бит")

        frequency_test(seq)
        runs_test(seq)
        longest_run_test(seq)

    except (FileNotFoundError, ValueError) as exc:
        print(f"Ошибка: {exc}")


if __name__ == "__main__":
    main()