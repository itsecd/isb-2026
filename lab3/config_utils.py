import json


def load_config(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл конфигурации не найден: {path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка чтения JSON: {e}")


def save_config(path: str, config: dict) -> None:
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    except OSError as e:
        raise OSError(f"Ошибка сохранения конфигурации: {e}")