import json


def read_file(path: str, mode: str = "rb") -> bytes:
    """
    Читает файл.

    :param path: путь
    :param mode: режим
    :return: содержимое файла
    """
    with open(path, mode) as f:
        return f.read()


def write_file(path: str, data: bytes, mode: str = "wb") -> None:
    """
    Записывает файл.

    :param path: путь
    :param data: данные
    """
    with open(path, mode) as f:
        f.write(data)


def load_config() -> dict:
    """
    Загружает настройки из settings.json.

    :return: dict
    :raises Exception: если ошибка чтения
    """
    with open("settings.json", "r", encoding="utf-8") as f:
        return json.load(f)
