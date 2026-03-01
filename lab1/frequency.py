"""Модуль для частотного анализа текста."""

from collections import Counter


def calculate_frequencies(text: str) -> dict:
    """
    Вычислить частоты символов в тексте.

    Частота считается как отношение количества
    символа к общему количеству символов в тексте.

    Args:
        text: Анализируемый текст.

    Returns:
        Словарь вида {символ: частота}.
    """
    counter = Counter(text)
    total = len(text)

    frequencies = {}

    for char, count in counter.items():
        frequencies[char] = count / total

    return frequencies


def save_frequencies(freq: dict, path: str) -> None:
    """
    Сохранить частоты символов в файл.

    Args:
        freq: Словарь частот.
        path: Путь к файлу для сохранения.
    """
    sorted_items = sorted(freq.items(), key=lambda item: item[1], reverse=True)

    lines = [f"{char}:{value:.6f}" for char, value in sorted_items]

    with open(path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))
