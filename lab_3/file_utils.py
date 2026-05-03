import json


def load_config(path: str) -> dict:
    """
    Загружает конфигурацию из JSON файла.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл конфигурации не найден: {path}")
    except json.JSONDecodeError:
        raise ValueError(f"Ошибка разбора JSON в файле: {path}")


def read_file(path: str, mode: str = "rb") -> bytes:
    try:
        with open(path, mode) as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {path}")
    except Exception as e:
        raise RuntimeError(f"Ошибка чтения файла {path}: {e}")


def write_file(path: str, data: bytes, mode: str = "wb") -> None:
    try:
        with open(path, mode) as f:
            f.write(data)
    except Exception as e:
        raise RuntimeError(f"Ошибка записи файла {path}: {e}")
