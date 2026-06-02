"""
Модуль для генерации криптографических ключей.

Поддерживает генерацию:
- Симметричных ключей для Blowfish (32-448 бит)
- Асимметричных пар ключей RSA (2048 бит)
"""

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from cryptography.hazmat.backends import default_backend
import os
import sys


def create_symmetric_key(key_size_bits: int) -> bytes:
    """
    Генерация криптографического ключа для симметричного шифрования.
    
    Args:
        key_size_bits: Размер ключа в битах (должен быть кратен 8).
        
    Returns:
        bytes: Случайный симметричный ключ заданной длины.
        
    Raises:
        ValueError: Если размер ключа вне допустимого диапазона.
        
    Note:
        Blowfish поддерживает ключи от 32 до 448 бит включительно.
    """
    try:
        if key_size_bits < 32 or key_size_bits > 448 or key_size_bits % 8 != 0:
            raise ValueError("Размер ключа должен быть от 32 до 448 бит включительно, кратно 8")
        key_size_bytes = key_size_bits // 8
        return os.urandom(key_size_bytes)
    except ValueError as err:
        print(f"Ошибка генерации ключа: {err}")
        sys.exit(1)


def create_rsa_keypair() -> tuple[RSAPrivateKey, RSAPublicKey]:
    """
    Создание пары асимметричных ключей RSA.
    
    Returns:
        tuple[RSAPrivateKey, RSAPublicKey]: Кортеж из приватного и публичного ключей.
        
    Note:
        Использует стандартные параметры:
        - Размер ключа: 2048 бит
        - Публичная экспонента: 65537
    """
    private_key_obj = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key_obj = private_key_obj.public_key()
    return private_key_obj, public_key_obj