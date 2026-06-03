from typing import Tuple
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding, rsa
from exceptions import AsymmetricCryptoError


class AsymmetricCipher:
    """Класс для управления асимметричным шифрованием и работы с ключами RSA.
    
    Предоставляет методы для генерации, сериализации и использования RSA-ключей
    для шифрования сессионных ключей AES.
    """
    
    def __init__(self, key_size: int = 2048, public_exponent: int = 65537):
        """Инициализирует менеджер асимметричного шифрования.
        
        Args:
            key_size (int, optional): Размер RSA-ключа в битах. Должен быть >= 2048.
                                     По умолчанию 2048.
            public_exponent (int, optional): Открытая экспонента RSA.
                                            Допустимые значения: 3 или 65537.
                                            По умолчанию 65537.
                                            
        Raises:
            AsymmetricCryptoError: Если параметры имеют недопустимые значения.
            
        Example:
            >>> cipher = AsymmetricCipher(key_size=4096, public_exponent=65537)
        """
        self._key_size = self._validate_key_size(key_size)
        self._public_exponent = self._validate_exponent(public_exponent)
    
    def _validate_key_size(self, key_size: int) -> int:
        """Проверяет корректность размера RSA-ключа.
        
        Args:
            key_size (int): Размер ключа для проверки.
            
        Returns:
            int: Проверенный размер ключа.
            
        Raises:
            AsymmetricCryptoError: Если размер не является числом или меньше 2048 бит.
        """
        try:
            size = int(key_size)
        except (TypeError, ValueError) as exc:
            raise AsymmetricCryptoError("Размер RSA-ключа должен быть числом") from exc
        
        if size < 2048:
            raise AsymmetricCryptoError("Размер RSA-ключа должен быть не меньше 2048 бит")
        return size
    
    def _validate_exponent(self, exponent: int) -> int:
        """Проверяет корректность открытой экспоненты RSA.
        
        Args:
            exponent (int): Экспонента для проверки.
            
        Returns:
            int: Проверенная экспонента.
            
        Raises:
            AsymmetricCryptoError: Если экспонента не является числом или не равна 3 или 65537.
        """
        try:
            val = int(exponent)
        except (TypeError, ValueError) as exc:
            raise AsymmetricCryptoError("Экспонента RSA должна быть числом") from exc
        
        match val:
            case 3 | 65537:
                return val
            case _:
                raise AsymmetricCryptoError("Открытая экспонента RSA должна быть 3 или 65537")
    
    def generate_pair(self) -> Tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
        """Генерирует новую пару RSA-ключей (закрытый и открытый).
        
        Returns:
            Tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]: Кортеж из закрытого и открытого ключей.
            
        Raises:
            AsymmetricCryptoError: Если не удалось сгенерировать пару ключей.
            
        Example:
            >>> cipher = AsymmetricCipher()
            >>> private_key, public_key = cipher.generate_pair()
        """
        try:
            private_key = rsa.generate_private_key(
                public_exponent=self._public_exponent,
                key_size=self._key_size,
            )
            return private_key, private_key.public_key()
        except ValueError as exc:
            raise AsymmetricCryptoError("Не удалось сгенерировать пару ключей RSA") from exc
    
    def _get_oaep_padding(self) -> asym_padding.OAEP:
        """Создает и возвращает объект OAEP padding для RSA операций.
        
        Использует SHA-256 для хеширования и MGF1 в качестве маскирующей функции.
        
        Returns:
            asym_padding.OAEP: Объект padding для RSA-OAEP шифрования.
        """
        return asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        )
    
    def serialize_public_key(self, public_key: rsa.RSAPublicKey) -> bytes:
        """Сериализует открытый RSA-ключ в PEM формат.
        
        Args:
            public_key (rsa.RSAPublicKey): Открытый ключ для сериализации.
            
        Returns:
            bytes: Сериализованный ключ в PEM формате.
            
        Example:
            >>> cipher = AsymmetricCipher()
            >>> _, pub_key = cipher.generate_pair()
            >>> pem_data = cipher.serialize_public_key(pub_key)
        """
        return public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    
    def serialize_private_key(self, private_key: rsa.RSAPrivateKey) -> bytes:
        """Сериализует закрытый RSA-ключ в PEM формат без шифрования.
        
        Args:
            private_key (rsa.RSAPrivateKey): Закрытый ключ для сериализации.
            
        Returns:
            bytes: Сериализованный ключ в PEM формате (незашифрованный).
            
        Example:
            >>> cipher = AsymmetricCipher()
            >>> priv_key, _ = cipher.generate_pair()
            >>> pem_data = cipher.serialize_private_key(priv_key)
        """
        return private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
    
    def load_private_key(self, key_data: bytes) -> rsa.RSAPrivateKey:
        """Десериализует закрытый RSA-ключ из PEM формата.
        
        Args:
            key_data (bytes): Байтовые данные ключа в PEM формате.
            
        Returns:
            rsa.RSAPrivateKey: Десериализованный закрытый ключ.
            
        Raises:
            AsymmetricCryptoError: Если не удалось загрузить ключ.
            
        Example:
            >>> cipher = AsymmetricCipher()
            >>> with open("private.pem", "rb") as f:
            ...     key_data = f.read()
            >>> private_key = cipher.load_private_key(key_data)
        """
        try:
            return serialization.load_pem_private_key(key_data, password=None)
        except (TypeError, ValueError) as exc:
            raise AsymmetricCryptoError("Не удалось десериализовать закрытый RSA-ключ") from exc
    
    def load_public_key(self, key_data: bytes) -> rsa.RSAPublicKey:
        """Десериализует открытый RSA-ключ из PEM формата.
        
        Args:
            key_data (bytes): Байтовые данные ключа в PEM формате.
            
        Returns:
            rsa.RSAPublicKey: Десериализованный открытый ключ.
            
        Raises:
            AsymmetricCryptoError: Если не удалось загрузить ключ.
            
        Example:
            >>> cipher = AsymmetricCipher()
            >>> with open("public.pem", "rb") as f:
            ...     key_data = f.read()
            >>> public_key = cipher.load_public_key(key_data)
        """
        try:
            return serialization.load_pem_public_key(key_data)
        except (TypeError, ValueError) as exc:
            raise AsymmetricCryptoError("Не удалось десериализовать открытый RSA-ключ") from exc
    
    def encrypt_session_key(self, aes_key: bytes, public_key: rsa.RSAPublicKey) -> bytes:
        """Зашифровывает сессионный AES-ключ с помощью открытого RSA-ключа.
        
        Args:
            aes_key (bytes): Байтовое представление AES-ключа для шифрования.
            public_key (rsa.RSAPublicKey): Открытый ключ для шифрования.
            
        Returns:
            bytes: Зашифрованный сессионный ключ.
            
        Raises:
            AsymmetricCryptoError: Если произошла ошибка при шифровании.
            
        Example:
            >>> cipher = AsymmetricCipher()
            >>> _, pub_key = cipher.generate_pair()
            >>> aes_key = os.urandom(32)
            >>> encrypted_key = cipher.encrypt_session_key(aes_key, pub_key)
        """
        try:
            return public_key.encrypt(aes_key, self._get_oaep_padding())
        except (TypeError, ValueError) as exc:
            raise AsymmetricCryptoError("Ошибка шифрования ключа алгоритмом RSA-OAEP") from exc
    
    def decrypt_session_key(self, encrypted_key: bytes, private_key: rsa.RSAPrivateKey) -> bytes:
        """Расшифровывает сессионный AES-ключ с помощью закрытого RSA-ключа.
        
        Args:
            encrypted_key (bytes): Зашифрованный сессионный ключ.
            private_key (rsa.RSAPrivateKey): Закрытый ключ для расшифрования.
            
        Returns:
            bytes: Расшифрованный AES-ключ.
            
        Raises:
            AsymmetricCryptoError: Если произошла ошибка при расшифровании.
            
        Example:
            >>> cipher = AsymmetricCipher()
            >>> priv_key, _ = cipher.generate_pair()
            >>> aes_key = cipher.decrypt_session_key(encrypted_key, priv_key)
        """
        try:
            return private_key.decrypt(encrypted_key, self._get_oaep_padding())
        except (TypeError, ValueError) as exc:
            raise AsymmetricCryptoError("Ошибка расшифрования ключа алгоритмом RSA-OAEP") from exc
