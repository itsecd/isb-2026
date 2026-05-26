import os
import hashlib
from typing import Dict, Any, List


def generate_salt() -> str:
    """
    Generates a 16 bytes salt.

    Returns:
        str: A string of 32 characters in the hexadecimal system.
    """

    random_salt = os.urandom(16)
    return random_salt.hex()


def calculate_hash(password: str, salt: str=None) -> str:
    """
    Calculates the password hash using the SHA-3-256 method.


    Args:
        password (str): A password string.
        salt (str, optional): A 128-bit hexadecimal salt string.
                              Defaults to None.

    Returns:
        str:  A 64-character string in the hexadecimal system.
    """
    
    if salt is not None:
        password = password + salt

    hash_object = hashlib.sha3_256()
    hash_object.update(password.encode('utf-8'))
    hex_hash = hash_object.hexdigest()
    
    return hex_hash