"""
Модуль генерации ключей (гибридная система: SEED + RSA).
"""

import os
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from asymmetric_cipher import AsymmetricCipher
from file_manager import FileManager


class KeyGenerator:
    """Генерация SEED (симметричного) и RSA (асимметричного) ключей."""

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
            FileManager.write(settings["public_key"], public_bytes)

            private_bytes = private_key.private_bytes(
                serialization.Encoding.PEM,
                serialization.PrivateFormat.TraditionalOpenSSL,
                serialization.NoEncryption()
            )
            FileManager.write(settings["private_key"], private_bytes)

            log_callback("RSA ключи сохранены.")

            encrypted_key = AsymmetricCipher.encrypt(
                symmetric_key,
                Path(settings["public_key"])
            )
            FileManager.write(settings["symmetric_key"], encrypted_key)

            log_callback("SEED ключ зашифрован RSA и сохранён.")

        except KeyError as exc:
            raise KeyError(f"Отсутствует параметр в settings.json: {exc}") from exc