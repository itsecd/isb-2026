from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

def encrypt_session_key(pub_key: RSAPublicKey, session_key: bytes) -> bytes:
    """
    Шифрование сессионного ключа асимметричным алгоритмом
    """
    encrypted_key = pub_key.encrypt(
        session_key, 
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_key

def decrypt_session_key(priv_key: RSAPrivateKey, encrypted_session_key: bytes) -> bytes:
    """
    Расшифровка сессионного ключа асимметричным алгоритмом
    """
    decrypted_key = priv_key.decrypt(
        encrypted_session_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_key
