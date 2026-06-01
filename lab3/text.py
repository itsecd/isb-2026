def read_text(path: str):
    """
    Read text from file.
    Args:
        path(str): Path to the file
    Returns:
        (bytes): file content as bytes
    Raises:
        OSError: Error reading data
        FileNotFoundError: File not found
        Exception: Unexpected error
    """
    try:
        with open(path, "rb") as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {path}")
    except OSError as e:
        raise OSError(f"Ошибка чтения файла: {e}")
    except Exception as e:
        raise Exception(f"Неожиданная ошибка при чтении файла: {e}")

def save_text(data: bytes, path: str):
    """
    Save bytes data to file.
    Args:
        path(str): Path to the file
        data(bytes): Data to save
    Raises:
        OSError: Error writing data
        Exception: Unexpected error
    """
    try:
        with open(path, "wb") as file:
            file.write(data)
    except OSError as e:
        raise OSError(f"Ошибка сохранения файла: {e}")
    except Exception as e:
        raise Exception(f"Неожиданная ошибка при сохранении файла: {e}")

def read_encrypted(path: str):
    """
    Read text from file.
    Args:
        path(str): Path to the file
    Returns:
        (bytes,bytes): iv and encrypted data
    Raises:
        OSError: Error reading data
        FileNotFoundError: File not found
        Exception: Unexpected error
    """
    try:
        with open(path, "rb") as f:
            iv = f.read(16)
            encrypted = f.read()
            return iv, encrypted
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {path}")
    except OSError as e:
        raise OSError(f"Ошибка чтения файла: {e}")
    except Exception as e:
        raise Exception(f"Неожиданная ошибка при чтении шифротекста: {e}")