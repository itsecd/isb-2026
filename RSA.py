from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes


def generate():
    """
      Генерирует пару RSA-ключей (приватный и публичный)

      Returns:
          tuple: (private_key, public_key)
      """
    keys = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
    )
    private_key = keys
    public_key = keys.public_key()

    return private_key,public_key

def encryption(text: bytes, public_key) -> bytes:
    """
       Шифрует данные с использованием RSA-OAEP.

       Args:
           text (bytes): открытые данные.
           public_key: публичный RSA-ключ.

       Returns:
           bytes: зашифрованные данные.
       """
    c_text = public_key.encrypt(text, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
    return c_text


def decryption(c_text: bytes, private_key) -> bytes:
    """
    Расшифровывает данные, зашифрованные RSA-OAEP.

    Args:
        c_text (bytes): зашифрованные данные.
        private_key: приватный RSA-ключ.

    Returns:
        bytes: расшифрованные данные.
    """
    dc_text = private_key.decrypt(c_text,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(),label=None))
    return dc_text
