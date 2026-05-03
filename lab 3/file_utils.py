def read_binary_file(file_path: str) -> bytes:
    """
    Читает бинарный файл.

    :param file_path: путь к файлу
    :return: содержимое файла в байтах
    """
    try:
        with open(file_path, "rb") as file:
            return file.read()
        
    except FileNotFoundError as error:
        raise FileNotFoundError(f"Файл не найден: {file_path}") from error
    

def write_binary_file(file_path: str, data: bytes) -> None:
    """
    Записывает данные в бинарный файл.

    :param file_path: путь к файлу
    :param data: данные для записи
    :return: None
    """
    with open(file_path, "wb") as file:
        file.write(data)