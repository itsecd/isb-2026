from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

def generate_rsa_keys() -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """
    Генерирует пару ключей RSA (приватный и публичный).
    Использует стандартную публичную экспоненту 65537 и размер ключа 2048 бит.

    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    return private_key, private_key.public_key()

def encrypt_sym_key(sym_key: bytes, public_key: rsa.RSAPublicKey) -> bytes:
    """
    Шифрует симметричный ключ с помощью публичного ключа RSA.
    Использует схему дополнения OAEP с хешированием SHA256.

    """
    return public_key.encrypt(
        sym_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def decrypt_sym_key(encrypted_sym_key: bytes, private_key: rsa.RSAPrivateKey) -> bytes:
    """
    Расшифровывает симметричный ключ с помощью приватного ключа RSA.

    """
    return private_key.decrypt(
        encrypted_sym_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )