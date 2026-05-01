import os


def serialize_data(path: str, data: bytes):
    """
    Запись двоичных данных в файл.
    """
    try:
        with open(path, 'wb') as f:
            f.write(data)
    except Exception as e:
        raise RuntimeError(f"Ошибка написания в {path}: {e}")


def deserialize_data(path: str):
    """
    Чтение двоичных данных из файла.
    """
    try:
        with open(path, 'rb') as f:
            return f.read()
    except Exception as e:
        raise RuntimeError(f"Ошибка чтения {path}: {e}")