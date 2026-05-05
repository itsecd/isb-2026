from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey


def encrypt_symmetric_key(symmetric_key: bytes, public_key: RSAPublicKey) -> bytes:
    """шифрование ключа с помощью RSA-OAEP"""
    encrypted_key = public_key.encrypt(symmetric_key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
    return encrypted_key

def decrypt_symmetric_key(encrypted_key: bytes, private_key: RSAPrivateKey) -> bytes:
    """дешифровка ключа"""
    return private_key.decrypt(encrypted_key,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))

def get_asymmetric_key() -> bytes:
    """ключ для ассиметричного алгоритма"""
    keys = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
    )
    private_key = keys
    public_key = keys.public_key()
    return private_key, public_key