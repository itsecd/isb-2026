from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.asymmetric import padding as rsa_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.serialization import load_pem_private_key


def decrypt_with_keys(settings: dict) -> None:
    print("Чтение ключей и зашифрованного файла")

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

    with open(settings['encrypted_file'], 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()

    iv = encrypted_data[:8]
    cipher_text = encrypted_data[8:]

    cipher = Cipher(algorithms.Blowfish(symmetric_key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(cipher_text) + decryptor.finalize()

    unpadder = padding.PKCS7(64).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()

    with open(settings['decrypted_file'], 'wb') as file:
        file.write(data)

    print(f"Текст был расшифрован и записан в {settings['decrypted_file']}")
