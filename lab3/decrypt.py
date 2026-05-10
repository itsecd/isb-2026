import os
from cryptography.hazmat.primitives import serialization, hashes, padding as sym_padding
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import settings_loader

def sym_key_decrypt(settings):
    with open(settings['private_key'], "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)
    with open(settings['symmetric_key'], "rb") as f:
        enc_sym_key = f.read()
    return private_key.decrypt(
        enc_sym_key,
        asym_padding.OAEP(mgf=asym_padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )

def sym_decrypt_encrypted_file(sym_key, input_path, output_path):
    with open(input_path, "rb") as f:
        data = f.read()
        iv, ciphertext = data[:16], data[16:]

    cipher = Cipher(algorithms.AES(sym_key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_text = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = sym_padding.PKCS7(128).unpadder()
    text = unpadder.update(padded_text) + unpadder.finalize()

    with open(output_path, "wb") as f:
        f.write(text)

def run_decryption(settings_path):
    settings = settings_loader.load(settings_path)
    sym_key = sym_key_decrypt(settings)
    sym_decrypt_encrypted_file(sym_key, settings['encrypted_file'], settings['decrypted_file'])
    return "File decrypted successfully."