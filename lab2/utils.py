import os
import math

def read_sequence(filename):
    """Читает битовую последовательность из файла."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            sequence = ''.join(content.split())
            return sequence
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None

def save_result(filename, sequence_name, test_name, p_value, result):
    """Сохраняет результат теста в файл."""
    os.makedirs("results", exist_ok=True)
    with open(f"results/{filename}", 'a', encoding='utf-8') as f:
        f.write(f"Последовательность: {sequence_name}\n")
        f.write(f"Тест: {test_name}\n")
        f.write(f"P-value: {p_value:.6f}\n")
        f.write(f"Результат: {'СЛУЧАЙНАЯ' if result else 'НЕ СЛУЧАЙНАЯ'}\n")
        f.write("-" * 50 + "\n")

def erfc(x):
    """Дополнительная функция ошибок."""
    from math import erfc as math_erfc
    return math_erfc(x)

def igamc(a, x):
    """Неполная гамма-функция (верхняя)."""
    try:
        from scipy.special import gammaincc
        return gammaincc(a, x)
 