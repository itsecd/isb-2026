import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def create_blowfish_key(length_bits: int) -> bytes:
    """
    Генерирует криптографически стойкий ключ (32-448, кратные 8) для алгоритма Blowfish.
    
    Args:
        length_bits (int): Длина ключа в битах.
        
    Returns:
        bytes: Случайный ключ заданной длины.
        
    Raises:
        ValueError: Если длина ключа выходит за допустимые пределы.
    """
    try:
        match length_bits:
            case _ if not (32 <= length_bits <= 448) or length_bits % 8 != 0:
                raise ValueError("Недопустимая длина ключа.")
            case _:
                return os.urandom(length_bits // 8)
    except Exception as exc:
        print(f"Ошибка генерации симметричного ключа: {exc}")
        raise

def cipher_blowfish_cbc(plaintext: bytes, secret: bytes) -> bytes:
    """
    Шифрует данные алгоритмом Blowfish в режиме CBC с паддингом PKCS#7.
    
    Args:
        plaintext (bytes): Исходные данные для шифрования.
        secret (bytes): Симметричный ключ Blowfish.
        
    Returns:
        bytes: Вектор инициализации с шифротекстом.
        
    Raises:
        Exception: При ошибке шифрования.
    """
    try:
        iv = os.urandom(8)
        engine = Cipher(algorithms.Blowfish(secret), modes.CBC(iv)).encryptor()
        padder = padding.PKCS7(64).padder()
        padded = padder.update(plaintext) + padder.finalize()
        return iv + engine.update(padded) + engine.finalize()
    except Exception as exc:
        print(f"Ошибка симметричного шифрования: {exc}")
        raise

def decipher_blowfish_cbc(ciphertext: bytes, secret: bytes) -> bytes:
    """
    Расшифровывает данные, защищённые алгоритмом Blowfish в режиме CBC.
    
    Args:
        ciphertext (bytes): Зашифрованные данные.
        secret (bytes): Симметричный ключ Blowfish.
        
    Returns:
        bytes: Исходные данные после удаления паддинга.
        
    Raises:
        ValueError: Если длина данных меньше 8 байт или паддинг некорректен.
    """
    try:
        match len(ciphertext):
            case _ if len(ciphertext) < 8:
                raise ValueError("Некорректная длина зашифрованных данных.")
            case _:
                iv, payload = ciphertext[:8], ciphertext[8:]
                engine = Cipher(algorithms.Blowfish(secret), modes.CBC(iv)).decryptor()
                padded_plain = engine.update(payload) + engine.finalize()
                unpadder = padding.PKCS7(64).unpadder()
                return unpadder.update(padded_plain) + unpadder.finalize()
    except Exception as exc:
        print(f"Ошибка симметричного дешифрования: {exc}")
        raise
