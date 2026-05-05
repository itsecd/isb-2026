import os


def serialize_data(path: str, data: bytes):
    """
    Запись двоичных данных в файл.

    Args:
        path: Путь к файлу для записи.
        data: Данные для сохранения в байтовом формате.

    Raises:
        RuntimeError: Ошибка при открытии файла или записи данных.
    """
    try:
        with open(path, 'wb') as f:
            f.write(data)
    except Exception as e:
        raise RuntimeError(f"Ошибка написания в {path}: {e}")


def deserialize_data(path: str):
    """
    Чтение двоичных данных из файла.

    Args:
        path: Путь к файлу для чтения.

    Returns:
        Содержимое файла в виде байтовой строки.

    Raises:
        RuntimeError: Ошибка при чтении, либо файл не найден.
    """
    try:
        with open(path, 'rb') as f:
            return f.read()
    except Exception as e:
        raise RuntimeError(f"Ошибка чтения {path}: {e}")