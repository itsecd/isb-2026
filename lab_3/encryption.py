import os

from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from utils import load_private_key, read_bytes, write_bytes


def encrypt(
    path_original_text: str,
    path_asymmetric_private_text: str,
    path_symmetric_key: str,
    path_cipher_text: str,
) -> None:
    """
    Функция для зашифровки файла с помощью алгоритма SEED.
    Симметричный ключ расшифровывается закрытым RSA ключом перед использованием.
    Результат сохраняется в зашифрованный файл вместе с вектором инициализации.
    """
    print(f"Чтение симметричного ключа из {path_symmetric_key}:")
    symmetric_key = read_bytes(path_symmetric_key)
    print("Симметричный ключ считан")

    print(f"Загрузка закрытого ключа из {path_asymmetric_private_text}:")
    private_key = load_private_key(path_asymmetric_private_text)
    print("Закрытый ключ считан")

    print("Расшифровка симметричного ключа закрытым RSA ключом:")
    try:
        symmetric_key = private_key.decrypt(
            symmetric_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
    except Exception as e:
        raise RuntimeError(f"Симметричный ключ не расшифровался: {e}")
    print("Симметричный ключ расшифрован")

    print(f"Чтение исходного файла из {path_original_text}:")
    text = read_bytes(path_original_text)
    print("Исходный файл считан")

    print("Шифрование файла SEED-CBC:")
    try:
        padder = padding.ANSIX923(128).padder()
        text = padder.update(text) + padder.finalize()

        iv = os.urandom(16)
        cipher = Cipher(algorithms.SEED(symmetric_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        c_text = encryptor.update(text) + encryptor.finalize()
    except Exception as e:
        raise RuntimeError(f"Файл не зашифровался: {e}")
    print("Файл зашифрован")

    print(f"Сохранение зашифрованного файла в {path_cipher_text}:")
    write_bytes(path_cipher_text, iv + c_text)
    print("Шифрование завершено успешно")