
def save_bytes(data: bytes, path: str) -> None:
    """
    Сохраняет байты в файл.

    :param data: данные для сохранения
    :param path: путь к файлу
    """
    with open(path, "wb") as file:
        file.write(data)
    print(f"[OK] Данные сохранены: {path}")


def load_bytes(path: str) -> bytes:
    """
    Читает байты из файла.

    :param path: путь к файлу
    :return: содержимое файла
    """
    with open(path, "rb") as file:
        data = file.read()
    print(f"[OK] Данные загружены: {path} ({len(data)} байт)")
    return data