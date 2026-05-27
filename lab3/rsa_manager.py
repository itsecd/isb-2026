"""
Модуль асимметричного шифрования на основе алгоритма RSA.

Реализует генерацию ключей RSA, сериализацию в PEM-формат
и шифрование/расшифрование симметричного ключа по схеме OAEP.
"""

from cryptography.hazmat.primitives.asymmetric import (rsa,
                                                       padding as asym_padding)
from cryptography.hazmat.primitives import serialization, hashes
from exceptions import (KeyGenerationError,
                        EncryptionError, DecryptionError, KeyLoadError)


class RSAKeyManager:
    """
    Класс для управления RSA-ключами и операциями с ними.

    Все параметры (размер ключа, публичная экспонента) передаются
    извне при создании экземпляра. Никакие значения не захардкожены.

    Атрибуты экземпляра:
        _private: Приватный RSA-ключ.
        _public: Публичный RSA-ключ.
        _key_size (int): Размер ключа в битах.
        _public_exponent (int): Публичная экспонента.
    """

    def __init__(self, key_size: int, public_exponent: int) -> None:
        """
        Генерирует новую пару RSA-ключей.

        Аргументы:
            key_size: Размер ключа в битах.
            public_exponent: Публичная экспонента.

        Исключения:
            KeyGenerationError: Если генерация не удалась.
        """
        print(f"Генерация RSA-ключей ({key_size} бит)")
        self._key_size = key_size
        self._public_exponent = public_exponent
        try:
            self._private = rsa.generate_private_key(
                public_exponent=public_exponent,
                key_size=key_size
            )
            self._public = self._private.public_key()
            print("RSA-ключи успешно сгенерированы")
        except Exception as exc:
            raise KeyGenerationError(
                f"Не удалось сгенерировать RSA-ключи: {exc}"
            )

    @property
    def public_key(self):
        """Возвращает публичный RSA-ключ."""
        return self._public

    @property
    def private_key(self):
        """Возвращает приватный RSA-ключ."""
        return self._private

    def encrypt_key(self, symmetric_key: bytes) -> bytes:
        """
        Шифрует симметричный ключ с помощью RSA-OAEP.

        Аргументы:
            symmetric_key: Симметричный ключ для шифрования.

        Возвращает:
            bytes: Зашифрованный симметричный ключ.

        Исключения:
            EncryptionError: Если шифрование не удалось.
        """
        print("Шифрование симметричного ключа (RSA-OAEP)")
        try:
            encrypted = self._public.encrypt(
                symmetric_key,
                asym_padding.OAEP(
                    mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            print("Симметричный ключ зашифрован")
            return encrypted
        except Exception as exc:
            raise EncryptionError(
                f"Ошибка при RSA-шифровании симметричного ключа: {exc}"
            )

    def decrypt_key(self, encrypted_key: bytes) -> bytes:
        """
        Расшифровывает симметричный ключ с помощью RSA-OAEP.

        Аргументы:
            encrypted_key: Зашифрованный симметричный ключ.

        Возвращает:
            bytes: Исходный симметричный ключ.

        Исключения:
            DecryptionError: Если расшифрование не удалось.
        """
        print("Расшифрование симметричного ключа (RSA-OAEP)")
        try:
            decrypted = self._private.decrypt(
                encrypted_key,
                asym_padding.OAEP(
                    mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            print("Симметричный ключ расшифрован")
            return decrypted
        except Exception as exc:
            raise DecryptionError(
                f"Ошибка при RSA-расшифровании симметричного ключа: {exc}. "
                f"Возможно,"
                f" ключ повреждён или используется неверный приватный ключ."
            )

    def serialize_public(self) -> bytes:
        """Сериализует публичный ключ в PEM."""
        return self._public.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def serialize_private(self) -> bytes:
        """Сериализует приватный ключ в PEM."""
        return self._private.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

    @classmethod
    def load_from_private_pem(cls, pem_bytes: bytes) -> 'RSAKeyManager':
        """
        Создаёт экземпляр из PEM-байтов приватного ключа.

        Аргументы:
            pem_bytes: Приватный ключ в PEM-формате.

        Возвращает:
            RSAKeyManager: Новый экземпляр с загруженным ключом.

        Исключения:
            KeyLoadError: Если не удалось загрузить ключ.
        """
        try:
            private_key = serialization.load_pem_private_key(
                pem_bytes, password=None
            )
        except Exception as exc:
            raise KeyLoadError(
                f"Не удалось загрузить приватный RSA-ключ: {exc}"
            )

        instance = cls.__new__(cls)
        instance._private = private_key
        instance._public = private_key.public_key()
        instance._key_size = instance._private.key_size
        instance._public_exponent = None
        return instance