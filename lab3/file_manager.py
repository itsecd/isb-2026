import os

def read_binary(path):
    """
    Read .bin file
    Args:
        path: path to file
    Returns:
        file data
    Raises:
        FileNotFoundError: file not found
    """
    if not os.path.exists(path):
        raise FileNotFoundError("File not found: {path}")
    with open(path, "rb") as f:
        return f.read()

def write_binary(path, data):
    """
    Saving .bin file
    Args:
        path: path to save file
        data: data to write in file
    Raises:
        OSError: file saving error
    """
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(data)
    except OSError as e:
        raise OSError(f"File saving error {path}: {e}")
