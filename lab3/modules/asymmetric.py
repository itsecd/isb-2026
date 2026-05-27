from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


def encrypt_symmetric_key(symmetric_key: bytes, public_key) -> bytes:
    """
    Шифрует симметричный ключ с помощью открытого ключа RSA.

    Используется схема OAEP с хеш-функцией SHA-256 и MGF1.

    Args:
        symmetric_key (bytes): симметричный ключ для шифрования.
        public_key: открытый ключ RSA.

    Returns:
        bytes: зашифрованный симметричный ключ.

    Raises:
        Exception: если произошла ошибка при шифровании
                   (например, ключ слишком длинный).
    """
    try:
        encrypted = public_key.encrypt(
            symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print("Симметричный ключ зашифрован с помощью RSA-OAEP")
        return encrypted
    except Exception as e:
        print(f"Ошибка при шифровании ключа RSA: {e}")
        raise


def decrypt_symmetric_key(encrypted_key: bytes, private_key) -> bytes:
    """
    Расшифровывает симметричный ключ с помощью закрытого ключа RSA.

    Используется схема OAEP с хеш-функцией SHA-256 и MGF1.

    Args:
        encrypted_key (bytes): зашифрованный симметричный ключ.
        private_key: закрытый ключ RSA.

    Returns:
        bytes: расшифрованный симметричный ключ.

    Raises:
        Exception: если произошла ошибка при расшифровке
                   (например, ключ повреждён или не соответствует).
    """
    try:
        symmetric_key = private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print("Симметричный ключ расшифрован с помощью RSA-OAEP")
        return symmetric_key
    except Exception as e:
        print(f"Ошибка при расшифровке ключа RSA: {e}")
        raise