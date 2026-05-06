from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
import os
from decription import file_saving, file_reading

def session_key_decryption(config: dict, username: str):
    encrypted_key_path = f"encrypted_keys/{username}_session_key.enc"  
    private_key_path = config['users'][username]['private_key']   

    encrypted_key=file_reading(encrypted_key_path)

    with open(private_key_path, 'rb') as f:
        private_key = load_pem_private_key(f.read(), password=None)

    session_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return session_key

def encrypt_file_3des(input_path: str, output_path: str, key: bytes):
    with open(input_path, 'rb') as f:
        data = f.read()

    iv = os.urandom(8)

    # padding
    padder = PKCS7(64).padder()  # 64 бита = 8 байт
    padded_data = padder.update(data) + padder.finalize()

    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    file_saving(output_path, iv + ciphertext)

    print("File encrypted")

    

    

