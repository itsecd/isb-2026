import json
import os.path

from errors import FileUtilsError


def load_json(setting_file: str = 'settings.json') -> dict:
    """
    Load settings from JSON file.
    :return: settings
    """
    if not os.path.exists(setting_file):
        raise FileUtilsError(f"Файл {setting_file} не найден.")
    try:
        with open(setting_file, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    except Exception as err:
        raise FileUtilsError(f"Error reading JSON file: {err}") from err


def save_json(path: str, data: dict) -> None:
    """
    Save settings to JSON file.
    :param path: path to save
    :param data: settings
    """
    try:
        with open(path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
    except Exception as err:
        raise FileUtilsError(f"Error writing JSON file: {err}") from err
