def read_file(path: str, mode: str = 'rb') -> bytes:
    """Прочитать содержимое файла.
    Args:
        path: Путь к файлу.
        mode: Режим открытия ('rb' по умолчанию, 'r' для текста).
    Returns:
        Содержимое файла в виде байтов.
    Raises:
        FileNotFoundError: Если указанный файл не найден.
        RuntimeError: При других ошибках ввода-вывода или прав доступа.
    """
    try:
        with open(path, mode) as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {path}") from None
    except Exception as e:
        raise RuntimeError(f"Ошибка при чтении файла '{path}': {e}") from e

def write_file(path: str, data: bytes) -> None:
    """Записать данные в файл.
    Args:
        path: Путь к файлу для записи.
        data: Байтовые данные для записи.
    Raises:
        RuntimeError: При ошибках записи (нет прав, место на диске и т.д.).
    """
    try:
        with open(path, 'wb') as f:
            f.write(data)
    except Exception as e:
        raise RuntimeError(f"Ошибка при записи файла '{path}': {e}") from e
