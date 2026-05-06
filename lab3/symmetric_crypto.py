from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from file_utils import generate_random_bytes

class AESCipher:
    def __init__(self, key):
        if len(key) not in [16, 24, 32]:  # 128, 192, 256 бит
            raise ValueError("Неправильный размер ключа AES")
        self.key = key

    def encrypt(self, plaintext, iv):
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        padder = padding.ANSIX923(16).padder()
        padded_data = padder.update(plaintext) + padder.finalize()
        return encryptor.update(padded_data) + encryptor.finalize()

    def decrypt(self, ciphertext, iv):
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = padding.ANSIX923(16).unpadder()
        return unpadder.update(padded_plaintext) + unpadder.finalize()

def generate_aes_key(key_size_bits):
    key_size_bytes = key_size_bits // 8
    return generate_random_bytes(key_size_bytes)
