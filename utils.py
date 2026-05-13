import sys


def fail(message: str, code: int = 1) -> None:
    """Единая точка выхода с ошибкой."""
    print(message)
    sys.exit(code)


def read_file(path: str, mode: str = 'rb') -> bytes:
    """Чтение файла с обработкой ошибок."""
    try:
        with open(path, mode) as f:
            return f.read()
    except FileNotFoundError:
        fail(f"Файл не найден: {path}")
    except Exception as e:
        fail(f"Ошибка при чтении файла '{path}': {e}")


def write_file(path: str, data: bytes) -> None:
    """Запись файла с обработкой ошибок."""
    try:
        with open(path, 'wb') as f:
            f.write(data)
    except Exception as e:
        fail(f"Ошибка при записи файла '{path}': {e}")