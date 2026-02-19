import json


def read_file(file_name: str) -> dict:
    """Чтение JSON-файлов"""
    
    with open(f"{file_name}.txt", "r", encoding="utf-8") as file:
        return json.load(file)

def write_file(file_name: str, data: dict) -> None:
    """Запись JSON-файлов"""

    with open(f"{file_name}.txt", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    

def read_file_txt(file_name: str) -> str:
    """Чтение TXT-файлов"""
    with open(f'{file_name}.txt', "r", encoding='utf-8') as file:
        return file.read()


def write_file_txt(file_name: str, text: str) -> None:
    """Запись TXT-файлов"""
    with open(f'{file_name}.txt', "w", encoding='utf-8') as file:
        file.write(text)    