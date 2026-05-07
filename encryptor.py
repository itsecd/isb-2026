import os
import sys

from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding


def encrypt_symmetric_key(symmetric_key, public_key):
    print("Шифрование симметричного ключа RSA-ключом.")
    try:
        encrypted_key = public_key.encrypt(
            symmetric_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print("Симметричный ключ зашифрован")
        return encrypted_key
    except Exception as e:
        print(f"Ошибка при шифровании симметричного ключа: {e}")
        sys.exit(1)


def pad_data(data):
    padder = sym_padding.ANSIX923(128).padder()
    return padder.update(data) + padder.finalize()


def aes_encrypt_file(input_path, output_path, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor_obj = cipher.encryptor()

    print(f"Шифрование файла AES-CBC: {input_path}")
    try:
        with open(input_path, 'rb') as f:
            plaintext = f.read()
    except FileNotFoundError:
        print(f"Файл не найден: {input_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при чтении файла для шифрования: {e}")
        sys.exit(1)

    try:
        padded_plaintext = pad_data(plaintext)
        ciphertext = encryptor_obj.update(padded_plaintext) + encryptor_obj.finalize()

        with open(output_path, 'wb') as f:
            f.write(iv + ciphertext)
        print(f"Файл зашифрован и сохранён: {output_path}")
    except Exception as e:
        print(f"Ошибка при шифровании файла: {e}")
        sys.exit(1)