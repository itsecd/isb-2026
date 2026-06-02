import os


def read_bytes(filepath: str) -> bytes:
    """Считывает и возвращает байты из файла."""
    with open(filepath, 'rb') as f:
        return f.read()


def save_to_file(filepath: str, data: bytes) -> str:
    """Сохраняет данные в файл по указанному пути."""
    os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
    with open(filepath, 'wb') as f:
        f.write(data)
    return filepath


def save_to_dir(directory: str, filename: str, data: bytes) -> str:
    """Сохраняет данные в указанную директорию."""
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    with open(filepath, 'wb') as f:
        f.write(data)
    return filepath