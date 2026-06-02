import json
from exceptions import FileProcessingError


def load_json(path: str) -> dict:
    """
    Загружает и парсит JSON-файл.

    :param path: Путь к JSON-файлу.
    :return: Словарь с данными из файла.
    :raises FileProcessingError: Если файл не найден,
                                 нечитаем или содержит некорректный JSON.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise FileProcessingError(f"Ошибка загрузки JSON из {path}: {e}") from e


def read_bytes(path: str) -> bytes:
    """
    Читает файл в бинарном режиме.

    :param path: Путь к файлу.
    :return: Содержимое файла в виде байтовой строки.
    :raises FileProcessingError: Если файл не найден или не удалось прочитать.
    """
    try:
        with open(path, "rb") as f:
            return f.read()
    except Exception as e:
        raise FileProcessingError(f"Ошибка чтения бинарного файла {path}: {e}") from e


def write_bytes(path: str, data: bytes) -> None:
    """
    Записывает байтовые данные в файл (создавая или перезаписывая его).

    :param path: Путь к выходному файлу.
    :param data: Байтовая строка для записи.
    :raises FileProcessingError: Если не удалось создать или записать файл.
    """
    try:
        with open(path, "wb") as f:
            f.write(data)
    except Exception as e:
        raise FileProcessingError(f"Ошибка записи бинарного файла {path}: {e}") from e


def load_settings(path: str) -> dict:
    """
    Загружает настройки из JSON-файла.

    :param path: Путь к settings.json.
    :return: Словарь настроек.
    :raises FileProcessingError: При ошибке загрузки.
    """
    return load_json(path)
