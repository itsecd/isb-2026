import os

def read_file(filepath):
    """Чтение содержимого текстового файла."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Файл '{filepath}' не найден.")
        return None
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

def write_file(filepath, content):
    """Запись содержимого в текстовый файл."""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Сохранено: {filepath}")
        return True
    except Exception as e:
        print(f"Ошибка: {e}")
        return False

def clear_screen():
    """Очистка экрана консоли."""
    os.system('cls' if os.name == 'nt' else 'clear')
