"""Вспомогательные функции для бинарного чтения и записи файлов."""

from pathlib import Path


def read_bytes(path: str) -> bytes:
    """Читает файл как последовательность байтов.

    Аргументы:
        path: Путь к исходному файлу.

    Возвращает:
        Содержимое файла.
    """
    return Path(path).read_bytes()


def write_bytes(path: str, data: bytes) -> None:
    """Записывает байты в файл и создает родительские каталоги при необходимости.

    Аргументы:
        path: Путь для сохранения файла.
        data: Данные для записи.
    """
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
