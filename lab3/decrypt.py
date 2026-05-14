from cryptography.hazmat.primitives import serialization, hashes, padding as sym_padding
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import settings_loader
import file_manager

def sym_key_decrypt(settings):
    """
    Decrypting sym key with RSA private key
    Args:
        settings(dict): dictionary with settings
    Returns:
        bytes: decrypted sym key
    """
    private_key = serialization.load_pem_private_key(file_manager.read_binary(settings['private_key']), password=None)
    enc_sym_key = file_manager.read_binary(settings['symmetric_key'])
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
        ValueError: integrity error, invalid padding
    """

    data = file_manager.read_binary(input_path)

    iv, ciphertext = data[:16], data[16:]

    cipher = Cipher(algorithms.AES(sym_key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_text = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = sym_padding.PKCS7(128).unpadder()

    try:
        text = unpadder.update(padded_text) + unpadder.finalize()
    except ValueError:
        raise ValueError("Invalid padding")
    file_manager.write_binary(output_path, text)
def run_decryption(settings_path):
    """
    Runs decrypting cycle
    Args:
        settings_path: path to settings JSON file
    Returns:
        str: message of successful decryption
    Raises:
        ValueError: integrity error, padding failure
        Exception: Decryption error
    """
    try:
        settings = settings_loader.load(settings_path)
        sym_key = sym_key_decrypt(settings)
        sym_decrypt_encrypted_file(sym_key, settings['encrypted_file'], settings['decrypted_file'])
        return "File decrypted successfully."

    except ValueError as e:
        if "padding" in str(e).lower():
            raise Exception("Integrity error: data is corrupted or deleted.")
        raise Exception(f"Data format error: {e}")
    except Exception as e:
        raise Exception (f"Decryption error.")
