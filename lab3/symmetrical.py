import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def create_blowfish_key(length_bits: int) -> bytes:
    """
    Генерирует случайный ключ заданной длины для алгоритма Blowfish.
    Длина должна быть от 32 до 448 бит и кратна 8.
    """
    if not (32 <= length_bits <= 448) or length_bits % 8 != 0:
        raise ValueError("Недопустимая длина ключа. Допустимый диапазон: 32-448 бит, шаг 8.")
    return os.urandom(length_bits // 8)

def cipher_blowfish_cbc(plaintext: bytes, secret: bytes) -> bytes:
    """
    Шифрует данные алгоритмом Blowfish в режиме CBC с PKCS7.
    Возвращает вектор инициализации, с шифротекстом.
    """
    iv = os.urandom(8)
    engine = Cipher(algorithms.Blowfish(secret), modes.CBC(iv)).encryptor()
    block_pad = padding.PKCS7(64).padder()
    padded = block_pad.update(plaintext) + block_pad.finalize()
    return iv + engine.update(padded) + engine.finalize()

def decipher_blowfish_cbc(ciphertext: bytes, secret: bytes) -> bytes:
    """
    Расшифровывает данные, защищенные Blowfish-CBC.
    Ожидает, что первые 8 байт входных данных являются вектором инициализации.
    """
    if len(ciphertext) < 8:
        raise ValueError("Некорректная длина зашифрованных данных.")
    iv, payload = ciphertext[:8], ciphertext[8:]
    engine = Cipher(algorithms.Blowfish(secret), modes.CBC(iv)).decryptor()
    padded_plain = engine.update(payload) + engine.finalize()
    unpad = padding.PKCS7(64).unpadder()
    return unpad.update(padded_plain) + unpad.finalize()