import os
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
from utils import read_file, write_file

def encrypt_symmetric_key(symmetric_key: bytes, public_key) -> bytes:
    """Зашифровать AES-ключ открытым RSA-ключом (RSA-OAEP).
    Args:
        symmetric_key: Исходный AES-ключ (байты).
        public_key:    Объект открытого RSA-ключа.
    Returns:
        Зашифрованный ключ (байты).
    Raises:
        RuntimeError: При ошибках шифрования.
    """
    print("Шифрование симметричного ключа RSA-ключом.")
    try:
        return public_key.encrypt(
            symmetric_key,
            asym_padding.OAEP(mgf=asym_padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )
    except Exception as e:
        raise RuntimeError(f"Ошибка при шифровании симметричного ключа: {e}") from e

def pad_data(data: bytes) -> bytes:
    """Добавить ANSI X.923-заполнение до кратности 16 байт.
    Args:
        data: Исходные данные произвольной длины.
    Returns:
        Данные с дополнением (длина кратна 16).
    Raises:
        RuntimeError: При ошибках добавления заполнения.
    """
    try:
        padder = sym_padding.ANSIX923(128).padder()
        return padder.update(data) + padder.finalize()
    except Exception as e:
        raise RuntimeError(f"Ошибка при добавлении заполнения: {e}") from e

def generate_iv() -> bytes:
    """Сгенерировать случайный вектор инициализации (IV).
    Returns:
        16 криптографически случайных байт.
    Raises:
        RuntimeError: При ошибках генерации энтропии.
    """
    try:
        return os.urandom(16)
    except Exception as e:
        raise RuntimeError(f"Ошибка генерации IV: {e}") from e

def aes_encrypt_file(input_path: str, output_path: str, key: bytes) -> None:
    """Зашифровать файл алгоритмом AES-CBC.
    Args:
        input_path:  Путь к исходному файлу.
        output_path: Путь для сохранения зашифрованного файла (IV + шифротекст).
        key:         AES-ключ (16/24/32 байта).
    Raises:
        RuntimeError: При ошибках чтения, шифрования или записи.
    """
    print(f"Шифрование файла AES-CBC: {input_path}")
    plaintext = read_file(input_path)
    iv = generate_iv()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor_obj = cipher.encryptor()

    try:
        padded_plaintext = pad_data(plaintext)
        ciphertext = encryptor_obj.update(padded_plaintext) + encryptor_obj.finalize()
        write_file(output_path, iv + ciphertext)
        print(f"Файл зашифрован и сохранён: {output_path}")
    except Exception as e:
        raise RuntimeError(f"Ошибка при шифровании файла: {e}") from e
