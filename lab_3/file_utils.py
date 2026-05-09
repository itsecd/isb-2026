import json
from typing import Dict, Any

def load_config(path: str) -> Dict[str, Any]:
    """
    Загружает конфигурацию из JSON-файла.
    """
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def read_bytes(path: str) -> bytes:
    """
    Читает файл в бинарном режиме.
    """
    with open(path, 'rb') as f:
        return f.read()

def write_bytes(path: str, data: bytes) -> None:
    """
    Записывает байтовые данные в файл.
    """
    with open(path, 'wb') as f:
        f.write(data)