import os
import string
from typing import Dict, Any


LIBRARY = string.ascii_uppercase + string.digits + string.ascii_lowercase + '_'


def check_login(login: str) -> bool:
    """
    Checks the validity of the login.

    Args:
        login (str): Login string.

    Returns:
        bool: True if the login is valid and false otherwise.
    """

    if not (3 <= len(login) <= 20):
        print(f"The length of the login does not match the standart: from 3 to 20 characters.")
        return False

    for char in login:
        if char not in LIBRARY:
            print(f"An invalid character {char} was used in the login.")
            return False
    
    return True


def check_secure_user_data(user_info: Any, login: str) -> bool:
    """
    Checks if the salt and hash storage structure has been changed.

    Args:
        user_info (Any): Information stored in the .json file.
        login (str): Login string.

    Returns:
        bool: True if the structure has not been changed, false in other cases.
    """

    if not isinstance(user_info, dict) or "salt" not in user_info or "hash" not in user_info:
        print(f"The structure of the .json file has been changed.\n"
              f"Please inform minialbina about the problem!")
        return False

    if len(user_info["salt"]) != 32:
        print(f"The {login}'s salt has been changed!")
        return False

    if len(user_info["hash"]) != 64:
        print(f"The {login}'s hash has been changed!")
        return False
    
    return True


def check_unsecure_user_data(user_info: Any, login: str) -> bool:
    """
    Checks if the hash storage structure has been changed.

    Args:
        user_info (Any): Information stored in the .json file.
        login (str): Login string.

    Returns:
        bool: True if the structure has not been changed, false in other cases.
    """

    if not isinstance(user_info, str):
        print(f"The structure of the .json file has been changed.\n"
              f"Please inform minialbina about the problem!")
        return False

    if len(user_info) != 64:
        print(f"The {login}'s hash has been changed!")
        return False
    
    return True