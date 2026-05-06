import json

def load_config(path: str) -> Dict[str, Any]:
    """Загрузка конфига из файла"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Config file not found: {path}") from e

    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in config file: {path}") from e

    except PermissionError as e:
        raise PermissionError(f"No permission to read config file: {path}") from e


def read_bytes(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def write_bytes(path: str, data: bytes) -> None:
    with open(path, "wb") as f:
        f.write(data)
