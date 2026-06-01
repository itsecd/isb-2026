import string
import json
import random

def generate_random_string(length: int) -> str:
    """
    Генерация случайной строки заданной длины.
    Принимает:
        length - длину строки
    Возвращает:
        Строку длиной length
    """
    # Явная проверка на дурака: длина должна быть int и строго больше нуля
    if not isinstance(length, int) or length <= 0:
        raise ValueError("Длина строки должна быть натуральным числом")
    try:
        chars = string.ascii_letters + string.digits
        return ''.join(random.choices(chars, k=length))
    except Exception as e:
        raise RuntimeError("Внутренняя ошибка при генерации строки") from e
    

def read_json_file(filepath: str) -> dict:
    """
    Чтение .json файла по указанному пути в словарь.
    Принимает:
        filepath - путь до .json файла.
    Возвращает:
        - словарь со считанными из файла данными
    """
    try:
        with open(filepath, 'r') as fp:
            json_data = json.load(fp)
        return json_data
    except Exception as e:
        print(f"Не удалось открыть файл {filepath}: {e}")
        raise