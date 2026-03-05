"""Константы для тестов NIST"""
import os

# Параметры последовательности
SEQUENCE_LENGTH = 128
"""int: Длина тестируемой последовательности в битах."""

# Пороговые значения
ALPHA = 0.01
"""float: Уровень значимости для принятия решения (Pvalue >= ALPHA означает случайность)."""

# Параметры для теста на самую длинную последовательность единиц
BLOCK_SIZE = 8
"""int: Длина блока для разбиения последовательности."""

# Теоретические вероятности для теста на самую длинную последовательность
PI_VALUES = [0.2148, 0.3672, 0.2305, 0.1875]
"""list[float]: Теоретические вероятности для распределения длин последовательностей единиц."""

# Пути к файлам с последовательностями
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SEQUENCE_FILES = {
    "C++ (mt19937)": os.path.join(BASE_DIR, "sequences", "sequence_cpp.txt"),
    "Java (java.util.Random)": os.path.join(BASE_DIR, "sequences", "sequence_java.txt"),
    "Python (random)": os.path.join(BASE_DIR, "sequences", "sequence_python.txt")
}
"""dict: Пути к файлам с последовательностями от разных генераторов."""