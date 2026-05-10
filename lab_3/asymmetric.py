from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding, rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

from utils import load_private_key, read_bytes


def generate_rsa_keys() -> tuple[RSAPrivateKey, RSAPublicKey]:
    """Генерирует пару RSA ключей — закрытый и открытый."""
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return private_key, private_key.public_key()


def encrypt_symmetric_key(symmetric_key: bytes, public_key: RSAPublicKey) -> bytes:
    """
    Шифрует симметричный ключ открытым RSA ключом.

    Args:
        symmetric_key: симметричный ключ в байтах
        public_key: открытый RSA ключ
    """
    return public_key.encrypt(
        symmetric_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def decrypt_symmetric_key(encrypted_key: bytes, private_key: RSAPrivateKey) -> bytes:
    """
    Расшифровывает симметричный ключ закрытым RSA ключом.

    Args:
        encrypted_key: зашифрованный симметричный ключ в байтах
        private_key: закрытый RSA ключ
    """
    try:
        return private_key.decrypt(
            encrypted_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
    except Exception as e:
        raise RuntimeError(f"Симметричный ключ не расшифровался: {e}")


def get_symmetric_key(path_symmetric_key: str, path_private_key: str) -> bytes:
    """
    Читает и расшифровывает симметричный ключ с помощью закрытого RSA ключа.

    Args:
        path_symmetric_key: путь к зашифрованному симметричному ключу
        path_private_key: путь к закрытому RSA ключу
    """
    encrypted_key = read_bytes(path_symmetric_key)
    private_key = load_private_key(path_private_key)
    return decrypt_symmetric_key(encrypted_key, private_key)