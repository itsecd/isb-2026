import json


def load_json(path_to_json: str) -> dict:
    """
    Загрузка данных из json файла с обработкой исключений
    """
    try:
        with open(path_to_json, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        print(f"Ошибка: Файл {path_to_json} не найден.")
        return {}
    except json.JSONDecodeError:
        print(f"Ошибка: Файл {path_to_json} содержит некорректный формат JSON.")
        return {}
    except Exception as e:
        print(f"Непредвиденная ошибка при загрузке JSON: {e}")
        return {}
    

def save_json(path_to_json: str, data: dict) -> None:
    """
    Сохранение данных в json файл с обработкой исключений
    """
    try:
        with open(path_to_json, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
    except PermissionError:
        print(f"Ошибка доступа: Нет прав на запись в файл {path_to_json}.")
    except Exception as e:
        print(f"Ошибка при сохранении JSON: {e}")