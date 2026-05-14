import os.path
import json


def read_bytes(path: str) -> bytes:
    """
    Read bytes from file.
    :param path: path to file
    :return: data from file
    """
    with open(path, 'rb') as file:
        return file.read()


def write_bytes(path: str, data: bytes) -> None:
    """
    Write bytes from file.
    :param path: path to file
    :param data: data to save
    """
    with open(path, 'wb') as file:
        file.write(data)


def load_settings() -> dict:
    """
    Load settings from JSON file
    :return: settings
    """
    setting_file = 'settings.json'
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
        with open(setting_file, 'w', encoding='utf-8') as json_file:
            json.dump(default_settings, json_file)
    with open(setting_file, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)
