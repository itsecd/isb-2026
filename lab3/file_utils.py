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
            f"Settings file not found: {settings_path}"
        ) from exc
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON structure: {settings_path}"
        ) from exc
    except OSError as exc:
        raise OSError(
            f"Failed to read settings file: {settings_path}"
        ) from exc


def save_settings(path, settings):
    """Save application settings to a JSON file."""
    settings_path = Path(path)

    try:
        create_parent_folder(settings_path)
        with settings_path.open("w", encoding="utf-8") as file:
            json.dump(settings, file, ensure_ascii=False, indent=4)
    except OSError as exc:
        raise OSError(
            f"Failed to save settings file: {settings_path}"
        ) from exc


def read_bytes(path):
    """Read file contents as bytes."""
    file_path = Path(path)

    try:
        with file_path.open("rb") as file:
            return file.read()
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"File not found: {file_path}") from exc
    except OSError as exc:
        raise OSError(f"Failed to read file: {file_path}") from exc


def write_bytes(path, data):
    """Write bytes to a file, creating parent directories if needed."""
    file_path = Path(path)

    try:
        create_parent_folder(file_path)
        with file_path.open("wb") as file:
            file.write(data)
    except OSError as exc:
        raise OSError(f"Failed to write file: {file_path}") from exc


def create_parent_folder(path):
    """Create the parent directory for a file if it does not exist."""
    folder = Path(path).parent

    if str(folder) == ".":
        return

    try:
        folder.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise OSError(f"Failed to create directory: {folder}") from exc


def get_file_size_str(path):
    """Return a human-readable file size string."""
    try:
        size = Path(path).stat().st_size
        match True:
            case _ if size < 1024:
                return f"{size} Б"
            case _ if size < 1024 * 1024:
                return f"{size / 1024:.1f} КБ"
            case _:
                return f"{size / (1024 * 1024):.2f} МБ"
    except OSError:
        return "unknown"
