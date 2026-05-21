"""Модуль для загрузки конфигурации из JSON-файла."""
import json
import os


def load_config():
    """Загружает конфигурацию из JSON-файла.
    Вернет:
    dict(Словарь с константами DEFAULT_KEY и ENCODING)"""
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    return config


# Загружаем конфигурацию ОДИН РАЗ при импорте модуля
_config = load_config()

DEFAULT_KEY = _config["DEFAULT_KEY"]
ENCODING = _config["ENCODING"]