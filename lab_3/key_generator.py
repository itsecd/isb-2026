"""
Модуль генерации ключей (гибридная система: SEED + RSA).
"""

import os
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from asymmetric_cipher import AsymmetricCipher


class KeyGenerator:
    """Генерация SEED (симметричного) и RSA (асимметричного) ключей."""

    @staticmethod
    def _save_bytes(path: str, data: bytes) -> None:
        """
        Args:
            path: str - путь для сохранения файла
            data: bytes - данные для записи

        Returns:
            None
        """
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as file:
            file.write(data)

    @staticmethod
    def generate(settings: dict, log_callback) -> None:
        """
        Args:
            settings: dict - словарь с путями из settings.json
            log_callback: callable - функция логирования

        Returns:
            None

        Raises:
            KeyError: отсутствует параметр в settings
        """
        try:
            symmetric_key = os.urandom(settings["symmetric_key_size"])
            log_callback("SEED ключ сгенерирован.")

            private_key = rsa.generate_private_key(
                public_exponent=settings["rsa_public_exponent"],
                key_size=settings["rsa_key_size"]
            )
            public_key = private_key.public_key()
            log_callback("RSA ключи сгенерированы.")

            public_bytes = public_key.public_bytes(
                serialization.Encoding.PEM,
                serialization.PublicFormat.SubjectPublicKeyInfo
            )
            KeyGenerator._save_bytes(settings["public_key"], public_bytes)

            private_bytes = private_key.private_bytes(
                serialization.Encoding.PEM,
                serialization.PrivateFormat.TraditionalOpenSSL,
                serialization.NoEncryption()
            )
            KeyGenerator._save_bytes(settings["private_key"], private_bytes)

            log_callback("RSA ключи сохранены.")

            encrypted_key = AsymmetricCipher.encrypt(
                symmetric_key,
                Path(settings["public_key"])
            )
            KeyGenerator._save_bytes(settings["symmetric_key"], encrypted_key)

            log_callback("SEED ключ зашифрован RSA и сохранён.")

        except KeyError as exc:
            raise KeyError(f"Отсутствует параметр в settings.json: {exc}") from exc