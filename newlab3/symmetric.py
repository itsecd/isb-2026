import os
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from exceptions import SymmetricCryptoError


class SymmetricCipher:
    """Класс для управления симметричным шифрованием с использованием алгоритма AES-CBC.
    
    Предоставляет методы для генерации ключей, шифрования и дешифрования данных
    с использованием AES в режиме CBC с PKCS7 дополнением.
    """
    
    def __init__(self, key_size: int = 256):
        """Инициализирует менеджер симметричного шифрования.
        
        Args:
            key_size (int, optional): Размер AES-ключа в битах.
                                     Допустимые значения: 128, 192, 256.
                                     По умолчанию 256.
                                     
        Raises:
            SymmetricCryptoError: Если указан недопустимый размер ключа.
            
        Example:
            >>> cipher = SymmetricCipher(key_size=256)
        """
        self._key_size = self._validate_key_size(key_size)
    
    def _validate_key_size(self, key_size: int) -> int:
        """Проверяет корректность размера AES-ключа.
        
        Args:
            key_size (int): Размер ключа для проверки.
            
        Returns:
            int: Проверенный размер ключа.
            
        Raises:
            SymmetricCryptoError: Если размер не является числом или не входит
                                 в список допустимых значений (128, 192, 256).
        """
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
        """Генерирует случайный AES-ключ указанного размера.
        
        Returns:
            bytes: Сгенерированный ключ в байтовом представлении.
            
        Example:
            >>> cipher = SymmetricCipher(256)
            >>> key = cipher.generate_key()
            >>> len(key)  # 256 бит = 32 байта
            32
        """
        return os.urandom(self._key_size // 8)
    
    def encrypt(self, data: bytes, aes_key: bytes) -> bytes:
        """Шифрует данные с использованием AES-CBC.
        
        Процесс шифрования:
        1. Генерируется случайный initialization vector (IV)
        2. Данные дополняются до размера, кратного блоку AES
        3. Выполняется шифрование в режиме CBC
        4. Результат: IV + зашифрованные данные
        
        Args:
            data (bytes): Открытые данные для шифрования.
            aes_key (bytes): AES-ключ для шифрования.
            
        Returns:
            bytes: Зашифрованные данные с префиксом IV.
            
        Raises:
            SymmetricCryptoError: Если произошла ошибка при шифровании.
            
        Example:
            >>> cipher = SymmetricCipher()
            >>> key = cipher.generate_key()
            >>> encrypted = cipher.encrypt(b"Secret message", key)
        """
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
        """Расшифровывает данные, зашифрованные методом encrypt().
        
        Процесс расшифрования:
        1. Извлекается IV из первых block_size байтов
        2. Расшифровываются остальные данные в режиме CBC
        3. Удаляется PKCS7 дополнение
        
        Args:
            data (bytes): Зашифрованные данные (IV + шифртекст).
            aes_key (bytes): AES-ключ для расшифрования.
            
        Returns:
            bytes: Расшифрованные открытые данные.
            
        Raises:
            SymmetricCryptoError: Если зашифрованные данные слишком короткие
                                 или произошла ошибка при расшифровании
                                 (например, неверный ключ).
                                 
        Example:
            >>> cipher = SymmetricCipher()
            >>> key = cipher.generate_key()
            >>> encrypted = cipher.encrypt(b"Secret message", key)
            >>> decrypted = cipher.decrypt(encrypted, key)
            >>> decrypted == b"Secret message"
            True
        """
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
