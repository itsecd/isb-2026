from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
import os
import sys

def create_symmetric_key(key_size_bits: int) -> bytes:
    """Генерация криптографического ключа для симметричного шифрования"""
    try:
        if key_size_bits < 32 or key_size_bits > 448 or key_size_bits % 8 != 0:
            raise ValueError("Размер ключа должен быть от 32 до 448 бит включительно, кратно 8")
        
        key_size_bytes = key_size_bits // 8
        return os.urandom(key_size_bytes)
    except ValueError as err:
        print(f"Ошибка генерации ключа: {err}")
        sys.exit(1)

def create_rsa_keypair() -> tuple[RSAPrivateKey, RSAPublicKey]:
    """Создание пары асимметричных ключей RSA"""
    private_key_obj = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key_obj = private_key_obj.public_key()
    return private_key_obj, public_key_obj