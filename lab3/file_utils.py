def read_bytes(file_path: str) -> bytes:
    """Читает бинарный файл."""
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
        print(f"Прочитан файл: {file_path}")
        return content
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл '{file_path}' не найден")
    except PermissionError:
        raise PermissionError(f"Нет прав на чтение файла '{file_path}'")


def read_text(file_path: str) -> str:
    """Читает текстовый файл в кодировке UTF-8."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"Прочитан файл: {file_path}")
        return content
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл '{file_path}' не найден")
    except PermissionError:
        raise PermissionError(f"Нет прав на чтение файла '{file_path}'")
    except UnicodeDecodeError:
        raise ValueError(f"Файл '{file_path}' не является текстовым в UTF-8")


def write_bytes(file_path: str, data: bytes) -> None:
    """Записывает бинарные данные в файл."""
    try:
        with open(file_path, 'wb') as f:
            f.write(data)
        print(f"Данные записаны в: {file_path}")
    except PermissionError:
        raise PermissionError(f"Нет прав на запись в '{file_path}'")


def write_text(file_path: str, content: str) -> None:
    """Записывает текст в файл."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Текст записан в: {file_path}")
    except PermissionError:
        raise PermissionError(f"Нет прав на запись в '{file_path}'")