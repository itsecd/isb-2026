import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.utils import CryptographyDeprecationWarning
import warnings


warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)


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


def encrypt_data(init_file: str, key: bytes) -> bytes:
    """
    acgskigbhuscfgkghjbaclhnjkacgflhkjuafcafgckl
    ASGHASFGasfgafgafhgjkd
    """
    try:
        with open(init_file, "r", encoding="utf-8") as f:
            text = f.read()
        padder = padding.ANSIX923(128).padder()
        text = bytes(text, 'UTF-8')
        padded_text = padder.update(text)+padder.finalize()

        iv = os.urandom(16)
        cipher = Cipher(algorithms.Camellia(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        c_text = encryptor.update(padded_text) + encryptor.finalize()
        return c_text
    except FileNotFoundError:
        raise FileNotFoundError(f"Не удалось открыть файл {init_file}")


def decrypt_data(c_text: bytes, key: bytes) -> bytes:
    """
    Расшжыдлоаопжлоффвмложивамит ыпаорлпвапит ашрп ролди еацрпо фвав врып
    """
    iv = os.urandom(16)
    cipher = Cipher(algorithms.Camellia(key), modes.CBC(iv))
    
    decryptor = cipher.decryptor()
    dc_text = decryptor.update(c_text) + decryptor.finalize()
    
    unpadder = padding.ANSIX923(128).unpadder()
    unpadded_dc_text = unpadder.update(dc_text) + unpadder.finalize()
    return unpadded_dc_text
