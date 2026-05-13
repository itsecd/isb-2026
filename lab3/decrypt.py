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
    Raises:
        FileNotFoundError: key file not found
    """
    try:
        with open(settings['private_key'], "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {settings}")
    
    try:
        with open(settings['symmetric_key'], "rb") as f:
            enc_sym_key = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {settings}")
    
    return private_key.decrypt(
        enc_sym_key,
        asym_padding.OAEP(mgf=asym_padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )

def sym_decrypt_encrypted_file(sym_key, input_path, output_path):
    """
    Decrypting .bin file with AES
    Read initialization vector from first file bytes
    Args:
        sym_key(bytes): sym key
        input_path(str): path to encrypted .bin file
        output_path(str): path to save decrypted file
    Raises:
        FileNotFoundError: source file for decryption not found
        OSError: Error of writing data on drive
    """
    
    try:
        with open(input_path, "rb") as f:
            data = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {input_path}")

    iv, ciphertext = data[:16], data[16:]

    cipher = Cipher(algorithms.AES(sym_key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_text = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = sym_padding.PKCS7(128).unpadder()
    text = unpadder.update(padded_text) + unpadder.finalize()

    try:
        with open(output_path, "wb") as f:
            f.write(text)
    except OSError as e:
        raise OSError(f"Ошибка сохранения файла: {e}")
    
def run_decryption(settings_path):
    """
    Runs decrypting cycle
    Args:
        settings_path: path to settings JSON file
    Returns:
        str: message of successful decryption
    Raises:
        FileNotFoundError: source file for decryption not found
        Exception: Decryption error
    """
    try:
        settings = settings_loader.load(settings_path)
        sym_key = sym_key_decrypt(settings)
        sym_decrypt_encrypted_file(sym_key, settings['encrypted_file'], settings['decrypted_file'])
        return "File decrypted successfully."
    
    except FileNotFoundError as e:
        raise Exception(f"File not found: {e}")
    except Exception as e:
        raise Exception (f"Decryption error.")
