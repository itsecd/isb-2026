import json
from pathlib import Path


def load_settings(path):
    """Load application settings from a JSON file."""
    settings_path = Path(path)

    try:
        with settings_path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Файл настроек не найден: {settings_path}"
        ) from exc
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Ошибка в структуре JSON-файла: {settings_path}"
        ) from exc
    except OSError as exc:
        raise OSError(
            f"Не удалось прочитать файл настроек: {settings_path}"
        ) from exc


def read_bytes(path):
    """Read file content as bytes."""
    file_path = Path(path)

    try:
        with file_path.open("rb") as file:
            return file.read()
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Файл не найден: {file_path}") from exc
    except OSError as exc:
        raise OSError(f"Ошибка чтения файла: {file_path}") from exc


def write_bytes(path, data):
    """Write bytes to a file and create the parent folder if needed."""
    file_path = Path(path)

    try:
        create_parent_folder(file_path)
        with file_path.open("wb") as file:
            file.write(data)
    except OSError as exc:
        raise OSError(f"Ошибка записи файла: {file_path}") from exc


def create_parent_folder(path):
    """Create the parent folder for a file if it does not exist."""
    folder = Path(path).parent

    match str(folder):
        case ".":
            return
        case _:
            try:
                folder.mkdir(parents=True, exist_ok=True)
            except OSError as exc:
                raise OSError(f"Не удалось создать папку: {folder}") from exc