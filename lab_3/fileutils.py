import json
import os.path


def read_bytes(path: str) -> bytes | None:
    """
    Read bytes from file.
    :param path: path to file
    :return: data from file
    """
    try:
        with open(path, 'rb') as file:
            return file.read()
    except FileNotFoundError as err:
        print(f"File cannot be found: {err}")
        raise
    except PermissionError as err:
        print(f"Not enough rights to reach file: {err}")
        raise
    except Exception as err:
        print(f"Error while working: {err}")
        raise


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
        print(f"File cannot be found: {err}")
        raise
    except PermissionError as err:
        print(f"Not enough rights to reach file: {err}")
        raise PermissionError
    except Exception as err:
        print(f"Error while working: {err}")
        raise


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
        print(f"Error reading JSON file: {err}")
        raise


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
        print(f"Error writing JSON file: {err}")
        raise
