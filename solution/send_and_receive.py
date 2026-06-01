import json
from hmac_logic import verify_hmac
from load_and_save import read_data, write_data
def send_message(data:str, hmac_hash: str, file_path:str) -> None:
    """
    Сохранение данных и hmac подписи в файл
    Входные данные:
    data - данные
    hmac_hash - HMAC подпись
    file_path - путь к файлу для сохранения
    Возвращает:
    None
    """
    try:
        message = {
            "data": data,
            "hmac_hash": hmac_hash,
        }
        write_data(json.dumps(message, ensure_ascii=False, indent=2), file_path)
    except Exception:
        return

def receive_message(key: str, file_path: str) -> tuple[bool, str]:
    """
    Чтение данных и hmac подписи из файла и проверка подписи
    Входные данные:
    key - ключ
    file_path - путь к файлу
    Возвращает:
    Кортеж (bool, str) - результат проверки подписи и считанные данные
    """
    try:
        message = json.loads(read_data(file_path))
        data = message["data"]
        hmac_hash = message["hmac_hash"]
        return verify_hmac(key, data, hmac_hash), data
    except Exception:
        return False, ""