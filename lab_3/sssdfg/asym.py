import util
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key

def encrypt_with_public_key(text: bytes, public_key_path: str) -> bytes:
    """
    Шифрует бинарные данные с помощью открытого ключа RSA.
    Принимает:
        text - открытый текст для шифрования
        public_key_path - путь до файла с открытым ключом RSA
    Возвращает зашифрованные данные.
    """
    try:
        public_bytes = util.read_file(public_key_path)
        public_key = load_pem_public_key(public_bytes)
        c_text = public_key.encrypt(text, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
        return c_text
    except FileNotFoundError:
        raise FileNotFoundError(f"Не удалось открыть файл {public_key_path}, увы")


def decrypt_with_private_key(c_text: bytes, secret_key_path: str) -> bytes:
    """
    Расшифровывает бинарные данные с помощью закрытого ключа RSA.
    Принимает:
        с_text - шифротекст для расшифровывания
        secret_key_path - путь до файла с заткрытым ключом RSA
    Возвращает расшифрованные данные.
    """
    try:
        private_bytes = util.read_file(secret_key_path)
        private_key = load_pem_private_key(private_bytes,password=None,)
        dc_text = private_key.decrypt(c_text,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
        return dc_text
    except FileNotFoundError:
        raise FileNotFoundError(f"Не удалось открыть файл {secret_key_path}, увы")