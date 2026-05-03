from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes


def generate_rsa_keys() -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """Генерация приватного и публичного ключей RSA"""
    keys = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    private_key = keys
    public_key = keys.public_key()
    return private_key, public_key


def encrypt_sym_key(sym_key: bytes, public_key: rsa.RSAPublicKey) -> bytes:
    """Шифрование симитричного ключа при помощи публичного ключа"""
    encrypt_sym_key = public_key.encrypt(sym_key,
                                         padding.OAEP(
                                             mgf=padding.MGF1(
                                                 algorithm=hashes.SHA256()),
                                             algorithm=hashes.SHA256(),
                                             label=None
                                         )
                                         )
    return encrypt_sym_key


def decrypt_sym_key(encrypted_sym_key: bytes, private_key: rsa.RSAPrivateKey) -> bytes:
    """Дешифрование симметричного ключа при помощи приватного ключа"""
    sym_key = private_key.decrypt(
        encrypted_sym_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return sym_key
