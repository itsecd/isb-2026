import json
from pathlib import Path
from exceptions import ConfigError, FileOperationError


def load_crypto_config(path="settings.json"):
    """
    Load crypto configuration from JSON file.

    Args:
        path: Path to JSON config file.

    Returns:
        Configuration dictionary.

    Raises:
        ConfigError: If config file does not exist or JSON is invalid.
        FileOperationError: If file cannot be read.
    """
    settings_path = Path(path)

    try:
        with settings_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError as exc:
        raise ConfigError(f"Settings file not found: {settings_path}") from exc

    except json.JSONDecodeError as exc:
        raise ConfigError(f"Invalid JSON structure: {settings_path}") from exc

    except OSError as exc:
        raise FileOperationError(f"Failed to read config file: {settings_path}") from exc
