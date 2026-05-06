import json


def load_config(path: str):
    """
    Загружает JSON-конфигурацию из файла.

    Parameters
    ----------
    path : str
        Путь к JSON-файлу конфигурации.

    Returns
    -------
    dict
        Словарь с конфигурацией.

    Raises
    ------
    FileNotFoundError
        Если файл конфигурации не найден.
    ValueError
        Если JSON некорректен.
    PermissionError
        Если нет прав на чтение файла.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Config file not found: {path}") from e

    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in config file: {path}") from e

    except PermissionError as e:
        raise PermissionError(f"No permission to read config file: {path}") from e


def read_bytes(path: str) -> bytes:
    """
    Читает файл в бинарном режиме.

    Parameters
    ----------
    path : str
        Путь к файлу.

    Returns
    -------
    bytes
        Содержимое файла в байтах.
    """
    with open(path, "rb") as f:
        return f.read()


def write_bytes(path: str, data: bytes) -> None:
    """
    Записывает байты в файл.

    Parameters
    ----------
    path : str
        Путь к файлу.
    data : bytes
        Данные для записи.
    """
    with open(path, "wb") as f:
        f.write(data)