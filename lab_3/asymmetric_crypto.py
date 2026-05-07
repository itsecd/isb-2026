from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

import constants as const


def generate_rsa_keypair() -> tuple:
    """Генерирует пару ключей RSA (приватный, публичный)"""
    private_key = rsa.generate_private_key(public_exponent=const.RSA_PUBLIC_EXPONENT, key_size=const.RSA_KEY_SIZE)
    public_key = private_key.public_key()#Из закрытого ключа извлекает открытый ключ (содержит только n и e)
    return private_key, public_key#Возвращает оба ключа как кортеж


def encrypt_asymmetric(data: bytes, public_key) -> bytes:
    """Шифрование симметричного ключа(32байта) с помощью RSA (OAEP padding)
    data - симметричный ключ, public_key Открытый ключ получателя"""
    return public_key.encrypt(data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))


def decrypt_asymmetric(ciphertext: bytes, private_key) -> bytes:
    """Дешифрование данных с помощью RSA"""
    return private_key.decrypt(ciphertext, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))