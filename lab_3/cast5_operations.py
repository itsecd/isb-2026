import os
from Crypto.Cipher import CAST
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

BLOCK_SIZE = CAST.block_size  # 8 байт (64 бита)


def validate_key_length(length_bits):
    """Проверяет допустимость длины ключа CAST-5 (40-128, кратно 8)."""
    if not isinstance(length_bits, int):
        raise TypeError("Длина ключа должна быть целым числом")
    if length_bits < 40 or length_bits > 128 or length_bits % 8 != 0:
        raise ValueError(f"CAST-5: длина ключа {length_bits} бит не подходит. Нужно 40-128, кратно 8")


def generate_key(length_bits):
    """Генерирует случайный ключ CAST-5 заданной длины."""
    validate_key_length(length_bits)
    key_bytes = length_bits // 8
    return get_random_bytes(key_bytes)


def encrypt_file(input_path, output_path, key):
    """Шифрует файл CAST-5 в режиме CBC с PKCS7 паддингом."""
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Файл для шифрования не найден: {input_path}")
    if not key:
        raise ValueError("Ключ не может быть пустым")
    
    cipher = CAST.new(key, CAST.MODE_CBC)
    iv = cipher.iv
    
    with open(input_path, 'rb') as f:
        plain_data = f.read()
    
    encrypted_data = cipher.encrypt(pad(plain_data, BLOCK_SIZE))
    
    with open(output_path, 'wb') as f:
        f.write(iv + encrypted_data)


def decrypt_file(input_path, output_path, key):
    """Расшифровывает файл, зашифрованный encrypt_file."""
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Зашифрованный файл не найден: {input_path}")
    if not key:
        raise ValueError("Ключ не может быть пустым")
    
    with open(input_path, 'rb') as f:
        iv = f.read(BLOCK_SIZE)
        encrypted_data = f.read()
    
    if len(iv) != BLOCK_SIZE:
        raise ValueError("Неверный вектор инициализации в файле")
    
    cipher = CAST.new(key, CAST.MODE_CBC, iv=iv)
    decrypted_padded = cipher.decrypt(encrypted_data)
    decrypted_data = unpad(decrypted_padded, BLOCK_SIZE)
    
    with open(output_path, 'wb') as f:
        f.write(decrypted_data)