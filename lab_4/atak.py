import create

def get_original_packet(secret_key: str) -> dict:
    """
    Генерирует эталонный пакет для проведения тестирования.

    Args:
        secret_key (str): Секретный ключ для создания подписи.
    """
    text = "Оригинальное сообщение"
    hmac_hex = create.create(text, secret_key)
    return {"data": text, "hmac_hex": hmac_hex}

def simulate_atak(packet: dict, new_text: str) -> dict:
    """
    Имитирует скрытую подмену текстового контента внутри сетевого пакета.

    Args:
        packet (dict): Перехваченный оригинальный пакет.
        new_text (str): Вредоносный текст для подмены.
    """
    if not isinstance(packet, dict) or "data" not in packet:
        raise ValueError("Перехваченный пакет поврежден или имеет неверный формат.")
        
    if not isinstance(new_text, str):
        raise TypeError("Вредоносный текст для подмены должен быть строкой.")

    danger_packet = packet.copy()
    danger_packet["data"] = new_text
    print("Зафиксировано несанкционированное вмешательство! Данные внутри пакета были изменены.")
    return danger_packet

def detect(is_valid: bool) -> None:
    """
    Анализирует результат проверки пакета и выводит текстовый лог.

    Args:
        is_valid (bool): Статус валидности пакета.
    """
    if not isinstance(is_valid, bool):
        raise TypeError("Результат проверки должен быть логического типа.")
        
    if is_valid:
        print("Проверка успешна. Целостность данных подтверждена, изменений не обнаружено.")
    else:
        print("Внимание!!! Обнаружено изменение данных. Цифровая подпись пакета не совпадает.")