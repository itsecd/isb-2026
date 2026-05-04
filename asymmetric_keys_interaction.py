from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

def enc_sym_key(public_key,sym_key)->bytes:
    """Шифровка симметричного ключа"""
    enc_sym_key=public_key.encrypt(
        sym_key, 
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                     algorithm=hashes.SHA256(),
                     label=None)
                     )
    return enc_sym_key

def dec_sym_key(private_key,enc_sym_key)->bytes:
    """Дешифровка симметричного ключа"""
    dec_sym_key=private_key.decrypt(enc_sym_key,
                        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                     algorithm=hashes.SHA256(),
                                     label=None)
                                     )
    return dec_sym_key