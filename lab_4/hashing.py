import hashlib
import os
import json
from typing import Literal


def serialize(path: str, data: bytes) -> None:
    """
    Функция для сериализации данных в файл
    Args:
        path (str): Путь, по которому будут сохранены данные
    """
    directory = os.path.dirname(os.path.abspath(path))
    if not os.path.exists(directory):
        os.makedirs(directory)
    try:
        with open(path, mode='wb') as file:
            file.write(data)
    except OSError as e:
        print(f"Ошибка при работе с файлом! {e}")


def deserialize(path: str) -> bytes:
    """
    Функция для считывания (десериализации) данных из файла
    Args:
        path (str): Путь до считываемого файла
    Returns:
        Байты - данные из считанного фалы
    """
    try:
        with open(path, mode='rb') as file:
            data = file.read()
        return data
    except OSError as e:
        print(f"Ошибка при работе с файлом! {e}")


def get_file_hash(data: bytes, algo: Literal["sha256", "md5", "sha512"]) -> str:
    """
    Функция, вычисляющая хэш для набора байт
    Args:
        data (bytes): Данные для вычисления хэша
    Returns:
        str - хэш-строка
    """
    h = hashlib.new(algo)
    h.update(data)
    return h.hexdigest()


def load_checksums(settings: dict[str, str | int | bytes]) -> dict:
    """
    Функция для подгрузки сохранённых хешей
    Args:
        settings: Параметры приложения
    Returns:
        Словарь - считанные данные
    """
    if os.path.exists(settings["hash_db_path"]):
        return json.loads(deserialize(settings["hash_db_path"]))
    else:
        return dict()
