import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding as sym_padding  
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey 



def encrypt_text(text:str, key:bytes)->bytes:
    data = text.encode('utf-8')
    padder = sym_padding.PKCS7(64).padder()
    padded_data = padder.update(data) + padder.finalize()
    iv = os.urandom(8)
    cipher = Cipher(algorithms.CAST5(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv + ciphertext


def encrypt_symmetric_key(public_key)-> bytes:
    encrypted_key = public_key.encrypt(symmetric_key,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
    return encrypted_key