from file_open_and_close import *
from salt_generation import *
from hash_generation import *
from hash_comparison import *
from argon2.low_level import hash_secret_raw, Type

def hash_password_no_salt(password):
    """
    Генерирует хэш пароля БЕЗ уникальной соли (использует фиксированную соль для всех).
    """
    password_bytes = password.encode('utf-8')
    # Маскируемся под отсутствие соли: передаем одинаковую строку для всех пользователей
    static_salt = "DUMMY_STATIC_SALT_8_BYTES".encode('utf-8')
    
    hashed = hash_secret_raw(
        secret=password_bytes,
        salt=static_salt,
        time_cost=3,        
        memory_cost=65536,  
        parallelism=4,     
        hash_len=32,        
        type=Type.ID        
    )
    return hashed.hex()


def hash_comparison_no_salt(data_base, current_username, current_password) -> bool:
    """
    Сравнивает хэш введенного пароля без использования уникальной соли.
    """
    if current_username not in data_base:
        return False
    
    user_info = data_base[current_username]
    user_hash = user_info["hash"]
    checking_hash = hash_password_no_salt(current_password)
    return checking_hash == user_hash


def user_registration_no_salt(config_path: str):
    """Регистрация пользователя БЕЗ соли"""
    config = load_config(config_path)
    # Загружаем отдельную базу данных для небезопасного режима
    db_path = config.get("files", {}).get("data_base_no_salt", "data_base_no_salt.json")
    data_base = load_user_database(db_path)

    user_name = ""
    while user_name == "":
        current_input = input("[UNSAFE] Enter username: ").strip()
        if current_input == "":
            print("No username was entered.")
            continue
        if current_input in data_base:
            print("Username already taken.")
            continue
        user_name = current_input
     
    user_password = ""
    while user_password == "":
        current_password = input("[UNSAFE] Enter password: ").strip()
        if current_password == "":
            print("No password was entered.") 
            continue
        user_password = current_password

    password_hash = hash_password_no_salt(user_password)
    add_user_to_file(db_path, user_name, password_hash, user_salt="none")
    print("Unsafe registration complete!")


def user_login_no_salt(config_path: str) -> bool:
    """Авторизация пользователя БЕЗ соли"""
    config = load_config(config_path)
    db_path = config.get("files", {}).get("data_base_no_salt", "data_base_no_salt.json")
    data_base = load_user_database(db_path)

    current_username = input("[UNSAFE Login] Enter username: ").strip()
    current_password = input("[UNSAFE Login] Enter password: ").strip()

    if hash_comparison_no_salt(data_base, current_username, current_password):
        print("Unsafe login successful!")
        return True
    else:
        print("Incorrect password.")
        return False
