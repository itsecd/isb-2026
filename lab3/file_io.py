import os
import json


def read_file(path: str) -> bytes:
    """
    Чтение бинарных данных из файла.

    Args:
        path: Путь к файлу.

    Returns:
        bytes: Содержимое файла.

    Raises:
        FileNotFoundError: Файл не найден.
        RuntimeError: Ошибка при чтении.
    """
    try:
        with open(path, "rb") as f:
            data = f.read()
        print(f"Файл прочитан: {path} ({len(data)} байт)")
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {path}")
    except Exception as e:
        raise RuntimeError(f"Ошибка при чтении файла '{path}': {e}")


def write_file(path: str, data: bytes) -> None:
    """
    Запись бинарных данных в файл с созданием директорий.

    Args:
        path: Путь для сохранения.
        data: Данные для записи.

    Raises:
        RuntimeError: Ошибка при записи.
    """
    try:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "wb") as f:
            f.write(data)
        print(f"Файл сохранён: {path} ({len(data)} байт)")
    except Exception as e:
        raise RuntimeError(f"Ошибка при записи файла '{path}': {e}")


def load_settings(path: str) -> dict:
    """
    Загрузка настроек из JSON-файла.

    Args:
        path: Путь к JSON-файлу.

    Returns:
        dict: Загруженные настройки.

    Raises:
        FileNotFoundError: Файл не найден.
        ValueError: Некорректный формат JSON.
        RuntimeError: Ошибка при загрузке.
    """
    try:
        with open(path, encoding="utf-8") as f:
            settings = json.load(f)
        print(f"Настройки загружены: {path}")
        return settings
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл настроек не найден: {path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Некорректный формат JSON в файле '{path}': {e}")
    except Exception as e:
        raise RuntimeError(f"Ошибка при загрузке настроек '{path}': {e}")


def save_settings(settings: dict, path: str) -> None:
    """
    Сохранение настроек в JSON-файл.

    Args:
        settings: Словарь с настройками.
        path: Путь для сохранения.

    Raises:
        RuntimeError: Ошибка при сохранении.
    """
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
        print(f"Настройки сохранены: {path}")
    except Exception as e:
        raise RuntimeError(f"Ошибка при сохранении настроек '{path}': {e}")
