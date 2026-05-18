import json


def write_data(text: bytes, path: str):
    """
    Записывает данные в файл

    Аргументы:
        text: исходный текст
        path: путь для сохранения текста
    """
    try:
        with open(path, "wb") as file:
            file.write(text)
    except PermissionError:
        print(f"Недостаточно прав для сохранения файла {path} (смените путь)")
        raise PermissionError
    except Exception as e:
        raise e


def read_text(path: str):
    """
    Считывает текст из файла

    Аргумент:
        path: путь к файлу
    """
    try:
        with open(path, "rb") as file:
            return file.read()
    except PermissionError:
        print(f"Недостаточно прав для чтения файла {path} (смените путь)")
        raise PermissionError
    except FileNotFoundError:
        print(f"Не найден файл {path} (смените путь)")
        raise FileNotFoundError
    except Exception as e:
        raise e


def read_encrypted(path: str):
    """
    Считывает зашифрованные данные

    Аргументы:
        path: путь к файлу
    """
    try:
        with open(path, "rb") as f:
            iv = f.read(16)
            c_text = f.read()
            return iv, c_text
    except PermissionError:
        print(f"Недостаточно прав для чтения файла {path} (смените путь)")
        raise PermissionError
    except FileNotFoundError:
        print(f"Не найден файл {path} (смените путь)")
        raise FileNotFoundError
    except Exception as e:
        raise e


def load_settings(path: str):
    """
    Загружает настройки с файла
    Аргументы:
        path: Путь до файла с настройками
    """
    try:
        with open(path) as json_file:
            settings = json.load(json_file)
            settings["path"] = path
            return settings
    except PermissionError:
        print("Недостаточно прав для чтения файла с настройками")
        raise PermissionError
    except FileNotFoundError:
        default_settings = {
            "initial_file": "source_text.txt",
            "encrypted_file": "encrypted_file.txt",
            "decrypted_file": "decrypted_file.txt",
            "lenght": 128,
            "symmetric_key": "symmetric_key.txt",
            "public_key": "public_key.pem",
            "private_key": "private_key.pem",
        }
        default_settings["path"] = path
        save_settings(default_settings)
    except Exception as e:
        raise e


def save_settings(settings: dict):
    """
    Сохраняет настройки в файл

    Аргумент:
        settings (dict): словарь с настройками
        path (str): Путь до файла для сохранения
    """
    try:
        with open(settings["path"], "w") as fp:
            json.dump(settings, fp)
    except PermissionError:
        print("Недостаточно прав для сохранения файла настроек")
        raise PermissionError
    except Exception as e:
        raise e
