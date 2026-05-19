import json
import os.path

from errors import FileUtilsError


def read_bytes(path: str) -> bytes:
    """
    Read bytes from file.
    :param path: path to file
    :return: data from file
    """
    try:
        with open(path, 'rb') as file:
            return file.read()
    except FileNotFoundError as err:
        raise FileUtilsError(f"File not found: {path}") from err
    except PermissionError as err:
        raise FileUtilsError(f"Not enough rights to read file: {path}") from err
    except Exception as err:
        raise FileUtilsError(f"Error while reading file: {path}: {err}") from err


def write_bytes(path: str, data: bytes) -> None:
    """
    Write bytes from file.
    :param path: path to file
    :param data: data to save
    """
    try:
        with open(path, 'wb') as file:
            file.write(data)
    except FileNotFoundError as err:
        raise FileUtilsError(f"File not found: {path}") from err
    except PermissionError as err:
        raise FileUtilsError(f"Not enough rights to write file: {path}") from err
    except Exception as err:
        raise FileUtilsError(f"Error while writing file: {path}: {err}") from err


def load_settings(setting_file: str = 'settings.json') -> dict:
    """
    Load settings from JSON file or default.
    :return: settings
    """
    if not os.path.exists(setting_file):
        default_settings = {
            'initial_file': 'text.txt',
            'encrypted_file': 'encrypted.bin',
            'decrypted_file': 'decrypted.txt',
            'symmetric_key': 'symmetric_key.bin',
            'public_key': 'public_key.pem',
            'secret_key': 'secret_key.pem',
            'symmetric_key_length': 128
        }
        save_settings(setting_file, default_settings)
        return default_settings
    try:
        with open(setting_file, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    except Exception as err:
        raise FileUtilsError(f"Error reading JSON file: {err}") from err


def save_settings(path: str, data: dict) -> None:
    """
    Save settings to JSON file.
    :param path: path to save
    :param data: settings
    """
    try:
        with open(path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file)
    except Exception as err:
        raise FileUtilsError(f"Error writing JSON file: {err}") from err
