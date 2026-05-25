import hashlib

def hash_without_salt(password):
    """Генерация хэша с помощью sha256(без использованием соли)"""
    passw = password.encode('utf-8')
    return hashlib.sha256(passw).hexdigest()

def check_password_w(password_user,password_db):
    """Сравнение хэша БД с введенным пользвателем"""
    passw = password_user.encode('utf-8')
    p=hashlib.sha256(passw).hexdigest()
    return p==password_db
