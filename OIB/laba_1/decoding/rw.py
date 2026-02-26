def read(path_original: str) -> str:
    """Функция для считывания файла."""
    try:
        with open(path_original, 'r', encoding="utf-8") as f:
            text = f.read()
        return text
    except FileNotFoundError:
        print("ОШИБКА: Файл не найден по указанному пути.")
        return ""
    except Exception as e:
        print("Ошибка при чтении файла.")
        return ""

def write(path_encrypted: str, encoding_text: str) -> None:
    """Функция для записи в файл."""
    try:
        with open(path_encrypted, 'w', encoding="utf-8") as f:
            f.write(encoding_text) 
    except PermissionError:
        print("ОШИБКА: не удаётся записать.")
    except Exception as e:
        print("Ошибка при записи в файл.")