import os
from cryptography.hazmat.primitives.asymmetric import rsa
import util


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
    """
    Генерирует пару ключей RSA и сериализует их в .pem файлы.
    На вход принимает пути, по которым сохраняются ключи.
    """
    try:
        keys = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        private_key = keys
        public_key = keys.public_key()
        util.write_public_key(public_filepath, public_key)
        util.write_private_key(private_filepath, private_key)
        return
    except FileNotFoundError:
        raise FileNotFoundError(f"Не удалось открыть файл {public_filepath}, увы")


