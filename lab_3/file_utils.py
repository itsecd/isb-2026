import json

def read_file(filepath: str) -> bytes:
    try:
        with open(filepath, 'rb') as f:
            return f.read()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {filepath}") from e


def write_text(filepath, text):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        return True
    except Exception as error:
        print(f"Не удалось записать {filepath}: {error}\n")
        return False


def load_settings(filepath: str):
    try:
        with open(filepath) as json_file:
            json_data = json.load(json_file)
    except FileNotFoundError:
        raise 