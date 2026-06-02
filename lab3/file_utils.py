"""
File utility module for binary data I/O operations.

Provides safe file reading and writing functions with consistent error handling.
All operations raise descriptive FileOperationError exceptions on failure.
"""

from exceptions import FileOperationError


def save_bytes(data, path):
    """
    Write binary data to a file.

    Args:
        data (bytes): Binary data to write to file.
        path (str): File system path where data will be saved.

    Raises:
        FileOperationError: If file cannot be opened for writing or write fails.
    
    Example:
        >>> save_bytes(b'Hello World', '/tmp/output.bin')
    """
    try:
        with open(path, 'wb') as f:
            f.write(data)
    except OSError as e:
        raise FileOperationError(f"Failed to save file '{path}': {e}")


def load_bytes(path):
    """
    Read binary data from a file.

    Args:
        path (str): File system path to read from.

    Returns:
        bytes: Binary content of the file.

    Raises:
        FileOperationError: If file cannot be opened for reading or read fails.
    
    Example:
        >>> data = load_bytes('/tmp/input.bin')
    """
    try:
        with open(path, 'rb') as f:
            return f.read()
    except OSError as e:
        raise FileOperationError(f"Failed to load file '{path}': {e}")