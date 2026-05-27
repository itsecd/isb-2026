import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms


def gen_chacha20_key(key_size: int) -> bytes:
    """
    create symmetric key of specified size

    args:
        key_size: size of key in bytes (16 or 32)

    return:
        a random sequence of key_size bytes
    """
    return os.urandom(key_size)


def gen_nonce(nonce_size: int) -> bytes:
    """
    create one-time nonce number

    args:
        nonce_size: size of nonce in bytes

    return:
        a random sequence of nonce_size bytes
    """
    return os.urandom(nonce_size)


def encrypt_chacha20(data: bytes, key: bytes, nonce: bytes) -> bytes:
    """
    encrypt data with chacha20 cipher

    args:
        data: source data to encrypt
        key: symmetric key
        nonce: one-time nonce number

    return:
        encrypted data
    """
    try:
        cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
        encryptor = cipher.encryptor()
        return encryptor.update(data)
    except TypeError as e:
        raise RuntimeError(f"ChaCha20 encryption error - invalid parameter type: {e}") from e
    except ValueError as e:
        raise RuntimeError(f"ChaCha20 encryption error - invalid parameter value: {e}") from e
    except AttributeError as e:
        raise RuntimeError(f"ChaCha20 encryption error - missing attribute: {e}") from e
    except OverflowError as e:
        raise RuntimeError(f"ChaCha20 encryption error - numeric overflow: {e}") from e
    except MemoryError as e:
        raise RuntimeError(f"ChaCha20 encryption error - insufficient memory: {e}") from e
    except Exception as e:
        raise RuntimeError(f"ChaCha20 encryption error: {e}") from e
    

def decrypt_chacha20(data: bytes, key: bytes, nonce: bytes) -> bytes:
    """
    decrypt data with chacha20 cipher

    args:
        data: source data to decrypt
        key: symmetric key
        nonce: one-time nonce number

    return:
        decrypted data
    """
    try:
        cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
        decryptor = cipher.decryptor()
        return decryptor.update(data)
    except TypeError as e:
        raise RuntimeError(f"Wrong parameter type - key/nonce/data must be bytes: {e}") from e
    except ValueError as e:
        raise RuntimeError(f"Invalid key or nonce length: {e}") from e
    except AttributeError as e:
        raise RuntimeError(f"Missing cryptography module or class: {e}") from e
    except MemoryError as e:
        raise RuntimeError(f"Memory error during decryption: {e}") from e
    except OverflowError as e:
        raise RuntimeError(f"Internal counter overflow: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Unexpected ChaCha20 decryption error: {e}") from e