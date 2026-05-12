from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as assym_padding, rsa

def generate_rsa_keypair():
    keys = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return keys, keys.public_key()

def encrypt_idea_key_rsa(idea_key: bytes, public_key) -> bytes:
    try:
        return public_key.encrypt(
            idea_key,
            assym_padding.OAEP(
                mgf=assym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except Exception as e:
        raise RuntimeError(f"Ошибка шифрования RSA: {e}")

def decrypt_idea_key_rsa(encrypted_key: bytes, private_key) -> bytes:
    try:
        return private_key.decrypt(
            encrypted_key, 
            assym_padding.OAEP(
                mgf=assym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except ValueError:
        raise ValueError("Ошибка расшифровки ключа IDEA, неверный ключ или ключ повреждён.")