"""
Модуль для асимметричного шифрования с использованием RSA.

Содержит класс RSAKeyPair для генерации, загрузки, сохранения
RSA-ключей и шифрования/дешифрования симметричных ключей.
"""

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import hashes
from file_utils import read_binary_file, write_binary_file


class AsymmetricCryptoError(Exception):
    """Исключение для ошибок, связанных с асимметричным шифрованием (RSA)."""
    pass

class RSAKeyPair:
    """
    Класс для управления парой RSA-ключей (приватный и публичный).
    Предоставляет методы для генерации, сохранения, загрузки
    и использования ключей для шифрования симметричного ключа.
    """

    def __init__(self, private_key=None, public_key=None):
        """
        Инициализирует объект RSAKeyPair.

        Если ключи не предоставлены, генерирует новую пару.

        Args:
            private_key (RSAPrivateKey, optional): Существующий приватный ключ.
            public_key (RSAPublicKey, optional): Существующий публичный ключ.
                                                 Используется, если предоставлен private_key.
        """
        if private_key is None:
            try:
                self.private_key = rsa.generate_private_key(
                    public_exponent=65537,
                    key_size=2048
                )
                self.public_key = self.private_key.public_key()
            except Exception as e:
                
                raise AsymmetricCryptoError(f"Ошибка генерации RSA-ключей: {e}")
        else:
            self.private_key = private_key
            self.public_key = private_key.public_key()

    @staticmethod
    def load_from_files(priv_path, pub_path):
        """
        Загружает RSA-ключи из файлов.

        Args:
            priv_path (str): Путь к файлу приватного ключа.
            pub_path (str): Путь к файлу публичного ключа.

        Returns:
            RSAKeyPair: Новый экземпляр класса с загруженными ключами.

        Raises:
            FileNotFoundError: Если один из файлов не найден.
            ValueError: Если формат файла некорректен.
            AsymmetricCryptoError: Для других ошибок загрузки.
        """
        priv_bytes = read_binary_file(priv_path)
        pub_bytes = read_binary_file(pub_path)
        
        try:
            private_key = serialization.load_pem_private_key(priv_bytes, password=None)
            public_key = serialization.load_pem_public_key(pub_bytes)
            return RSAKeyPair(private_key, public_key)
        except Exception as e:
            raise AsymmetricCryptoError(f"Ошибка загрузки RSA-ключей: {e}")
            
            private_key = serialization.load_pem_private_key(priv_bytes, password=None)
            public_key = serialization.load_pem_public_key(pub_bytes)
            return RSAKeyPair(private_key, public_key)
        except FileNotFoundError as e:
            raise 
        except ValueError as e: 
            
            raise e 
        except Exception as e:
            
            raise AsymmetricCryptoError(f"Ошибка загрузки RSA-ключей: {e}")

    def save_to_files(self, priv_path, pub_path):
        """
        Сохраняет RSA-ключи в файлы в формате PEM.

        Args:
            priv_path (str): Путь для сохранения приватного ключа.
            pub_path (str): Путь для сохранения публичного ключа.

        Raises:
            AsymmetricCryptoError: Для ошибок сериализации или ввода-вывода.
        """
        try:
            pub_bytes = self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            write_binary_file(pub_path, pub_bytes)
          
            priv_bytes = self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
            write_binary_file(priv_path, priv_bytes)
        except Exception as e: 
            
            raise AsymmetricCryptoError(f"Ошибка сохранения RSA-ключей: {e}")

    def encrypt_symmetric_key(self, symmetric_key):
        """
        Шифрует симметричный ключ (например, AES) с помощью публичного RSA-ключа.

        Args:
            symmetric_key (bytes): Симметричный ключ для шифрования.

        Returns:
            bytes: Зашифрованный симметричный ключ.

        Raises:
            AsymmetricCryptoError: Для ошибок шифрования.
        """
        try:
            return self.public_key.encrypt(
                symmetric_key,
                asym_padding.OAEP(
                    mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
        except Exception as e:
            
            raise AsymmetricCryptoError(f"Ошибка шифрования симметричного ключа RSA: {e}")

    def decrypt_symmetric_key(self, encrypted_symmetric_key):
        """
        Расшифровывает симметричный ключ (например, AES) с помощью приватного RSA-ключа.

        Args:
            encrypted_symmetric_key (bytes): Зашифрованный симметричный ключ.

        Returns:
            bytes: Расшифрованный симметричный ключ.

        Raises:
            AsymmetricCryptoError: Для ошибок дешифрования.
        """
        try:
            return self.private_key.decrypt(
                encrypted_symmetric_key,
                asym_padding.OAEP(
                    mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
        except Exception as e:
            
            raise AsymmetricCryptoError(f"Ошибка дешифрования симметричного ключа RSA: {e}")
