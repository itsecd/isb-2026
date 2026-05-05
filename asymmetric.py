from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey


def encrypt_symmetric_key(symmetric_key: bytes, public_key: RSAPublicKey) -> bytes:
    """
    Шифрование ключа с помощью RSA-OAEP
    Входные данные:
    symmetric_key - данные для шифрования(в данном случае симметричный ключ)
    public_key - открытый RSA ключ
    Возвращает зашифрованные данные (bytes)
    """
    encrypted_key = public_key.encrypt(symmetric_key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
    return encrypted_key

def decrypt_symmetric_key(encrypted_key: bytes, private_key: RSAPrivateKey) -> bytes:
    """
    Дешифровка ключа с помощью RSA-OAEP
    Входные данные:
    encrypted_key - данные для дешифрования(в данном случае симметричный ключ)
    private_key - закрытый RSA ключ
    Возвращает расшифрованные данные (bytes)
    """
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