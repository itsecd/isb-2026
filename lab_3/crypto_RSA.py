from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


def encrypt_rsa(plaintext, public_key):
    """
    Зашифровать данные с помощью RSA-OAEP
    
    Args:
        plaintext: байты для шифрования
        public_key: открытый ключ RSA
    
    Returns:
        bytes: зашифрованные данные
    """
    try:
        return public_key.encrypt(
            plaintext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except ValueError as e:
        raise ValueError(f"Plaintext too long for RSA key: {e}") from e
    except Exception as e:
        raise Exception(f"Failed to encrypt with RSA: {e}") from e


def decrypt_rsa(ciphertext, private_key):
    """
    Расшифровать данные с помощью RSA-OAEP
    
    Args:
        ciphertext: зашифрованные байты
        private_key: закрытый ключ RSA
    
    Returns:
        bytes: расшифрованные данные
    """
    try:
        return private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except ValueError as e:
        raise ValueError(f"Decryption failed - invalid key or corrupted data: {e}") from e
    except Exception as e:
        raise Exception(f"Failed to decrypt with RSA: {e}") from e