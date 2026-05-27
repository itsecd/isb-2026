from typing import Tuple
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding, rsa
from exceptions import AsymmetricCryptoError

class AsymmetricCipher:
    """Класс для управления асимметричным шифрованием и работы с ключами RSA."""

    def __init__(self, key_size: int = 2048, public_exponent: int = 65537):
        self._key_size = self._validate_key_size(key_size)
        self._public_exponent = self._validate_exponent(public_exponent)

    def _validate_key_size(self, key_size: int) -> int:
        try:
            size = int(key_size)
        except (TypeError, ValueError) as exc:
            raise AsymmetricCryptoError("Размер RSA-ключа должен быть числом") from exc

        if size < 2048:
            raise AsymmetricCryptoError("Размер RSA-ключа должен быть не меньше 2048 бит")
        return size

    def _validate_exponent(self, exponent: int) -> int:
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
        try:
            private_key = rsa.generate_private_key(
                public_exponent=self._public_exponent,
                key_size=self._key_size,
            )
            return private_key, private_key.public_key()
        except ValueError as exc:
            raise AsymmetricCryptoError("Не удалось сгенерировать пару ключей RSA") from exc

    def _get_oaep_padding(self) -> asym_padding.OAEP:
        return asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        )

    def serialize_public_key(self, public_key: rsa.RSAPublicKey) -> bytes:
        return public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

    def serialize_private_key(self, private_key: rsa.RSAPrivateKey) -> bytes:
        return private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )

    def load_private_key(self, key_data: bytes) -> rsa.RSAPrivateKey:
        try:
            return serialization.load_pem_private_key(key_data, password=None)
        except (TypeError, ValueError) as exc:
            raise AsymmetricCryptoError("Не удалось десериализовать закрытый RSA-ключ") from exc

    def load_public_key(self, key_data: bytes) -> rsa.RSAPublicKey:
        try:
            return serialization.load_pem_public_key(key_data)
        except (TypeError, ValueError) as exc:
            raise AsymmetricCryptoError("Не удалось десериализовать открытый RSA-ключ") from exc

    def encrypt_session_key(self, aes_key: bytes, public_key: rsa.RSAPublicKey) -> bytes:
        try:
            return public_key.encrypt(aes_key, self._get_oaep_padding())
        except (TypeError, ValueError) as exc:
            raise AsymmetricCryptoError("Ошибка шифрования ключа алгоритмом RSA-OAEP") from exc

    def decrypt_session_key(self, encrypted_key: bytes, private_key: rsa.RSAPrivateKey) -> bytes:
        try:
            return private_key.decrypt(encrypted_key, self._get_oaep_padding())
        except (TypeError, ValueError) as exc:
            raise AsymmetricCryptoError("Ошибка расшифрования ключа алгоритмом RSA-OAEP") from exc