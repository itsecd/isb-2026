import json

def save(path, settings):
    """
    Save settings to JSON file
    Args:
        path(str): Path to the settings file
        settings(dict): Dictionary with data from settings file
    Raises:
        OSError: Error writing data
    """
    try:
        normalized_settings = {}
        for key, value in settings.items():
            if isinstance(value, str) and ('\\' in value or '/' in value):
                normalized_settings[key] = value.replace('\\', '/')
            else:
                normalized_settings[key] = value
        with open(path, "w", encoding="utf-8") as fp:
            json.dump(normalized_settings, fp, indent=4, ensure_ascii=False)
    except OSError as e:
        raise OSError(f"Ошибка сохранения файла: {e}")

def load(path):
    """
    Load settings from JSON file
    Args:
        path(str): Path to the settings file
    Returns:
        dict: Dictionary with settings data
    Raises:
        FileNotFoundError: file not found
        ValueError: Incorrect data
    """
    try:
        with open(path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл настроек не найден: {path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка чтения файла: {e}")