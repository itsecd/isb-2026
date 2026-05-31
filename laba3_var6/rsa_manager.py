from cryptography.hazmat.primitives.asymmetric import rsa, padding as rsa_padding
from cryptography.hazmat.primitives import serialization, hashes
from exceptions import KeyGenError, EncryptError, DecryptError, KeyLoadError


class RSAProcessor:
    def __init__(self, key_bits: int, exponent: int):
        print(f"  * Генерация пары RSA ({key_bits} бит)")
        try:
            self._priv = rsa.generate_private_key(
                public_exponent=exponent,
                key_size=key_bits
            )
            self._pub = self._priv.public_key()
        except Exception as err:
            raise KeyGenError(f"Ошибка создания RSA: {err}")

    def encrypt_key(self, sym_key: bytes) -> bytes:
        print("  * RSA шифрование (OAEP с SHA-256)")
        try:
            return self._pub.encrypt(
                sym_key,
                rsa_padding.OAEP(
                    mgf=rsa_padding.MGF1(hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
        except Exception as err:
            raise EncryptError(f"RSA шифрование не удалось: {err}")

    def decrypt_key(self, enc_data: bytes) -> bytes:
        print("  * RSA расшифрование")
        try:
            return self._priv.decrypt(
                enc_data,
                rsa_padding.OAEP(
                    mgf=rsa_padding.MGF1(hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
        except Exception as err:
            raise DecryptError(f"RSA расшифрование не удалось: {err}")

    def get_public_pem(self) -> bytes:
        return self._pub.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def get_private_pem(self) -> bytes:
        return self._priv.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

    @classmethod
    def restore_from_private(cls, pem_data: bytes):
        try:
            priv_key = serialization.load_pem_private_key(pem_data, password=None)
        except Exception as err:
            raise KeyLoadError(f"Не удалось загрузить приватный RSA: {err}")
        instance = cls.__new__(cls)
        instance._priv = priv_key
        instance._pub = priv_key.public_key()
        return instance