import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def volshebniy_kluch(key_length: int) -> bytes:
    """
    Генерирует ключ для алгоритма Camellia длиной 128, 192 или 256 байтов.
    На вход принимает длину ключа и возвращает ключ заданной длины.
    Для нестандартных значений длины возвращает ошибку.
    """
    if (key_length in [128,192,256]):
        return os.urandom(key_length//8)
    else:
        raise RuntimeError("Привет, я люблю числа 128, 192 и 256 и обожаю делать ключи такой длины.")
    

def asym_keygen(public_filepath: str, private_filepath: str) -> None:
    keys = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_key = keys
    public_key = keys.public_key()
    public_pem = public_filepath
    with open(public_pem, 'wb') as public_out:
            public_out.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo))
    private_pem = private_filepath
    with open(private_pem, 'wb') as private_out:
            private_out.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()))
    return