from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes


def generate_keys():
    try:
        private = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        return private, private.public_key()

    except Exception as e:
        raise RuntimeError(f"[RSA ERROR] Ошибка генерации ключей: {e}")


def encrypt_key(public_key, key: bytes) -> bytes:
    try:
        return public_key.encrypt(
            key,
            padding.OAEP(
                mgf=padding.MGF1(hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except Exception as e:
        raise RuntimeError(f"[RSA ERROR] Ошибка шифрования ключа: {e}")


def decrypt_key(private_key, encrypted: bytes) -> bytes:
    try:
        return private_key.decrypt(
            encrypted,
            padding.OAEP(
                mgf=padding.MGF1(hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except Exception as e:
        raise RuntimeError(f"[RSA ERROR] Ошибка расшифрования ключа: {e}")


def save_private(private_key) -> bytes:
    try:
        return private_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption()
        )
    except Exception as e:
        raise RuntimeError(f"[RSA ERROR] Ошибка сериализации private key: {e}")


def save_public(public_key) -> bytes:
    try:
        return public_key.public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo
        )
    except Exception as e:
        raise RuntimeError(f"[RSA ERROR] Ошибка сериализации public key: {e}")


def load_private(data: bytes):
    try:
        return serialization.load_pem_private_key(data, password=None)
    except ValueError:
        raise ValueError("[RSA ERROR] Невалидный private key")
    except Exception as e:
        raise RuntimeError(f"[RSA ERROR] Ошибка загрузки private key: {e}")
