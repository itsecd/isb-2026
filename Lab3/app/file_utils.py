
"""
Утилиты для работы с файлами.
Реализуют DRY-подход для чтения и записи данных.
"""

def write_bytes(path: str, data: bytes) -> None:
    """
    Записывает байтовые данные в файл.

    :param path: путь к файлу
    :param data: байтовые данные
    """
    try:
        if not path:
            raise ValueError("Путь к файлу не задан")

        with open(path, "wb") as file:
            file.write(data)

    except Exception as error:
        print(f"Ошибка записи байтов в файл {path}: {error}")
        raise


def read_bytes(path: str) -> bytes:
    """
    Считывает байтовые данные из файла.

    :param path: путь к файлу
    :return: байтовые данные
    """
    try:
        if not path:
            raise ValueError("Путь к файлу не задан")

        with open(path, "rb") as file:
            return file.read()

    except Exception as error:
        print(f"Ошибка чтения файла {path}: {error}")
        raise


def write_text(path: str, data: str) -> None:
    """
    Записывает текст в файл.

    :param path: путь к файлу
    :param data: текстовые данные
    """
    try:
        if not path:
            raise ValueError("Путь к файлу не задан")

        with open(path, "w", encoding="utf-8") as file:
            file.write(data)

    except Exception as error:
        print(f"Ошибка записи текста в файл {path}: {error}")
        raise
