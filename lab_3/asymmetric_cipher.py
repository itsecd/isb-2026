"""
Модуль RSA шифрования.
"""

from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from file_manager import FileManager


class AsymmetricCipher:
    """RSA шифрование и дешифрование."""

    @staticmethod
    def encrypt(data: bytes, public_key_path: Path) -> bytes:
        """
        Args:
            data: bytes - данные для шифрования
            public_key_path: Path - путь к файлу публичного ключа PEM

        Returns:
            bytes - зашифрованные данные

        Raises:
            FileNotFoundError: файл ключа не существует
            RuntimeError: ошибка шифрования
        """
        if not public_key_path.exists():
            raise FileNotFoundError("Файл открытого ключа не найден.")

        try:
            public_key_data = FileManager.read(str(public_key_path))
            public_key = serialization.load_pem_public_key(public_key_data)

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
        """
        Args:
            data: bytes - зашифрованные данные
            private_key_path: Path - путь к файлу приватного ключа PEM

        Returns:
            bytes - расшифрованные данные

        Raises:
            FileNotFoundError: файл ключа не существует
            RuntimeError: ошибка дешифрования
        """
        if not private_key_path.exists():
            raise FileNotFoundError("Файл закрытого ключа не найден.")

        try:
            private_key_data = FileManager.read(str(private_key_path))
            private_key = serialization.load_pem_private_key(
                private_key_data,
                password=None
            )

            return private_key.decrypt(
                data,
                padding.OAEP(
                    mgf=padding.MGF1(hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

        except Exception as exc:
            raise RuntimeError(f"Ошибка RSA дешифрования: {exc}") from exc