import json

def read_file(filepath: str, mode: str = 'rb') -> bytes:
    """Read from the file.
        Args:
            filepath (str): Path to the file.
            mode (str): File mode.
        Returns:
            bytes: File contents.
        Raises:
            Input/Output error: if reading fails.
    """
    try:
        with open(filepath, mode) as f:
            return f.read()
    except Exception as e:
        raise IOError(f"Could not read from {filepath}: {e}")

def write_file(filepath: str, data, mode: str = 'wb') -> None:
    """Write in the file.
        Args:
            filepath (str): Path to the file.
            data (bytes): Data to write.
            mode (str): File mode.
        Returns:
            None
        Raises:
            Input/Output error: if writing fails.
        """
    try:
        with open(filepath, mode) as f:
            f.write(data)
    except Exception as e:
        raise IOError(f"Could not write in {filepath}: {e}")

def load_json(filepath: str) -> dict:
    """Loading JSON-config.
        Args:
            filepath (str): Path to the file.
        Returns:
            dict: JSON-config.
        Raises:
            Input/Output error: if loading fails.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise IOError(f"Could not load settings from {filepath}: {e}")