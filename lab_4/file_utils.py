import json
import os


def load_settings():
    """
    Загрузка настроек из settings.json.

    Returns:
        dict: Словарь с настройками.
    """
    if not os.path.exists("settings.json"):
        raise FileNotFoundError("settings.json не найден")

    try:
        with open("settings.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise RuntimeError(f"Ошибка чтения settings.json: {e}")
