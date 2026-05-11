import os

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding


def generate_keys(settings: dict) -> None:
    try:
        key_length = settings['symmetric_key_length']

        print(f"Генерация Blowfish ключа длиной {key_length} бит")
        symmetric_key = os.urandom(key_length // 8)

        print("Генерация пары ключей RSA длиной 2048 бит")
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()

        with open(settings['public_key'], 'wb') as public_out:
            public_out.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

        with open(settings['secret_key'], 'wb') as private_out:
            private_out.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))

        encrypted_symmetric_key = public_key.encrypt(
            symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        with open(settings['symmetric_key'], 'wb') as file:
            file.write(encrypted_symmetric_key)

        print("Ключи были сгенерированы и сохранены в файлы")
    except IOError as error:
        print(f"Ошибка при работе с файлами: {error}")
        raise
    except Exception as error:
        print(f"Ошибка при работе: {error}")
        raise
