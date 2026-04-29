from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding

def decrypt_text(encrypt_text: bytes, key: bytes) -> str:
    """
    Дешифрование данных алгоритмом CAST5.
    """
    
    iv = encrypt_text[:8]
    ciphertext = encrypt_text[8:]
    
    cipher = Cipher(algorithms.CAST5(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    
    unpadder = sym_padding.PKCS7(64).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    
    
    return data.decode('utf-8')



def decrypt_key(encrypt_sym_key:bytes, private_key:RSAPrivateKey) -> bytes:
    """
    Дешифровка симметричного ключа 
    """
    dc_key = private_key.decrypt(encrypt_sym_key,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
    return dc_key