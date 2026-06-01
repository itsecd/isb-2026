import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class BlowfishCipher:
    
    BLOCK_SIZE = 64
    IV_SIZE = 8
    
    def generate_key(self, bit_length: int) -> bytes:
        """
        Генерирует симметричный ключ для алгоритма Blowfish.
        
        Args:
            bit_length: Длина ключа в битах (от 32 до 448, кратна 8)
        
        Returns:
            bytes: Сгенерированный симметричный ключ
        
        Raises:
            ValueError: Если длина ключа не соответствует требованиям
        """
        if bit_length < 32 or bit_length > 448 or bit_length % 8 != 0:
            raise ValueError(f"Длина ключа Blowfish должна быть от 32 до 448 бит и кратна 8, получено {bit_length}")
        return os.urandom(bit_length // 8)
    
    def encrypt(self, key: bytes, data: bytes) -> bytes:
        """
        Шифрует данные с использованием алгоритма Blowfish в режиме CBC.
        
        Args:
            key: Симметричный ключ Blowfish
            data: Данные для шифрования
        
        Returns:
            bytes: Зашифрованные данные с добавленным вектором инициализации в начале
        """
        padder = padding.PKCS7(self.BLOCK_SIZE).padder()
        padded_data = padder.update(data) + padder.finalize()
        iv = os.urandom(self.IV_SIZE)
        cipher = Cipher(algorithms.Blowfish(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        cipher_text = encryptor.update(padded_data) + encryptor.finalize()
        return iv + cipher_text
    
    def decrypt(self, key: bytes, encrypted_data: bytes) -> bytes:
        """
        Дешифрует данные с использованием алгоритма Blowfish.
        
        Args:
            key: Симметричный ключ Blowfish
            encrypted_data: Зашифрованные данные (IV + шифротекст)
        
        Returns:
            bytes: Расшифрованные исходные данные
        """
        iv = encrypted_data[:self.IV_SIZE]
        cipher_text = encrypted_data[self.IV_SIZE:]
        cipher = Cipher(algorithms.Blowfish(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(cipher_text) + decryptor.finalize()
        unpadder = padding.PKCS7(self.BLOCK_SIZE).unpadder()
        return unpadder.update(padded_data) + unpadder.finalize()