import os
from cryptography.hazmat.primitives import serialization, hashes, padding as sym_padding
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import settings_loader

def sym_key_decrypt(settings):
    """
    Decrypting sym key with RSA private key
    Args:
        settings(dict): dictionary with settings
    Returns:
        bytes: decrypted sym key
    """
    with open(settings['private_key'], "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)
    with open(settings['symmetric_key'], "rb") as f:
        enc_sym_key = f.read()
    return private_key.decrypt(
        enc_sym_key,
        asym_padding.OAEP(mgf=asym_padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )

def sym_encrypt_source(sym_key, input_path, output_path):
    """
    Encrypting source file with AES,
    adds an initialization vector to the beginning of the file
    Args:
        sym_key(bytes): sym key
        input_path(str): path to source file
        output_path(str): path to save encrypted .bin file
    """
    with open(input_path, "rb") as f:
        data = f.read()

    iv = os.urandom(16)
    padder = sym_padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    cipher = Cipher(algorithms.AES(sym_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    with open(output_path, "wb") as f:
        f.write(iv + ciphertext)

def run_encryption(settings_path):
    """
    Runs ecnrypting cycle
    Args:
        settings_path: path to settings JSON file
    Returns:
        str: message of successful encryption
    """
    settings = settings_loader.load(settings_path)
    sym_key = sym_key_decrypt(settings)
    sym_encrypt_source(sym_key, settings['initial_file'], settings['encrypted_file'])
    return "File encrypted successfully."