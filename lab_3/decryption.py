from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from utils import load_private_key, read_bytes, write_bytes


def decrypt(
    path_cipher_text: str,
    path_asymmetric_private_text: str,
    path_symmetric_key: str,
    path_original_text: str,
) -> None:
    """
    Функция для расшифровки файла с помощью алгоритма SEED.
    Симметричный ключ расшифровывается закрытым RSA ключом перед использованием.
    Первые 16 байт зашифрованного файла считаются вектором инициализации.
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

    print(f"Чтение зашифрованного файла из {path_cipher_text}:")
    data = read_bytes(path_cipher_text)
    print("Зашифрованный файл считан")

    print("Расшифровка файла SEED-CBC:")
    try:
        iv = data[:16]
        c_text = data[16:]

        cipher = Cipher(algorithms.SEED(symmetric_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        c_text = decryptor.update(c_text) + decryptor.finalize()

        unpadder = padding.ANSIX923(128).unpadder()
        unpadded_c_text = unpadder.update(c_text) + unpadder.finalize()
    except Exception as e:
        raise RuntimeError(f"Файл не расшифровался: {e}")
    print("Файл расшифрован")

    print(f"Сохранение расшифрованного файла в {path_original_text}:")
    write_bytes(path_original_text, unpadded_c_text)
    print("Расшифровка завершена успешно")