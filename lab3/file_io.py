import os
import json


def load_settings(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        settings = json.load(f)
    print(f"Настройки загружены: {path}")
    return settings


def save_settings(settings: dict, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4, ensure_ascii=False)
    print(f"Настройки сохранены: {path}")


def read_file(path: str) -> bytes:
    with open(path, "rb") as f:
        data = f.read()
    print(f"Файл прочитан: {path} ({len(data)} байт)")
    return data


def write_file(path: str, data: bytes) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)
    print(f"Файл сохранён: {path} ({len(data)} байт)")
