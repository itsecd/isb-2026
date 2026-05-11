import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.asymmetric import padding as rsa_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.serialization import load_pem_private_key


def encrypt_with_keys(settings: dict) -> None:
    try:
        print("Чтение ключей и исходного файла")

        with open(settings['secret_key'], 'rb') as private_file:
            private_key = load_pem_private_key(private_file.read(), password=None)

        with open(settings['symmetric_key'], mode='rb') as key_file:
            encrypted_symmetric_key = key_file.read()

        symmetric_key = private_key.decrypt(
            encrypted_symmetric_key,
            rsa_padding.OAEP(
                mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        with open(settings['initial_file'], 'rb') as initial_file:
            data = initial_file.read()

        padder = padding.PKCS7(64).padder()
        padded_data = padder.update(data) + padder.finalize()

        iv = os.urandom(8)
        cipher = Cipher(algorithms.Blowfish(symmetric_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        cipher_text = encryptor.update(padded_data) + encryptor.finalize()

        with open(settings['encrypted_file'], 'wb') as file:
            file.write(iv + cipher_text)

        print(f"Текст был зашифрован и записан в {settings['encrypted_file']}")
    except IOError as error:
        print(f"Ошибка при работе с файлами: {error}")
        raise
    except Exception as error:
        print(f"Ошибка при работе: {error}")
        raise
