from incription import session_key_decryption
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7

def file_reading(input_path: str) -> bytes:
    try:
        with open(input_path, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        raise Exception(f"File not found: {input_path}")
    except PermissionError:
        raise Exception(f"No access to file: {input_path}")
    except Exception as e:
        raise Exception(f"Error during file reading {input_path}: {e}")
    
def file_saving(output_path: str, data: bytes):
    try:
        with open(output_path, 'wb') as f:
            f.write(data)
    except PermissionError:
        raise Exception(f"No access to  save file: {output_path}")
    except FileNotFoundError:
        raise Exception(f"File not found: {output_path}")
    except Exception as e:
        raise Exception(f"Error during file reading {output_path}: {e}")
    

def decrypt_file_3des(input_path: str, output_path: str, key: bytes):
    data = file_reading(input_path)

    iv = data[:8]
    ciphertext = data[8:]

    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = PKCS7(64).unpadder()
    plaintext = unpadder.update(padded_data) + unpadder.finalize()

    file_saving(output_path, plaintext)

    print("File decrypted")