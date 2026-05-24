import hashlib

def compute_hash(data, algorithm: str):
    """
    Вычисление хеш-значения для строки или байтов.

    Args:
        data: Исходная строка или байты для хеширования.
        algorithm: Название алгоритма хеширования.

    Returns:
        Строка с шестнадцатеричным значением хеша.

    Raises:
        TypeError: Если на вход подан неверный тип данных.
        ValueError: Если указанный алгоритм не поддерживается библиотекой hashlib.
        RuntimeError: Непредвиденная ошибка в процессе хеширования.
    """
    if isinstance(data, str):
        data_bytes = data.encode("utf-8")
    elif isinstance(data, (bytes, bytearray)):
        data_bytes = data
    else:
        raise TypeError("Ожидается строка или байты")

    if algorithm not in hashlib.algorithms_available:
        raise ValueError(f"Алгоритм '{algorithm}' не поддерживается системой")

    try:
        h = hashlib.new(algorithm)
        h.update(data_bytes)
        return h.hexdigest()
    except Exception as e:
        raise RuntimeError(f"Ошибка хеширования: {e}")
