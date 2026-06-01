import hmac
import hashlib
import json

def create_hmac(key: str, data: str) -> str:
    hmac_hash = hmac.new(key.encode('utf-8') , data.encode('utf-8') , hashlib.sha256).hexdigest()
    return hmac_hash

def verify_hmac(key:str, data: str, hmac_hash: str) -> bool:
    true_hmac = create_hmac(key, data)
    return hmac.compare_digest(true_hmac, hmac_hash)

def send_message(data:str, hmac_hash: str, file_path:str) -> None:
    try:
        message = {
            "data": data,
            "hmac_hash": hmac_hash,
        }
        write_data(json.dumps(message, ensure_ascii=False, indent=2), file_path)
    except Exception:
        return

def receive_message(key: str, file_path: str) -> bool:
    try:
        message = json.loads(read_data(file_path))
        data = message["data"]
        hmac_hash = message["hmac_hash"]
        return verify_hmac(key, data, hmac_hash)
    except Exception:
        return False

def read_data(data_path:str) -> str:
    """
    Чтение текста из файла
    Входные данные:
    data_path - путь к файлу с данными
    Возвращает:
    Считанные данные(str)
    """
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return ""

def write_data(data: str,  file_path: str) -> None:
    """
    Запись данных в файл
    Входные данные:
    data - данные
    file_path - путь к сохранению файла
    Возвращает:
    None
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(data)
    except Exception:
        return