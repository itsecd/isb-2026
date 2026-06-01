import create

def transmit_packet(text: str, hmac_hex: str) -> dict:
    """
    Формирует сетевой пакет, упаковывая данные и цифровую подпись.

    Args:
        text (str): Текст сообщения.
        hmac_hex (str): Строка HMAC подписи.
    """
    if not isinstance(text, str) or not isinstance(hmac_hex, str):
        raise TypeError("Компоненты пакета должны быть строковыми данными.")

    packet = {
        "data": text,
        "hmac_hex": hmac_hex
    }
    
    print("Пакет успешно сформирован и отправлен в сеть.")
    return packet

def verify_packet(packet: dict, secret_key: str) -> bool:
    """
    Проверяет целостность и аутентичность полученного сетевого пакета.

    Args:
        packet (dict): Сетевой пакет со структурой {"data", "hmac_hex"}.
        secret_key (str): Секретный ключ для верификации.
    """
    if not isinstance(packet, dict):
        raise TypeError("Переданный пакет должен быть словарем (dict).")
        
    if "data" not in packet or "hmac_hex" not in packet:
        raise KeyError("Ошибка структуры: в сетевом пакете отсутствуют обязательные поля.")

    return create.verify(packet["data"], secret_key, packet["hmac_hex"])