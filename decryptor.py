from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
from utils import read_file, write_file

def decrypt_symmetric_key(encrypted_key: bytes, private_key) -> bytes:
    """Расшифровать AES-ключ закрытым RSA-ключом (RSA-OAEP).
    Args:
        encrypted_key: Зашифрованный RSA-OAEP ключ (байты).
        private_key:   Объект закрытого RSA-ключа.
    Returns:
        Расшифрованный AES-ключ (16/24/32 байта).
    Raises:
        RuntimeError: При ошибках расшифрования или неверном ключе.
    """
    print("Расшифрование симметричного ключа RSA-ключом.")
    try:
        return private_key.decrypt(
            encrypted_key,
            asym_padding.OAEP(mgf=asym_padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )
    except Exception as e:
        raise RuntimeError(f"Ошибка при расшифровании симметричного ключа: {e}") from e

def unpad_data(data: bytes) -> bytes:
    """Удалить ANSI X.923-заполнение.
    Args:
        data: Данные с заполнением (длина кратна 16).
    Returns:
        Исходные данные без дополнения.
    Raises:
        RuntimeError: При ошибках удаления заполнения (битый паддинг).
    """
    try:
        unpadder = sym_padding.ANSIX923(128).unpadder()
        return unpadder.update(data) + unpadder.finalize()
    except Exception as e:
        raise RuntimeError(f"Ошибка при удалении заполнения: {e}") from e

def aes_decrypt_file(input_path: str, output_path: str, key: bytes) -> None:
    """Расшифровать файл алгоритмом AES-CBC.
    Args:
        input_path:  Путь к зашифрованному файлу (первые 16 байт — IV).
        output_path: Путь для сохранения расшифрованного файла.
        key:         AES-ключ, используемый при шифровании.
    Raises:
        ValueError:    Если файл повреждён, пуст или ключ неверный.
        RuntimeError:  При других ошибках чтения/записи/расшифрования.
    """
    print(f"Расшифрование файла: {input_path}")
    data = read_file(input_path)

    match len(data):
        case n if n < 16:
            raise ValueError("Зашифрованный файл повреждён или пуст")
        case _:
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
        raise ValueError("Ошибка при расшифровании: возможно, неверный ключ") from e
    except Exception as e:
        raise RuntimeError(f"Ошибка при расшифровании файла: {e}") from e
