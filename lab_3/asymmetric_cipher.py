"""
Модуль RSA шифрования.
"""

from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization


class AsymmetricCipher:
    """RSA шифрование и дешифрование."""

    @staticmethod
    def encrypt(data: bytes, public_key_path: Path) -> bytes:
        """Шифрует данные открытым RSA ключом."""
        if not public_key_path.exists():
            raise FileNotFoundError("Файл открытого ключа не найден.")

        try:
            with open(public_key_path, "rb") as file:
                public_key = serialization.load_pem_public_key(file.read())

            return public_key.encrypt(
                data,
                padding.OAEP(
                    mgf=padding.MGF1(hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

        except Exception as exc:
            raise RuntimeError(f"Ошибка RSA шифрования: {exc}") from exc

    @staticmethod
    def decrypt(data: bytes, private_key_path: Path) -> bytes:
        """Дешифрует данные закрытым RSA ключом."""
        if not private_key_path.exists():
            raise FileNotFoundError("Файл закрытого ключа не найден.")

        try:
            with open(private_key_path, "rb") as file:
                private_key = serialization.load_pem_private_key(
                    file.read(),
                    password=None
                )

            return private_key.decrypt(data,
                padding.OAEP(mgf=padding.MGF1(hashes.SHA256()),algorithm=hashes.SHA256(),label=None))

        except Exception as exc:
            raise RuntimeError(f"Ошибка RSA дешифрования: {exc}") from exc