import os#для генерации случайных байтов через os.urandom()
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms

import constants as const


def generate_symmetric_key() -> bytes:
    """Генерирует случайный ключ для ChaCha20 (256 бит = 32 байта)
    const.SYMMETRIC_KEY_SIZE - сколько байтов сгенерировать (32)"""
    return os.urandom(const.SYMMETRIC_KEY_SIZE)


def generate_nonce() -> bytes:
    """Генерирует случайное одноразовое число (nonce) для ChaCha20 (128 бит = 16 байт)"""
    return os.urandom(const.NONCE_SIZE)


def encrypt_symmetric(plaintext: bytes, key: bytes, nonce: bytes) -> bytes:
    """Шифрование данных с помощью ChaCha20
    Cipher Объединяет алгоритм и режим в объект шифра"""
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None)#algorithms.ChaCha20(key, nonce)	Создаёт объект алгоритма с указанным ключом и nonce, None, потому что потоковый шифр
    encryptor = cipher.encryptor()#Создаёт объект шифратора encryptor.через него можно шифровать данные
    return encryptor.update(plaintext) + encryptor.finalize()#сложение ключевого потока и текста+(encryptor.finalize() для блочных данных, а тут просто говорит данных нет больше) 


def decrypt_symmetric(ciphertext: bytes, key: bytes, nonce: bytes) -> bytes:
    """Расшифрование данных с помощью ChaCha20"""
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None)#Создаём такой же объект шифра
    decryptor = cipher.decryptor()#Создаём объект дешифратора
    return decryptor.update(ciphertext) + decryptor.finalize()