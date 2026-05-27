from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

def generate_rsa_keys() -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """
    Генерирует пару асимметричных ключей RSA-2048.
    
    Returns:
        tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]: Кортеж (приватный, публичный).
        
    Raises:
        Exception: При ошибке генерации ключей.
    """
    try:
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        return private_key, private_key.public_key()
    except Exception as exc:
        print(f"Ошибка генерации RSA-ключей: {exc}")
        raise

def encrypt_sym_key(sym_key: bytes, public_key: rsa.RSAPublicKey) -> bytes:
    """
    Шифрует симметричный ключ публичным ключом RSA.
    
    Args:
        sym_key (bytes): Симметричный ключ для шифрования.
        public_key (rsa.RSAPublicKey): Публичный RSA-ключ получателя.
        
    Returns:
        bytes: Зашифрованный симметричный ключ.
        
    Raises:
        Exception: При ошибке асимметричного шифрования.
    """
    try:
        return public_key.encrypt(sym_key, padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        ))
    except Exception as exc:
        print(f"Ошибка шифрования сессионного ключа: {exc}")
        raise

def decrypt_sym_key(encrypted_sym_key: bytes, private_key: rsa.RSAPrivateKey) -> bytes:
    """
    Расшифровывает симметричный ключ приватным ключом RSA.
    
    Args:
        encrypted_sym_key (bytes): Зашифрованный симметричный ключ.
        private_key (rsa.RSAPrivateKey): Приватный RSA-ключ для дешифрования.
        
    Returns:
        bytes: Расшифрованный симметричный ключ.
        
    Raises:
        Exception: При ошибке асимметричного дешифрования.
    """
    try:
        return private_key.decrypt(encrypted_sym_key, padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        ))
    except Exception as exc:
        print(f"Ошибка дешифрования сессионного ключа: {exc}")
        raise
