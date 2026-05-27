import json
from pathlib import Path


def load_crypto_config(
    path="settings.json",
):
    """
    Load crypto configuration from JSON file.

    args:
        path:
            path to JSON config file

    return:
        configuration dictionary

    raises:
        FileNotFoundError:
            if config file does not exist

        ValueError:
            if JSON structure is invalid
    """

    settings_path = Path(path)

    try:
        with settings_path.open(
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(file)

    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Settings file not found: "
            f"{settings_path}"
        ) from exc

    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON structure: "
            f"{settings_path}"
        ) from exc
