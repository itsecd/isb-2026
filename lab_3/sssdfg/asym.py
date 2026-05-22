from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key

def encrypt_with_public_key(text: bytes, public_key_path: str) -> bytes:
    """
    Шифрует бинарные данные с помощью открытого ключа RSA.
    На вход принимает данные для шифрования и путь до файла с открытым ключом RSA.
    Возвращает зашифрованные данные.
    """
    with open(public_key_path, 'rb') as pem_in:
        public_bytes = pem_in.read()
    public_key = load_pem_public_key(public_bytes)
    c_text = public_key.encrypt(text, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
    return c_text


def decrypt_with_private_key(c_text: bytes, secret_key_path: str) -> bytes:
    """
    Расшифровывает бинарные данные с помощью закрытого ключа RSA.
    На вход принимает шифротекст и путь до файла с закрытым ключом RSA.
    Возвращает расшифрованные данные.
    """
    with open(secret_key_path, 'rb') as pem_in:
        private_bytes = pem_in.read()
        private_key = load_pem_private_key(private_bytes,password=None,)
    dc_text = private_key.decrypt(c_text,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
    return dc_text