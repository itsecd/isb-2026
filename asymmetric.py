from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey


def encrypt_symmetric_key(symmetric_key: bytes, public_key: RSAPublicKey) -> bytes:
    """
    Шифрование симметричного ключа открытым ключом RSA

    принимает:
        symmetric_key: Сгенерированный симметричный ключ AES
        public_key: Открытый ключ RSA

    возвращает:
        bytes: Зашифрованный симметричный ключ
    """
    encrypted_key = public_key.encrypt(
        symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_key


def decrypt_key(encrypt_sym_key: bytes, private_key: RSAPrivateKey) -> bytes:
    """
    Дешифрование симметричного ключа закрытым ключом RSA

    принимает:
        encrypt_sym_key: Зашифрованный симметричный ключ
        private_key: Закрытый ключ RSA

    возвращает:
        bytes: Расшифрованный симметричный ключ
    """
    dc_key = private_key.decrypt(
        encrypt_sym_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return dc_key