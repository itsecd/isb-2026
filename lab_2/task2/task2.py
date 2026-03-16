import math
from pathlib import Path
from typing import List
from const import CONST_PI
from scipy.special import gammaincc


def read_from_file(filename: str) -> List[int]:
    """Функция для чтения бинарной последовательности из файла
    на вход принимает путь к файлу
    возвращает список битов (0 и 1)
    """
    numbers: List[int] = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for char in file.read():
                if char in ("0", "1"):
                    numbers.append(int(char))
    except IOError:
        print(f"Ошибка при открытии файла: {filename}")

    return numbers


def save_to_file(text: str, filename: str) -> None:
    """Функция для сохранения текста в файл
    на вход принимает текст и путь к файлу
    """
    file_path = Path(filename)
    dir_path = file_path.parent

    if not dir_path.exists():
        dir_path.mkdir(parents=True)
        print(f"Создана директория: {dir_path}")

    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(text)
        print(f"Результаты сохранены в файл: {filename}")
    except IOError:
        print(f"Ошибка при открытии файла: {filename}")


def vector_summ(numbers: List[int]) -> int:
    """Функция для вычисления суммы последовательности
    нули интерпретируются как -1, единицы как +1
    на вход принимает список битов
    возвращает сумму преобразованной последовательности
    """
    summ: int = 0

    for n in numbers:
        if n == 0:
            summ -= 1
        else:
            summ += 1

    return summ


def summary(numbers: List[int]) -> int:
    """Функция для подсчёта количества единиц
    на вход принимает список битов
    возвращает количество единиц
    """
    return sum(numbers)


def summary_V(numbers: List[int]) -> int:
    """Функция для подсчёта количества переходов между битами
    на вход принимает список битов
    возвращает количество переходов 0→1 или 1→0
    """
    summ: int = 0

    for i in range(len(numbers) - 1):
        if numbers[i] != numbers[i + 1]:
            summ += 1

    return summ


def test_1(numbers: List[int]) -> float:
    """Функция для выполнения Frequency (Monobit) теста
    на вход принимает бинарную последовательность
    возвращает P-value теста
    """
    N: int = len(numbers)
    summ: int = vector_summ(numbers)

    formula_S_n: float = (1.0 / math.sqrt(N)) * abs(summ)
    Pvalue: float = math.erfc(formula_S_n / math.sqrt(2))

    return Pvalue


def test_2(numbers: List[int]) -> float:
    """Функция для выполнения Runs теста
    на вход принимает бинарную последовательность
    возвращает P-value теста
    """
    N: int = len(numbers)

    summ: int = summary(numbers)
    V: int = summary_V(numbers)

    psi: float = (1.0 / N) * summ

    if abs(psi - 0.5) >= (2.0 / math.sqrt(N)):
        P_value: float = 0
    else:
        P_value = math.erfc(
            abs(V - 2 * N * psi * (1 - psi)) /
            (2 * math.sqrt(2 * N) * psi * (1 - psi))
        )

    return P_value


def test_3(bits: List[int]) -> float:
    """Функция для выполнения теста на самую длинную последовательность
    единиц в блоке (Longest Run of Ones Test)

    на вход принимает бинарную последовательность длиной 128 бит
    возвращает P-value теста
    """
    n: int = len(bits)

    if n != 128:
        raise ValueError("Для теста нужно ровно 128 бит!")

    m: int = 8
    v: List[int] = [0, 0, 0, 0]

    for i in range(16):

        block: List[int] = bits[i * m:(i + 1) * m]

        maxRun: int = 0
        currentRun: int = 0

        for bit in block:

            if bit == 1:
                currentRun += 1
                maxRun = max(maxRun, currentRun)
            else:
                currentRun = 0

        if maxRun <= 1:
            v[0] += 1
        elif maxRun == 2:
            v[1] += 1
        elif maxRun == 3:
            v[2] += 1
        else:
            v[3] += 1

    chiSquared: float = 0

    for i in range(4):
        expected: float = 16 * CONST_PI[i]
        chiSquared += ((v[i] - expected) ** 2) / expected

    pValue: float = gammaincc(3/2, chiSquared/2)

    return pValue


def process_file(filename: str, file_label: str) -> str:
    """Функция для обработки файла с бинарной последовательностью
    на вход принимает путь к файлу и имя файла для отображения
    возвращает строку с результатами тестов
    """
    result: str = ""

    result += "\n======================================\n"
    result += f"Обработка файла: {file_label}\n"
    result += f"Читаем файл из: {filename}\n"

    numbers: List[int] = read_from_file(filename)

    if not numbers:
        result += "Вектор пуст! Пропускаем файл.\n"
        return result

    result += f"Размер последовательности: {len(numbers)} бит\n"

    result += "Первые 50 бит: "
    result += "".join(map(str, numbers[:50]))

    if len(numbers) > 50:
        result += "..."

    result += "\n"

    test1: float = test_1(numbers)
    test2: float = test_2(numbers)
    test3: float = test_3(numbers)

    result += "\nРезультаты тестов:\n"
    result += f"Test 1: P-value = {test1}\n"
    result += f"Test 2: P-value = {test2}\n"
    result += f"Test 3: P-value = {test3}\n"

    result += "\nИнтерпретация результатов (при уровне значимости 0.01):\n"
    result += "Test 1: " + ("НЕ РАНДОМНАЯ\n" if test1 < 0.01 else "рандомизированная\n")
    result += "Test 2: " + ("НЕ РАНДОМНАЯ\n" if test2 < 0.01 else "рандомизированная\n")
    result += "Test 3: " + ("НЕ РАНДОМНАЯ\n" if test3 < 0.01 else "рандомизированная\n")

    return result


def main() -> None:
    """Основная функция программы
    выполняет загрузку файлов, запуск тестов
    и сохранение результатов
    """
    source_dir: Path = Path(__file__).resolve().parent
    lab2_path: Path = source_dir.parent

    filename_cpp: Path = lab2_path / "task2" / "sequence_c++.txt"
    filename_java: Path = lab2_path / "task2" / "sequence_java.txt"

    results: str = ""

    results += process_file(filename_cpp, "sequence_c++.txt")
    results += process_file(filename_java, "sequence_java.txt")

    results += "\n======================================\n"
    results += "Обработка всех файлов завершена.\n"

    result_file: Path = lab2_path / "task2" / "tests_result.txt"

    save_to_file(results, result_file)


if __name__ == "__main__":
    main()