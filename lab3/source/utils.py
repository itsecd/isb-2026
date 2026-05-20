import json


def load_config(path: str):
    """
    Загружает JSON-конфигурацию из файла.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"Config file not found: {path}"
        ) from e

    except json.JSONDecodeError as e:
        raise ValueError(
            f"Invalid JSON in config file: {path}"
        ) from e

    except PermissionError as e:
        raise PermissionError(
            f"No permission to read config file: {path}"
        ) from e

    except Exception as e:
        raise Exception(
            f"Unexpected error while loading config '{path}': {e}"
        ) from e


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

    Raises
    ------
    FileNotFoundError
        Если файл не найден.
    PermissionError
        Если нет прав на чтение.
    OSError
        При других ошибках ввода-вывода.
    """
    try:
        with open(path, "rb") as f:
            return f.read()

    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {path}") from e

    except PermissionError as e:
        raise PermissionError(f"No permission to read file: {path}") from e

    except OSError as e:
        raise OSError(f"Failed to read file: {path}") from e


def write_bytes(path: str, data: bytes) -> None:
    """
    Сохраняет бинарные данные в файл.

    Parameters
    ----------
    path : str
        Путь к файлу.
    data : bytes
        Данные для записи.
    """
    try:
        with open(path, "wb") as f:
            f.write(data)

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Invalid path for output file: {path}") from e

    except PermissionError as e:
        raise PermissionError(f"No permission to write file: {path}") from e

    except OSError as e:
        raise OSError(f"Failed to write bytes to file: {path}") from e
