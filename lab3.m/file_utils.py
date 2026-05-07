def save_bytes(data: bytes, path: str) -> None:
    """
    Сохраняет байты в файл.

    :param data: данные для сохранения
    :param path: путь к файлу
    :raises IOError: если не удалось записать файл
    """
    try:
        with open(path, "wb") as file:
            file.write(data)
        print(f"[OK] Данные сохранены: {path}")
    except IOError as e:
        print(f"[ОШИБКА] Не удалось сохранить файл {path}: {e}")
        raise


def load_bytes(path: str) -> bytes:
    """
    Читает байты из файла.

    :param path: путь к файлу
    :return: содержимое файла
    :raises FileNotFoundError: если файл не найден
    :raises IOError: если не удалось прочитать файл
    """
    try:
        with open(path, "rb") as file:
            data = file.read()
        print(f"[OK] Данные загружены: {path} ({len(data)} байт)")
        return data
    except FileNotFoundError:
        print(f"[ОШИБКА] Файл не найден: {path}")
        raise
    except IOError as e:
        print(f"[ОШИБКА] Не удалось прочитать файл {path}: {e}")
        raise