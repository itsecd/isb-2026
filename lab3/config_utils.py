import json


def load_config(path: str) -> dict:
    '''Загружает настройки из JSON-файла.

    Args:
        path (str): Путь к JSON-файлу конфигурации.

    Returns:
        dict: Словарь с настройками.

    Raises:
        FileNotFoundError: Если файл не найден.
        ValueError: Если файл имеет неверный формат JSON.
    '''
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл конфигурации не найден: {path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка чтения JSON: {e}")


def save_config(path: str, config: dict) -> None:
    '''Сохраняет настройки в JSON-файл.

    Args:
        path (str): Путь к JSON-файлу.
        config (dict): Словарь с настройками.

    Raises:
        OSError: Если не удалось записать файл.
    '''
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    except OSError as e:
        raise OSError(f"Ошибка сохранения конфигурации: {e}")