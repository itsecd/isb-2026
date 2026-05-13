from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding

from utils import fail, read_file, write_file


def decrypt_symmetric_key(encrypted_key: bytes, private_key) -> bytes:
    """Расшифрование симметричного ключа закрытым RSA-ключом."""
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
        fail(f"Ошибка при расшифровании симметричного ключа: {e}")


def unpad_data(data: bytes) -> bytes:
    """Удаление ANSI X.923-заполнения."""
    try:
        unpadder = sym_padding.ANSIX923(128).unpadder()
        return unpadder.update(data) + unpadder.finalize()
    except Exception as e:
        fail(f"Ошибка при удалении заполнения: {e}")


def aes_decrypt_file(input_path: str, output_path: str, key: bytes) -> None:
    """Расшифрование файла алгоритмом AES-CBC."""
    print(f"Расшифрование файла: {input_path}")
    data = read_file(input_path)

    if len(data) < 16:
        fail("Ошибка: зашифрованный файл повреждён или пуст")

    iv = data[:16]
    ciphertext = data[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor_obj = cipher.decryptor()

    try:
        padded_plaintext = decryptor_obj.update(ciphertext) + decryptor_obj.finalize()
        plaintext = unpad_data(padded_plaintext)
        write_file(output_path, plaintext)
        print(f"Файл расшифрован и сохранён: {output_path}")
    except ValueError as e:
        fail(f"Ошибка при расшифровании — возможно, неверный ключ: {e}")
    except Exception as e:
        fail(f"Ошибка при расшифровании файла: {e}")
