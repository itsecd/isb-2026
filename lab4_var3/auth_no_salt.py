import hashlib

def hash_function_no_salt(password: str) -> str:
    """
    Генерирует хэш из пароля без соли с обработкой исключений
    """
    try:
        if not isinstance(password, str):
            password = str(password)
        hash_object = hashlib.sha256(password.encode('utf-8'))
        return hash_object.hexdigest()
    except Exception as e:
        print(f"Ошибка при генерации хэша: {e}")
        return ""


def check_password_no_salt(password: str, stored_hash: str) -> bool:
    """
    Сравнивает пароль с хэшем без соли
    """
    if not stored_hash or not isinstance(stored_hash, str):
        return False
    return hash_function_no_salt(password) == stored_hash


def login_user_no_salt(username: str, password: str, data: dict) -> bool:
    """
    Проверка для входа без соли
    """
    if not isinstance(data, dict):
        return False
        
    stored_hash = data.get(username)
    if not stored_hash:
        return False
    
    return check_password_no_salt(password, stored_hash)
    

def register_user_no_salt(username: str, password: str, data: dict) -> bool:
    """
    Добавляет пользователя с логином и хэшем пароля без соли
    """
    if not isinstance(data, dict):
        return False
        
    if username in data:
        return False
    
    hashed_password = hash_function_no_salt(password)
    if not hashed_password:
        return False
        
    data[username] = hashed_password
    return True