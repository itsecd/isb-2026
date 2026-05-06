import os
import json
from symmetric import unpack_encrypted_data, pack_encrypted_data


def read_file(filepath: str) -> bytes:
    """
    Reads binary file content.

    Args:
        filepath (str): Path to the file.

    Returns:
        bytes: File content as bytes.
    """
    try:
        with open(filepath, 'rb') as f:
            return f.read()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {filepath}") from e
    except PermissionError as e:
        raise PermissionError(f"No permission to read file: {filepath}") from e
    except OSError as e:
        raise OSError(f"I/O error while reading file: {filepath}") from e


def write_text(filepath: str, text: str) -> bool:
    """
    Writes text data to file.

    Args:
        filepath (str): Output file path.
        text (str): Text to write.

    Returns:
        bool: True if write succeeded.
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        return True
    except Exception as e:
        raise RuntimeError(f"Couldn't write file: {filepath}") from e


def write_bytes(filepath: str, data: bytes) -> None:
    """
    Writes binary data to file.

    Args:
        filepath (str): output file path
        data (bytes): data to write

    Returns:
        None
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, 'wb') as f:
            f.write(data)

    except Exception as e:
        raise RuntimeError(f"Failed to write binary file: {filepath}") from e


def load_settings(filepath: str) -> dict:
    """
    Loads JSON configuration.

    Args:
        filepath (str): Path to JSON config file.

    Returns:
        dict: Parsed configuration data.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {filepath}") from e
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {filepath}") from e
    except PermissionError as e:
        raise PermissionError(f"No permission to read file: {filepath}") from e


def load_encrypted_file(filepath: str) -> tuple[bytes, bytes]:
    """
    Loads encrypted file and splits it into nonce and ciphertext.

    Args:
        filepath (str): Path to encrypted file.

    Returns:
        tuple[bytes, bytes]: (nonce, ciphertext)
    """
    try:
        with open(filepath, 'rb') as enc_file:
            data = enc_file.read()

        return unpack_encrypted_data(data)

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Encrypted file not found: {filepath}") from e
    except Exception as e:
        raise RuntimeError(f"Failed to load encrypted file: {filepath}") from e


def write_encrypted_file(filepath: str, nonce: bytes, ciphertext: bytes) -> None:
    """
    Writes encrypted data to file.

    Args:
        filepath (str): Output file path.
        nonce (bytes): Encryption nonce.
        ciphertext (bytes): Encrypted data.

    Returns:
        None
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        packed = pack_encrypted_data(nonce, ciphertext)

        with open(filepath, 'wb') as f:
            f.write(packed)

    except Exception as e:
        raise RuntimeError(f"Failed to write encrypted file: {filepath}") from e