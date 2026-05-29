import json
from pathlib import Path
from exceptions import FileOperationError, ConfigError


def load_settings(path):
    """
    Load application settings from JSON file.

    Args:
        path: Path to settings JSON file.

    Returns:
        Dictionary with loaded settings.

    Raises:
        FileOperationError: If settings file does not exist or cannot be read.
        ConfigError: If JSON structure is invalid.
    """
    settings_path = Path(path)

    try:
        with settings_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError as exc:
        raise FileOperationError(f"Settings file not found: {settings_path}") from exc

    except json.JSONDecodeError as exc:
        raise ConfigError(f"Invalid JSON structure: {settings_path}") from exc

    except OSError as exc:
        raise FileOperationError(f"Failed to read settings file: {settings_path}") from exc


def save_settings(path, settings):
    """
    Save application settings to JSON file.

    Args:
        path: Path to output JSON file.
        settings: Dictionary with application settings.

    Raises:
        FileOperationError: If file cannot be written.
    """
    settings_path = Path(path)

    try:
        create_parent_folder(settings_path)

        with settings_path.open("w", encoding="utf-8") as file:
            json.dump(settings, file, ensure_ascii=False, indent=4)

    except OSError as exc:
        raise FileOperationError(f"Failed to save settings file: {settings_path}") from exc


def read_bytes(path):
    """
    Read file contents as bytes.

    Args:
        path: Path to input file.

    Returns:
        Binary file contents.

    Raises:
        FileOperationError: If file does not exist or cannot be read.
    """
    file_path = Path(path)

    try:
        with file_path.open("rb") as file:
            return file.read()

    except FileNotFoundError as exc:
        raise FileOperationError(f"File not found: {file_path}") from exc

    except OSError as exc:
        raise FileOperationError(f"Failed to read file: {file_path}") from exc


def write_bytes(path, data):
    """
    Write binary data to file.

    Args:
        path: Path to output file.
        data: Binary data to write.

    Raises:
        FileOperationError: If file cannot be written.
    """
    file_path = Path(path)

    try:
        create_parent_folder(file_path)

        with file_path.open("wb") as file:
            file.write(data)

    except OSError as exc:
        raise FileOperationError(f"Failed to write file: {file_path}") from exc


def create_parent_folder(path):
    """
    Create parent directory if it does not exist.

    Args:
        path: File path whose parent folder must be created.

    Raises:
        FileOperationError: If directory cannot be created.
    """
    folder = Path(path).parent

    if str(folder) == ".":
        return

    try:
        folder.mkdir(parents=True, exist_ok=True)

    except OSError as exc:
        raise FileOperationError(f"Failed to create directory: {folder}") from exc


def get_file_size_str(path):
    """
    Convert file size to human-readable string.

    Args:
        path: Path to file.

    Returns:
        Formatted file size string or "unknown" if cannot read.
    """
    file_path = Path(path)

    try:
        size = file_path.stat().st_size

    except OSError:
        return "unknown"

    if size < 1024:
        return f"{size} B"

    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"

    return f"{size / (1024 * 1024):.2f} MB"
