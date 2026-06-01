from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding


class RSAKeyManager:
    
    KEY_SIZE = 2048
    PUBLIC_EXPONENT = 65537
    
    def generate_pair(self) -> tuple:
        """
        Генерирует пару асимметричных ключей RSA длиной 2048 бит.
        
        Returns:
            tuple: (приватный_ключ, публичный_ключ)
        """
        private_key = rsa.generate_private_key(
            public_exponent=self.PUBLIC_EXPONENT,
            key_size=self.KEY_SIZE
        )
        return private_key, private_key.public_key()
    
    def save_public(self, path: str, public_key) -> None:
        """
        Сохраняет публичный ключ RSA в файл в формате PEM.
        
        Args:
            path: Путь для сохранения файла ключа
            public_key: Публичный ключ RSA
        """
        with open(path, 'wb') as public_out:
            public_out.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
    
    def save_private(self, path: str, private_key) -> None:
        """
        Сохраняет приватный ключ RSA в файл в формате PEM без шифрования.
        
        Args:
            path: Путь для сохранения файла ключа
            private_key: Приватный ключ RSA
        """
        with open(path, 'wb') as private_out:
            private_out.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
    
    def load_public(self, path: str):
        """
        Загружает публичный ключ RSA из PEM файла.
        
        Args:
            path: Путь к файлу публичного ключа
        
        Returns:
            Загруженный публичный ключ RSA
        """
        with open(path, 'rb') as public_file:
            return serialization.load_pem_public_key(public_file.read())
    
    def load_private(self, path: str):
        """
        Загружает приватный ключ RSA из PEM файла.
        
        Args:
            path: Путь к файлу приватного ключа
        
        Returns:
            Загруженный приватный ключ RSA
        """
        with open(path, 'rb') as private_file:
            return serialization.load_pem_private_key(private_file.read(), password=None)
    
    def encrypt(self, public_key, data: bytes) -> bytes:
        """
        Шифрует данные с использованием алгоритма RSA и OAEP паддинга.
        
        Args:
            public_key: Публичный ключ RSA
            data: Данные для шифрования
        
        Returns:
            bytes: Зашифрованные данные
        """
        return public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    
    def decrypt(self, private_key, data: bytes) -> bytes:
        """
        Дешифрует данные с использованием алгоритма RSA и OAEP паддинга.
        
        Args:
            private_key: Приватный ключ RSA
            data: Зашифрованные данные
        
        Returns:
            bytes: Расшифрованные данные
        """
        return private_key.decrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )