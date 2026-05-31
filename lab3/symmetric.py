def serialize_symmetric_key(encrypted_symmetric_key: bytes, path: str):
    """
    Save encrypted symmetric key to file
    Args:
        encrypted_symmetric_key(bytes): encrypted symmetric key
        path(str): save path for the key
    Raises:
        OSError: Error writing data
    """
    try:
        with open(path, "wb") as key_file:
            key_file.write(encrypted_symmetric_key)
    except OSError as e:
        raise OSError(f"Ошибка сохранения файла: {e}")

def deserialize_encrypted_key(symmetric_key_path: str) -> bytes:
    """
    Read encrypted symmetric key from file
    Args:
        path(str): read path for the encrypted symmetric key
    Returns:
        (bytes): encrypted symmetric key
    Raises:
        OSError: Error reading data
        FileNotFoundError: File not found
    """
    try:
        with open(symmetric_key_path, "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Симметричный ключ не найден: {symmetric_key_path}")
    except OSError as e:
        raise OSError(f"Ошибка чтения файла: {e}")

