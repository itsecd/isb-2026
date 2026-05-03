def write_binary_file(filepath: str, data: bytes):
    """Универсальная функция записи в бинарный файл"""
    try:
        with open(filepath, 'wb') as f:
            f.write(data)
    except IOError as e:
        raise IOError(f"Ошибка при записи в файл {filepath}: {e}")


def read_binary_file(filepath: str) -> bytes:
    """Универсальная функция чтения из бинарного файла"""
    try:
        with open(filepath, 'rb') as f:
            return f.read()
    except IOError as e:
        raise IOError(f"Ошибка при чтении файла {filepath}: {e}")


def read_text_file(filepath: str) -> bytes:
    """Универсальная функция чтения текстового файла в бинарном режиме"""
    try:
        with open(filepath, 'rb') as f:
            return f.read()
    except IOError as e:
        raise IOError(f"Ошибка при чтении файла {filepath}: {e}")