import os

def read_bytes(filepath: str) -> bytes:
    """
        Считывает и возвращает байты из файла
        Принимает: Путь к файлу
        Возвращает: Считанные байты (bytes)
    """
    with open(filepath, 'rb') as f:
        return f.read()

def save_to_file(filepath: str, data: bytes) -> str:
    """
        Сохраняет данные в файл по указанному пути, создавая необходимые директории
        Принимает: Путь к файлу, байты для сохранения
        Возвращает: Путь к сохраненному файлу
    """
    os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
    with open(filepath, 'wb') as f:
        f.write(data)
    return filepath

def save_to_dir(directory: str, filename: str, data: bytes) -> str:
    """
        Сохраняет данные в указанную директорию с заданным именем файла
        Принимает: Путь к директории, имя файла, байты для сохранения
        Возвращает: Полный путь к сохраненному файлу
    """
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    with open(filepath, 'wb') as f:
        f.write(data)
    return filepath