import json

def load(path):
    try:
        with open(path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл настроек не найден: {path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка чтения файла: {e}")
    
def save(path, settings):
    try:
        with open(path, "w", encoding="utf-8") as fp:
            json.dump(settings, fp, indent=4, ensure_ascii=False)
    except OSError as e:
        raise OSError(f"Ошибка сохранения файла: {e}")