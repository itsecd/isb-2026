def read_file(path: str, mode: str = 'rb') -> bytes:
    """Прочитать файл с обработкой ошибок."""
    try:
        with open(path, mode) as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {path}") from None
    except Exception as e:
        raise RuntimeError(f"Ошибка при чтении файла '{path}': {e}") from e

def write_file(path: str, data: bytes) -> None:
    """Записать данные в файл с обработкой ошибок."""
    try:
        with open(path, 'wb') as f:
            f.write(data)
    except Exception as e:
        raise RuntimeError(f"Ошибка при записи файла '{path}': {e}") from e
