import os
from cryptography.hazmat.primitives.ciphers import Cipher, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.decrepit.ciphers.algorithms import SEED
from exceptions import EncryptError, DecryptError


class SEEDWrapper:
    def __init__(self, key: bytes, block_bits: int, iv_len: int):
        if len(key) != iv_len:
            raise EncryptError(f"Длина ключа SEED = {iv_len} байт, получено {len(key)}")
        self._secret = key
        self._block_size = block_bits
        self._iv_bytes = iv_len
        self._init_vector = None

    @staticmethod
    def create_key(byte_count: int) -> bytes:
        print(f"  * Генерация SEED ключа ({byte_count * 8} бит)")
        return os.urandom(byte_count)

    def setup_iv(self) -> bytes:
        self._init_vector = os.urandom(self._iv_bytes)
        return self._init_vector

    def _add_padding(self, source: bytes) -> bytes:
        padder = padding.ANSIX923(self._block_size).padder()
        return padder.update(source) + padder.finalize()

    def _strip_padding(self, source: bytes) -> bytes:
        remover = padding.ANSIX923(self._block_size).unpadder()
        return remover.update(source) + remover.finalize()

    def process_encrypt(self, plain: bytes) -> bytes:
        if self._init_vector is None:
            raise EncryptError("IV не задан! Вызовите setup_iv() сначала")
        try:
            padded_data = self._add_padding(plain)
            engine = Cipher(SEED(self._secret), modes.CBC(self._init_vector))
            encoder = engine.encryptor()
            result = encoder.update(padded_data) + encoder.finalize()
            return result
        except Exception as err:
            raise EncryptError(f"Сбой шифрования SEED: {err}")

    def process_decrypt(self, ciphertext: bytes, iv: bytes) -> bytes:
        try:
            engine = Cipher(SEED(self._secret), modes.CBC(iv))
            decoder = engine.decryptor()
            padded_result = decoder.update(ciphertext) + decoder.finalize()
            return self._strip_padding(padded_result)
        except Exception as err:
            raise DecryptError(f"Сбой расшифрования SEED: {err}")