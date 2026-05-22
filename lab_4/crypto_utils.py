import hashlib


def generate_hash(password: str, salt: bytes):
    """
    Generate password hash by sha256 with salt

    :param password: Password for hashing
    :type password: str
    :param salt: Salt for hashing
    :type salt: bytes
    """
    hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    return hash
