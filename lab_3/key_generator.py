"""
Модуль генерации ключей.
"""

import os
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from asymmetric_cipher import AsymmetricCipher


class KeyGenerator:
    """Генерация SEED и RSA ключей."""

    KEY_SIZE = 16

    @staticmethod
    def generate(settings: dict, log_callback) -> None:
        """Генерация ключей гибридной системы."""
        try:
            symmetric_key = os.urandom(KeyGenerator.KEY_SIZE)
            log_callback("SEED ключ сгенерирован.")

            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
            public_key = private_key.public_key()

            Path(settings["public_key"]).parent.mkdir(
                parents=True, exist_ok=True
            )

            with open(settings["public_key"], "wb") as file:
                file.write(
                    public_key.public_bytes(
                        serialization.Encoding.PEM,
                        serialization.PublicFormat.SubjectPublicKeyInfo
                    )
                )

            with open(settings["private_key"], "wb") as file:
                file.write(
                    private_key.private_bytes(
                        serialization.Encoding.PEM,
                        serialization.PrivateFormat.TraditionalOpenSSL,
                        serialization.NoEncryption()
                    )
                )

            log_callback("RSA ключи сохранены.")

            encrypted_key = AsymmetricCipher.encrypt(
                symmetric_key,
                Path(settings["public_key"])
            )

            with open(settings["symmetric_key"], "wb") as file:
                file.write(encrypted_key)

            log_callback("SEED ключ зашифрован RSA.")

        except KeyError as exc:
            raise KeyError(f"Отсутствует параметр в settings.json: {exc}") from exc