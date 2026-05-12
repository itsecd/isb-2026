import json

def read_bytes(path: str) -> bytes:
    """Прочтение файла в байтовом режиме.
    Args:
        path: Путь к файлу, который нужно прочитать.
    """
    try:
        with open(path, "rb") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Файл не найден: {path}")
        raise
    except PermissionError:
        print(f"Нет прав на чтение файла: {path}")
        raise
    except OSError as e:
        print(f"Ошибка при чтении файла {path}: {e}")
        raise


def write_bytes(path: str, data: bytes) -> None:
    """Запись байтов в файл.
    Args:
        path: Путь к файлу, в который будут записаны данные.
        data: Байтовые данные для записи.
    """
    try:
        with open(path, "wb") as f:
            f.write(data)
    except PermissionError:
        print(f"Нет прав на запись в файл: {path}")
        raise
    except FileNotFoundError:
        print(f"Директория для файла не существует: {path}")
        raise
    except OSError as e:
        print(f"Ошибка при записи файла {path}: {e}")
        raise


def read_text(path: str, encoding: str = "utf-8") -> str:
    """Прочтение текстового файла.
    Args:
        path: Путь к текстовому файлу, который нужно прочитать.
        encoding: Кодировка файла. По умолчанию "utf-8".
    """
    try:
        with open(path, "r", encoding=encoding) as f:
            return f.read()
    except FileNotFoundError:
        print(f"Файл не найден: {path}")
        raise
    except UnicodeDecodeError as e:
        print(f"Файл {path} не соответствует кодировке {encoding}: {e}")
        raise
    except OSError as e:
        print(f"Ошибка при чтении файла {path}: {e}")
        raise


def load_settings(path: str = "settings.json") -> dict:
    """Загрузка настроек из JSON-файла.
    Args:
        path: Путь к JSON-файлу с настройками. По умолчанию "settings.json".
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл настроек не найден: {path}")
        raise
    except json.JSONDecodeError as e:
        print(f"Некорректный JSON в файле {path}: {e}")
        raise
    except OSError as e:
        print(f"Ошибка при чтении файла настроек {path}: {e}")
        raise