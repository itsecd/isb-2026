import json

def read_bytes(path: str) -> bytes:
    """Прочтение файла в байтовом режиме."""
    with open(path, "rb") as f:
        return f.read()


def write_bytes(path: str, data: bytes) -> None:
    """Запись байтов в файл."""
    with open(path, "wb") as f:
        f.write(data)


def read_text(path: str, encoding: str = "utf-8") -> str:
    """Прочтение текстового файла."""
    with open(path, "r", encoding=encoding) as f:
        return f.read()


def load_settings(path: str = "settings.json") -> dict:
    """Загрузка настроек из JSON-файла."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
