from Crypto.Cipher import CAST
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from file_utils import validate_key_length, file_exists, load_bytes, save_bytes


def generate_cast5_key(length_bits: int) -> bytes:
    """
    Генерирует случайный ключ CAST-5 заданной длины.

    Args:
        length_bits: Длина ключа в битах (40-128, кратно 8).

    Returns:
        bytes: Ключ указанной длины.
    """
    validate_key_length(length_bits)
    return get_random_bytes(length_bits // 8)


def encrypt_cast5_file(input_path: str, output_path: str, key: bytes) -> None:
    """
    Шифрует файл CAST-5 в режиме CBC.

    Args:
        input_path: Путь к исходному файлу.
        output_path: Путь для сохранения зашифрованного файла.
        key: Ключ шифрования.
    """
    if not file_exists(input_path):
        raise FileNotFoundError(f"Файл для шифрования не найден: {input_path}")
    if not key:
        raise ValueError("Ключ не может быть пустым")

    plain_data = load_bytes(input_path)

    cipher = CAST.new(key, CAST.MODE_CBC)
    iv = cipher.iv
    encrypted_data = cipher.encrypt(pad(plain_data, CAST.block_size))

    save_bytes(iv + encrypted_data, output_path)


def decrypt_cast5_file(input_path: str, output_path: str, key: bytes) -> None:
    """
    Расшифровывает файл, зашифрованный encrypt_cast5_file.

    Args:
        input_path: Путь к зашифрованному файлу.
        output_path: Путь для сохранения расшифрованного файла.
        key: Ключ расшифрования.
    """
    if not file_exists(input_path):
        raise FileNotFoundError(f"Зашифрованный файл не найден: {input_path}")
    if not key:
        raise ValueError("Ключ не может быть пустым")

    data = load_bytes(input_path)

    iv = data[:CAST.block_size]
    encrypted_data = data[CAST.block_size:]

    if len(iv) != CAST.block_size:
        raise ValueError("Неверный вектор инициализации")

    cipher = CAST.new(key, CAST.MODE_CBC, iv=iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), CAST.block_size)

    save_bytes(decrypted_data, output_path)