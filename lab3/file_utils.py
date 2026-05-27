import json
from pathlib import Path


def load_settings(path):
    """
    Load application settings from JSON file.

    args:
        path:
            path to settings JSON file

    return:
        dictionary with loaded settings
    """

    settings_path = Path(path)

    with settings_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_settings(path, settings):
    """
    Save application settings to JSON file.

    args:
        path:
            path to output JSON file

        settings:
            dictionary with application settings
    """

    settings_path = Path(path)

    create_parent_folder(settings_path)

    with settings_path.open("w", encoding="utf-8") as file:
        json.dump(settings, file, ensure_ascii=False, indent=4)


def read_bytes(path):
    """
    Read file contents as bytes.

    args:
        path:
            path to input file

    return:
        binary file contents
    """

    file_path = Path(path)

    with file_path.open("rb") as file:
        return file.read()


def write_bytes(path, data):
    """
    Write binary data to file.

    args:
        path:
            path to output file

        data:
            binary data to write
    """

    file_path = Path(path)

    create_parent_folder(file_path)

    with file_path.open("wb") as file:
        file.write(data)


def create_parent_folder(path):
    """
    Create parent directory if it does not exist.

    args:
        path:
            file path whose parent folder must be created
    """

    folder = Path(path).parent

    if str(folder) == ".":
        return

    folder.mkdir(parents=True, exist_ok=True)


def get_file_size_str(path):
    """
    Convert file size to human-readable string.

    args:
        path:
            path to file

    return:
        formatted file size string
    """

    size = Path(path).stat().st_size

    if size < 1024:
        return f"{size} Б"

    if size < 1024 * 1024:
        return f"{size / 1024:.1f} КБ"

    return f"{size / (1024 * 1024):.2f} МБ"
