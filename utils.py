import os

def ensure_directory_exists(file_path: str) -> None:
    """
    Создаёт директорию для файла, если её нет.

    Args:
        file_path (str): Полный путь к файлу. Директория будет создана
                         на основе os.path.dirname(file_path).
    """
    d = os.path.dirname(file_path)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)


def show_hex_dump(data: bytes) -> str:
    """
    Возвращает полный hex-дамп всех байтов.

    Args:
        data (bytes): Байтовые данные.

    Returns:
        str: Строка вида "a1 b2 c3 ..." или "<пусто>", если data пусто.
    """
    if not data:
        return "<пусто>"
    return ' '.join(f"{b:02x}" for b in data)


def show_text(data: bytes) -> str:
    """
    Возвращает полный декодированный текст UTF-8.

    Args:
        data (bytes): Байтовые данные.

    Returns:
        str: Декодированная строка или сообщение об ошибке, если декодирование не удалось.
    """
    if not data:
        return "<пусто>"
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError:
        return "<не удалось декодировать как UTF-8>"