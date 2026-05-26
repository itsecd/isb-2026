from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from file_utils import generate_random_bytes

class AESCipher:
    def __init__(self, key):
        if len(key) not in [16, 24, 32]:  # 128, 192, 256 бит
            raise ValueError("Неправильный размер ключа AES")
        self.key = key

    def encrypt(self, plaintext, iv):
        # 1. Создаем шифратор
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        
        # 2. Добавляем Padding (PKCS7 - самый стандартный вариант)
        # Используем PKCS7 вместо ANSIX923 для большей совместимости
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext) + padder.finalize()
        
        # 3. Шифруем дополненные данные
        return encryptor.update(padded_data) + encryptor.finalize()

    def decrypt(self, ciphertext, iv):
        # 1. Расшифровываем
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        
        # 2. Убираем Padding
        unpadder = padding.PKCS7(128).unpadder()
        return unpadder.update(padded_plaintext) + unpadder.finalize()

def generate_aes_key(key_size_bits):
    key_size_bytes = key_size_bits // 8
    return generate_random_bytes(key_size_bytes)    
