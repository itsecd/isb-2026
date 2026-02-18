import json


def read_file(file_name: str) -> dict:
    """Чтение JSON-файлов"""
    
    with open(f"{file_name}.txt", "r", encoding="utf-8") as file:
        return json.load(file)
    