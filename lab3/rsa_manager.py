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

    Инкапсулирует генерацию, сериализацию, шифрование и расшифрование
    симметричного ключа с использованием RSA-OAEP.

    Атрибуты класса:
        KEY_SIZE (int): Размер RSA-ключа в битах (2048).
        PUBLIC_EXPONENT (int): Публичная экспонента (65537).

    Атрибуты экземпляра:
        _private: Приватный RSA-ключ.
        _public: Публичный RSA-ключ.
    """

    KEY_SIZE: int = 2048
    PUBLIC_EXPONENT: int = 65537

    def __init__(self) -> None:
        """
        Инициализирует менеджер и генерирует новую пару RSA-ключей.

        При создании объекта автоматически вызывается генерация ключей.

        Исключения:
            KeyGenerationError: Если генерация ключей не удалась.
        """
        print(f"Генерация RSA-ключей ({self.KEY_SIZE} бит)")
        try:
            self._private = rsa.generate_private_key(
                public_exponent=self.PUBLIC_EXPONENT,
                key_size=self.KEY_SIZE
            )
            self._public = self._private.public_key()
            print("RSA-ключи успешно сгенерированы")
        except Exception as exc:
            raise KeyGenerationError(
                f"Не удалось сгенерировать RSA-ключи: {exc}"
            )

    @property
    def public_key(self):
        """
        Возвращает публичный RSA-ключ.

        Возвращает:
            Публичный ключ RSA.
        """
        return self._public

    @property
    def private_key(self):
        """
        Возвращает приватный RSA-ключ.

        Возвращает:
            Приватный ключ RSA.
        """
        return self._private

    def encrypt_key(self, symmetric_key: bytes) -> bytes:
        """
        Шифрует симметричный ключ с помощью RSA-OAEP.

        Использует схему OAEP с хеш-функцией SHA-256 для обеспечения
        семантической безопасности.

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
            DecryptionError: Если расшифрование не удалось
             (неверный ключ или данные).
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
                f"Возможно, ключ повреждён"
                f" или используется неверный приватный ключ."
            )

    def serialize_public(self) -> bytes:
        """
        Сериализует публичный ключ в формат PEM.

        Возвращает:
            bytes: Публичный ключ в PEM-формате.
        """
        return self._public.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def serialize_private(self) -> bytes:
        """
        Сериализует приватный ключ в формат PEM без шифрования.

        Возвращает:
            bytes: Приватный ключ в PEM-формате.
        """
        return self._private.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

    @classmethod
    def load_from_private_pem(cls, pem_bytes: bytes) -> 'RSAKeyManager':
        """
        Создаёт экземпляр RSAKeyManager из PEM-байтов приватного ключа.

        Это фабричный метод: он не вызывает __init__,
        а создаёт объект и заполняет его поля из существующего ключа.

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
        return instance