import os
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from exceptions import SymmetricCryptoError

class SymmetricCipher:
    """Класс для управления симметричным шифрованием с использованием алгоритма AES-CBC."""

    def __init__(self, key_size: int = 256):
        self._key_size = self._validate_key_size(key_size)

    def _validate_key_size(self, key_size: int) -> int:
        try:
            size = int(key_size)
        except (TypeError, ValueError) as exc:
            raise SymmetricCryptoError("Размер AES-ключа должен быть числом") from exc

        match size:
            case 128 | 192 | 256:
                return size
            case _:
                raise SymmetricCryptoError("Размер AES-ключа должен быть 128, 192 или 256 бит")

    def generate_key(self) -> bytes:
        return os.urandom(self._key_size // 8)

    def encrypt(self, data: bytes, aes_key: bytes) -> bytes:
        iv_size = algorithms.AES.block_size // 8
        iv = os.urandom(iv_size)
        
        try:
            padder = sym_padding.PKCS7(algorithms.AES.block_size).padder()
            padded_data = padder.update(data) + padder.finalize()

            cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
            encryptor = cipher.encryptor()
            encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
            return iv + encrypted_data
        except ValueError as exc:
            raise SymmetricCryptoError("Ошибка добавления дополнения или AES-шифрования") from exc

    def decrypt(self, data: bytes, aes_key: bytes) -> bytes:
        iv_size = algorithms.AES.block_size // 8

        if len(data) < iv_size:
            raise SymmetricCryptoError("Зашифрованный файл слишком короткий для извлечения IV")

        iv = data[:iv_size]
        encrypted_data = data[iv_size:]

        try:
            cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
            decryptor = cipher.decryptor()
            decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

            unpadder = sym_padding.PKCS7(algorithms.AES.block_size).unpadder()
            return unpadder.update(decrypted_data) + unpadder.finalize()
        except ValueError as exc:
            raise SymmetricCryptoError("Ошибка расшифрования. Возможно, используется неверный ключ") from exc