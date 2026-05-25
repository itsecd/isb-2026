from argon2.low_level import hash_secret_raw, Type

def hash_password(password, my_salt):
    """
    Генерирует хэш пароля
    Args:
        password: пароль, my_salt: соль
    Returns:
        Захэшанный пароль
    """
    password_bytes = password.encode('utf-8')
    my_salt_bit=my_salt.encode('utf-8')
    hashed = hash_secret_raw(
        secret=password_bytes,
        salt=my_salt_bit,
        time_cost=3,        
        memory_cost=65536,  
        parallelism=4,     
        hash_len=32,        
        type=Type.ID        
    )
    return hashed.hex()
