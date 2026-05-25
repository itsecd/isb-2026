import bcrypt

def hash_function(password: str) -> str:
    """
    генерирует хэш из пароля
    """
    try:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    except Exception as e:
        print(f"Ошибка хэширования bcrypt: {e}")
        return ""


def check_password(password: str, stored_hash: str) -> bool:
    """
    сравнивает пароль с хэшем
    """
    try:
        if not stored_hash or not isinstance(stored_hash, str):
            return False
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
    except Exception:
        return False


def login_user(username: str, password: str, data: dict) -> bool:
    """
    проверка для входа
    """
    if not data:
        return False
    stored_hash = data.get(username)
    return check_password(password, stored_hash)
    

def register_user(username: str, password: str, data: dict) -> bool:
    """
    добавляет пользователя с логином и паролем
    """
    if username in data:
        return False
    
    hashed_password = hash_function(password)
    if not hashed_password:
        return False
        
    data[username] = hashed_password
    return True