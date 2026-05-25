from hash_generation import *
from file_open_and_close import *

def hash_comparison(data_base: str, current_username, current_password)->bool:
    """
    Сравнивает хэш введенного пароля и хэш из базы данных
    Args:
        config_path (str): Путь к файлу конфигурации, current_username: имя пользователя, current_password: введенный пароль.
    Returns:
        Bool: True/False в зависимости от успошности входа.
    """
    if current_username not in data_base:
        return False
    if current_username in data_base:
        user_info = data_base[current_username]
        user_hash = user_info["hash"]
        user_salt = user_info["salt"]
    checking_hash=hash_password(current_password, user_salt)
    if checking_hash==user_hash:
        return True
    else:
        return False
    