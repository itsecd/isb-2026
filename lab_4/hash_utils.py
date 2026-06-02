import hashlib
import random
import string


def generate_string(length: int = 16) -> str:
    """
    Generate random string with set length.
    :param length: length of string
    :return: random string
    """
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def get_short_hash(data: str, length: int = 16) -> int:
    """
    Calculate short hash value of string.
    :param data: string
    :param length: length of short hash
    :return: hash value
    """
    if length not in (8, 12, 16):
        raise ValueError("length can only be 8, 12 or 16 bits.")

    hash_bytes = hashlib.sha256(data.encode('utf-8')).digest()

    hash_int = int.from_bytes(hash_bytes, byteorder='big')

    mask = (1 << length) - 1
    return hash_int & mask
