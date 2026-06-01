from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes


def generate_rsa_keys() -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """
    Генерирует пару ключей RSA (приватный и публичный).
    Использует стандартную публичную экспоненту 65537 и размер ключа 2048 бит.
    Returns:
        tuple: Кортеж, содержащий (private_key, public_key).
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    print("Приватный и публичный ключи сгенерированы")
    return private_key, public_key


def encrypt_sym_key(sym_key: bytes, public_key: rsa.RSAPublicKey) -> bytes:
    """
    Шифрует симметричный ключ с помощью публичного ключа RSA.
    Использует схему дополнения OAEP с хешированием SHA256 для обеспечения 
    максимальной безопасности.
    Args:
        sym_key (bytes): Исходный симметричный ключ.
        public_key (rsa.RSAPublicKey): Публичный ключ RSA получателя.
    Returns:
        bytes: Зашифрованный симметричный ключ.
    """
    encrypted_key = public_key.encrypt(
        sym_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print("Симметричный ключ успешно зашифрован при помощи публичного ключа")
    return encrypted_key


def decrypt_sym_key(encrypted_sym_key: bytes, private_key: rsa.RSAPrivateKey) -> bytes:
    """
    Расшифровывает симметричный ключ с помощью приватного ключа RSA.
    Args:
        encrypted_sym_key (bytes): Зашифрованный симметричный ключ.
        private_key (rsa.RSAPrivateKey): Приватный ключ RSA для дешифрования.
    Returns:
        bytes: Расшифрованный симметричный ключ.
    Raises:
        ValueError: Если дешифрование не удалось (например, неверный ключ).
    """
    sym_key = private_key.decrypt(
        encrypted_sym_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print("Симметричный ключ успешно дешифрован при помощи приватного ключа")
    return sym_key