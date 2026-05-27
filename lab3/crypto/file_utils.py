import json


def load_settings(path):
    """
    Загружает настройки из JSON-файла.

    Args:
        path (str): Путь к JSON-файлу с настройками.

    Returns:
        dict: Словарь с настройками.

    Raises:
        FileNotFoundError: Если файл настроек не найден.
        json.JSONDecodeError: Если JSON поврежден.
        OSError: При ошибке чтения файла.
    """

    try:
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)

    except FileNotFoundError:
        raise FileNotFoundError(f"Файл настроек не найден: {path}"        )

    except json.JSONDecodeError as err:
        raise json.JSONDecodeError(f"Ошибка декодирования JSON: {err.msg}",err.doc, err.pos)

    except OSError as e:
        raise OSError(f"Ошибка чтения файла настроек: {e}")


def save_binary_file(path, data):
    """
    Сохраняет бинарные данные в файл.

    Args:
        path (str): Путь к файлу.
        data (bytes): Данные для сохранения.

    Raises:
        OSError: Если запись в файл невозможна.
    """

    try:
        with open(path, 'wb') as file:
            file.write(data)

    except OSError as e:
        raise OSError(f"Ошибка записи бинарного файла: {e}")


def read_binary_file(path):
    """
    Считывает бинарные данные из файла.

    Args:
        path (str): Путь к файлу.

    Returns:
        bytes: Содержимое файла.

    Raises:
        FileNotFoundError: Если файл не найден.
        OSError: Если чтение невозможно.
    """

    try:
        with open(path, 'rb') as file:
            return file.read()

    except FileNotFoundError:
        raise FileNotFoundError(f"Бинарный файл не найден: {path}")

    except OSError as e:
        raise OSError(f"Ошибка чтения бинарного файла: {e}")


def save_text_file(path, text):
    """
    Сохраняет текст в файл.

    Args:
        path (str): Путь к файлу.
        text (str): Текст для сохранения.

    Raises:
        OSError: Если запись невозможна.
    """

    try:
        with open(path, 'w', encoding='utf-8') as file:
            file.write(text)

    except OSError as e:
        raise OSError(f"Ошибка записи текстового файла: {e}")


def read_text_file(path):
    """
    Считывает текст из файла.

    Args:
        path (str): Путь к файлу.

    Returns:
        str: Содержимое файла.

    Raises:
        FileNotFoundError: Если файл не найден.
        OSError: Если чтение невозможно.
    """

    try:
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()

    except FileNotFoundError:
        raise FileNotFoundError(f"Текстовый файл не найден: {path}")

    except OSError as e:
        raise OSError(f"Ошибка чтения текстового файла: {e}")
