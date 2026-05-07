import sys

from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding


def decrypt_symmetric_key(encrypted_key, private_key):
    print("Расшифрование симметричного ключа RSA-ключом.")
    try:
        key = private_key.decrypt(
            encrypted_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print("Симметричный ключ расшифрован")
        return key
    except Exception as e:
        print(f"Ошибка при расшифровании симметричного ключа: {e}")
        sys.exit(1)


def unpad_data(data):
    unpadder = sym_padding.ANSIX923(128).unpadder()
    return unpadder.update(data) + unpadder.finalize()


def aes_decrypt_file(input_path, output_path, key):
    print(f"Расшифрование файла: {input_path}")
    try:
        with open(input_path, 'rb') as f:
            data = f.read()
    except FileNotFoundError:
        print(f"Файл не найден: {input_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при чтении файла для расшифрования: {e}")
        sys.exit(1)

    if len(data) < 16:
        print("Ошибка: зашифрованный файл повреждён или пуст")
        sys.exit(1)

    iv = data[:16]
    ciphertext = data[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor_obj = cipher.decryptor()

    try:
        padded_plaintext = decryptor_obj.update(ciphertext) + decryptor_obj.finalize()
        plaintext = unpad_data(padded_plaintext)

        with open(output_path, 'wb') as f:
            f.write(plaintext)
        print(f"Файл расшифрован и сохранён: {output_path}")
    except ValueError as e:
        print(f"Ошибка при расшифровании — возможно, неверный ключ: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при расшифровании файла: {e}")
        sys.exit(1)