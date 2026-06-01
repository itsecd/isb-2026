def save_bytes(data, path):
    try:
        with open(path, 'wb') as f:
            f.write(data)
    except OSError as e:
        raise OSError(f"Failed to save file '{path}': {e}")


def load_bytes(path):
    try:
        with open(path, 'rb') as f:
            return f.read()
    except OSError as e:
        raise OSError(f"Failed to load file '{path}': {e}")
