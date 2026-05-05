from incription import session_key_decryption
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7

def decrypt_file_3des(input_path: str, output_path: str, key: bytes):
    with open(input_path, 'rb') as f:
        data = f.read()

    iv = data[:8]
    ciphertext = data[8:]

    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = PKCS7(64).unpadder()
    plaintext = unpadder.update(padded_data) + unpadder.finalize()

    # сохраняем
    with open(output_path, 'wb') as f:
        f.write(plaintext)

    print("File decrypted")