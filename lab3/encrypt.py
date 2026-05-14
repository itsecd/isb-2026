import os
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

def sym_encrypt_source(sym_key, input_path, output_path):
    """
    Encrypting source file with AES,
    adds an initialization vector to the beginning of the file
    Args:
        sym_key(bytes): sym key
        input_path(str): path to source file
        output_path(str): path to save encrypted .bin file
    Raises:
        FileNotFoundError: source file for encryption not found
        OSError: Error of writing data on drive
    """
    data = file_manager.read_binary(input_path)
    iv = os.urandom(16)
    padder = sym_padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    cipher = Cipher(algorithms.AES(sym_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    file_manager.write_binary(output_path, iv + ciphertext)
def run_encryption(settings_path):
    """
    Runs ecnrypting cycle
    Args:
        settings_path: path to settings JSON file
    Returns:
        str: message of successful encryption
    Raises:
        FileNotFoundError: source file for encryption not found
        ValueError: incorrect file format
        Exception: Encryption error
    """
    try:
        settings = settings_loader.load(settings_path)
        if not os.path.exists(settings['initial_file']):
            raise FileNotFoundError(f"Source file not found: {settings['initial_file']}")

        sym_key = sym_key_decrypt(settings)
        sym_encrypt_source(sym_key, settings['initial_file'], settings['encrypted_file'])
        return "File encrypted successfully."
    except ValueError:
        raise Exception("Error: incorrect private key or AES key format.")
    except Exception as e:
        raise Exception(f"Encryption error: {e}")
