import json
from typing import Dict, Any, Optional


def read_json(path: str) -> Dict[str, Any]:
    """Читает JSON-файл и возвращает его содержимое.

    Args:
        path (str): Путь к JSON-файлу.

    Returns:
        Dict[str, Any]: Разобранные данные из JSON.

    Raises:
        FileNotFoundError: Если файл не найден.
        json.JSONDecodeError: Если файл содержит некорректный JSON.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: str, data: Dict[str, Any]) -> None:
    """Записывает данные в JSON-файл.

    Args:
        path (str): Путь к JSON-файлу.
        data (Dict[str, Any]): Данные для записи.

    Raises:
        OSError: Если файл не может быть записан.
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def safe_load(path: str) -> Optional[Dict[str, Any]]:
    """Безопасно загружает JSON-файл базы данных.

    Args:
        path (str): Путь к JSON-файлу.

    Returns:
        Optional[Dict[str, Any]]: Словарь с данными, пустой словарь если файл
        не найден, None если файл повреждён.
    """
    try:
        return read_json(path)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print(f"Ошибка: файл {path} повреждён.")
        return None