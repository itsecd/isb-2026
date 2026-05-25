import bcrypt

def generate_hash(password):
    """Генерация хэша с помощью bcrypt(с использованием соли)"""
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash,salt

def check_password(hash_db,password_user):
    """Сравнение хэша БД с введенным пользвателем"""
    user_bytes = password_user.encode('utf-8')
    result = bcrypt.checkpw(user_bytes, hash_db)
    return result
