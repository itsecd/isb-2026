"""Модуль для работы с файлами."""

from pathlib import Path


def read_text(path: str) -> str:
    """
    Считать текст из файла.

    Args:
        path: Путь к файлу.

    Returns:
        Содержимое файла в виде строки.
    """
    return Path(path).read_text(encoding="utf-8")


def write_text(path: str, text: str) -> None:
    """
    Записать текст в файл.

    Args:
        path: Путь к выходному файлу.
        text: Текст для записи.
    """
    Path(path).write_text(text, encoding="utf-8")
