import os

from cryptography.hazmat.primitives.asymmetric import rsa


def generate_aes_key(key_size=256):
    """
    Сгенерировать симметричный AES ключ
    
    Args:
        key_size: длина ключа в битах (128, 192 или 256)
    
    Returns:
        bytes: сгенерированный ключ
    """
    if key_size not in [128, 192, 256]:
        raise ValueError(f"Invalid key_size: {key_size}. Expected 128, 192, or 256")
    
    return os.urandom(key_size // 8)


def generate_rsa_keys():
    """
    Сгенерировать пару асимметричных RSA ключей
    
    Returns:
        tuple: (private_key, public_key)
    """
    try:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        return private_key, private_key.public_key()
    except Exception as e:
        raise Exception(f"Failed to generate RSA keys: {e}") from e