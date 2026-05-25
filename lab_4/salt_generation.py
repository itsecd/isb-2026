import secrets

def generate_salt():
    """
    Генерирует соль
    Args:
        None
    Returns:
        salt: соль
    """
    salt=secrets.token_hex(16)
    return salt
