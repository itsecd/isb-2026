import os


def save_hash(file_path: str, hash_value: str, output_path: str) -> str:
    """
    Сохраняет хэш-сумму и имя файла в указанный выходной файл в стандартном формате.
    """
    filename = os.path.basename(file_path)
    content = f"{hash_value}  {filename}\n"
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return output_path
    except PermissionError:
        raise PermissionError(f"Нет прав на запись файла: {output_path}")
    except OSError as e:
        raise OSError(f"Ошибка при сохранении хеш-файла: {e}")


def load_hash(hash_file_path: str) -> str:
    """
    Загружает хэш-файл и извлекает из него строку хэш-суммы.
    """
    if not os.path.exists(hash_file_path):
        raise FileNotFoundError(f"Файл хеша не найден: {hash_file_path}")

    with open(hash_file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    if not content:
        raise ValueError("Файл контрольной суммы пуст")

    return content.split()[0]
