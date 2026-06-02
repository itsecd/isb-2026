from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding, rsa


def generate_rsa_keypair():
    """Генерирует пару ключей RSA."""
    keys = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return keys, keys.public_key()


def encrypt_idea_key_rsa(idea_key: bytes, public_key) -> bytes:
    """Шифрует IDEA ключ с помощью RSA."""
    try:
        return public_key.encrypt(
            idea_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except Exception as e:
        raise RuntimeError(f"Ошибка шифрования RSA: {e}")


def decrypt_idea_key_rsa(encrypted_key: bytes, private_key) -> bytes:
    """Расшифровывает IDEA ключ."""
    try:
        return private_key.decrypt(
            encrypted_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except ValueError:
        raise ValueError("Ошибка расшифровки ключа IDEA, неверный ключ или ключ повреждён.")