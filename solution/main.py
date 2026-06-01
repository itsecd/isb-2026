import hmac
import hashlib

def create_hmac(key: str, text: str) -> str:
    hmac_hash = hmac.new(key.encode('utf-8') , text.encode('utf-8') , hashlib.sha256).hexdigest()
    return hmac_hash

def verify_hmac(key:str, text: str, hmac_hash: str) -> bool:
    true_hmac = create_hmac(key, text)
    return hmac.compare_digest(true_hmac, hmac_hash)

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
    except Exception as ex:
        print(f"Ошибка!: {ex}")
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
    except Exception as ex:
        print(f"Ошибка!: {ex}")