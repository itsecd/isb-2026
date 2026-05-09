import json

def read_file(filepath: str, mode: str = 'rb') -> bytes:
    """Read from the file."""
    try:
        with open(filepath, mode) as f:
            return f.read()
    except Exception as e:
        raise IOError(f"Could not read from {filepath}: {e}")

def write_file(filepath: str, data, mode: str = 'wb') -> None:
    """Write in the file."""
    try:
        with open(filepath, mode) as f:
            f.write(data)
    except Exception as e:
        raise IOError(f"Could not wrine in {filepath}: {e}")

def load_json(filepath: str) -> dict:
    """Loading JSON-config."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise IOError(f"Could not load settings from {filepath}: {e}")