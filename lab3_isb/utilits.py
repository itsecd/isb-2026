from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding

def decrypt_symmetric_key(enc_key: bytes, private_key: RSAPrivateKey) -> bytes:
    """
    Дешифрование симметричного AES-ключа закрытым RSA-ключом.
    :param enc_key: зашифрованный симметричный AES-ключ
    :param private_key: закрытый RSA-ключ для дешифрования симметричного ключа
    :return: расшифрованный симметричный AES-ключ в виде байтов
    """

    padder = asym_padding.OAEP(mgf=asym_padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    decrypted_key = private_key.decrypt(enc_key, padder)
    return decrypted_key
