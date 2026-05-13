from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding

from utils import fail, read_file, write_file


def decrypt_symmetric_key(encrypted_key: bytes, private_key) -> bytes:
    """
    Расшифровать AES-ключ закрытым RSA-ключом.

    Параметры:
        encrypted_key: зашифрованный RSA-OAEP ключ (байты).
        private_key:  закрытый RSA-ключ.

    Возвращает:
        Расшифрованный AES-ключ (16/24/32 байта).
    """
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
    """
    Удалить ANSI X.923-заполнение.

    Параметры:
        data: данные с заполнением (длина кратна 16).

    Возвращает:
        Данные без заполнения.
    """
    try:
        unpadder = sym_padding.ANSIX923(128).unpadder()
        return unpadder.update(data) + unpadder.finalize()
    except Exception as e:
        fail(f"Ошибка при удалении заполнения: {e}")


def aes_decrypt_file(input_path: str, output_path: str, key: bytes) -> None:
    """
    Расшифровать файл алгоритмом AES-CBC.

    Параметры:
        input_path:  путь к зашифрованному файлу (первые 16 байт — IV).
        output_path: путь для сохранения расшифрованного файла.
        key:         AES-ключ (16/24/32 байта).

    Ошибки:
        - файл короче 16 байт → повреждён,
        - неверный ключ → ValueError при удалении заполнения.
    """
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
