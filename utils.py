import sys


def fail(message: str, code: int = 1) -> None:
    """
    Вывести сообщение об ошибке и завершить программу.

    Параметры:
        message: текст ошибки.
        code:    код возврата (по умолчанию 1).
    """
    print(message)
    sys.exit(code)


def read_file(path: str, mode: str = 'rb') -> bytes:
    """
    Прочитать файл с обработкой ошибок.

    Параметры:
        path: путь к файлу.
        mode: режим чтения ('rb' — бинарный по умолчанию, 'r' — текстовый).

    Возвращает:
        Содержимое файла.
    """
    try:
        with open(path, mode) as f:
            return f.read()
    except FileNotFoundError:
        fail(f"Файл не найден: {path}")
    except Exception as e:
        fail(f"Ошибка при чтении файла '{path}': {e}")


def write_file(path: str, data: bytes) -> None:
    """
    Записать данные в файл с обработкой ошибок.

    Параметры:
        path: путь к файлу.
        data: данные для записи (байты).
    """
    try:
        with open(path, 'wb') as f:
            f.write(data)
    except Exception as e:
        fail(f"Ошибка при записи файла '{path}': {e}")
