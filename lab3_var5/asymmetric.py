from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

def encrypt_symmetric_key(symmetric_key: bytes, public_key: RSAPublicKey) -> bytes:
    """
    Шифровка симметричного ключа

    принимает:
        symmetric_key: Сгенерированный симметричный ключ 
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
    Дешифровка симметричного ключа 

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