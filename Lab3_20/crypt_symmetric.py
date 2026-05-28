"""Модуль симметричной криптографии (Camellia)"""

import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

from file_utils import read_binary_file, write_binary_file


def generate_camellia_key(key_size_bits: int) -> bytes:
    """Генерирует случайный ключ для Camellia.
    
    Args:
        key_size_bits: Размер ключа (128, 192 или 256)
    
    Returns:
        bytes: Ключ указанного размера
    
    Raises:
        ValueError: При недопустимом размере ключа
    """
    match key_size_bits:
        case 128 | 192 | 256:
            key_size_bytes = key_size_bits // 8
            return os.urandom(key_size_bytes)
        case _:
            raise ValueError(f"Недопустимый размер ключа: {key_size_bits} бит. Допустимы: 128, 192, 256")


def encrypt_file_camellia(input_path: str, output_path: str, key: bytes) -> bool:
    """Шифрует файл с помощью Camellia в режиме CBC.
    
    Формат выходного файла: [IV (16 байт)] + [зашифрованные данные]
    
    Args:
        input_path: Путь к исходному файлу
        output_path: Путь для сохранения зашифрованного файла
        key: Ключ Camellia (16, 24 или 32 байта)
    
    Returns:
        bool: True при успешном шифровании
    
    Raises:
        FileNotFoundError: Если исходный файл не найден
        ValueError: При недопустимом размере ключа
        Exception: При других ошибках
    """
    try:
        key_size_bits = len(key) * 8
        match key_size_bits:
            case 128 | 192 | 256:
                pass
            case _:
                raise ValueError(f"Недопустимый размер ключа: {key_size_bits} бит")
        
        plaintext = read_binary_file(input_path)
        
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext) + padder.finalize()
        
        iv = os.urandom(16)
        
        cipher = Cipher(
            algorithms.Camellia(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        
        write_binary_file(output_path, iv + ciphertext)
        
        return True
        
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл для шифрования не найден: {input_path}")
    except Exception as e:
        raise Exception(f"Ошибка при шифровании файла Camellia: {str(e)}")


def decrypt_file_camellia(input_path: str, output_path: str, key: bytes) -> bool:
    """Расшифровывает файл, зашифрованный encrypt_file_camellia().
    
    Args:
        input_path: Путь к зашифрованному файлу
        output_path: Путь для сохранения расшифрованного файла
        key: Ключ Camellia (16, 24 или 32 байта)
    
    Returns:
        bool: True при успешном расшифровании
    
    Raises:
        FileNotFoundError: Если зашифрованный файл не найден
        ValueError: При недопустимом размере ключа или поврежденном файле
        Exception: При других ошибках
    """
    try:
        key_size_bits = len(key) * 8
        match key_size_bits:
            case 128 | 192 | 256:
                pass
            case _:
                raise ValueError(f"Недопустимый размер ключа: {key_size_bits} бит")
        
        data = read_binary_file(input_path)
        
        match len(data):
            case n if n < 16:
                raise ValueError("Файл поврежден: недостаточно данных для IV")
            case _:
                pass
        
        iv = data[:16]
        ciphertext = data[16:]
        
        cipher = Cipher(
            algorithms.Camellia(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        
        write_binary_file(output_path, plaintext)
        
        return True
        
    except FileNotFoundError:
        raise FileNotFoundError(f"Зашифрованный файл не найден: {input_path}")
    except ValueError as e:
        raise ValueError(f"Ошибка при расшифровании: {str(e)}")
    except Exception as e:
        raise Exception(f"Ошибка при расшифровании файла Camellia: {str(e)}")