import os
import sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


def pad_data(data: bytes, block_size: int = 128) -> bytes:
    """
    Добавляет паддинг ANSIX923 к данным для выравнивания по размеру блока.

    ANSIX923 добивает блок байтами со значением 0x00, а последний байт
    содержит количество добавленных байт паддинга.

    Args:
        data (bytes): исходные данные.
        block_size (int): размер блока в битах. По умолчанию 128.

    Returns:
        bytes: данные с добавленным паддингом.

    Raises:
        Exception: если произошла ошибка при добавлении паддинга.
    """
    try:
        padder = padding.ANSIX923(block_size).padder()
        padded = padder.update(data) + padder.finalize()
        return padded
    except Exception as e:
        print(f"Ошибка при добавлении паддинга: {e}")
        raise


def unpad_data(data: bytes, block_size: int = 128) -> bytes:
    """
    Удаляет паддинг ANSIX923 из данных.

    Args:
        data (bytes): данные с паддингом.
        block_size (int): размер блока в битах. По умолчанию 128.

    Returns:
        bytes: исходные данные без паддинга.

    Raises:
        Exception: если произошла ошибка при удалении паддинга
                   (например, неверный ключ или повреждённые данные).
    """
    try:
        unpadder = padding.ANSIX923(block_size).unpadder()
        unpadded = unpadder.update(data) + unpadder.finalize()
        return unpadded
    except Exception as e:
        print(f"Ошибка при удалении паддинга (возможно, неверный ключ): {e}")
        raise


def encrypt_file(input_path: str, output_path: str, key: bytes) -> None:
    """
    Шифрует содержимое файла алгоритмом AES в режиме CBC.

    Вектор инициализации (IV) генерируется случайно и сохраняется
    в начале выходного файла (первые 16 байт). После IV следует шифротекст.

    Args:
        input_path (str): путь к исходному файлу для шифрования.
        output_path (str): путь для сохранения зашифрованного файла.
        key (bytes): симметричный ключ AES (16, 24 или 32 байта).

    Raises:
        FileNotFoundError: если исходный файл не найден.
        IOError: при ошибках чтения или записи файлов.
        Exception: при ошибках криптографических операций.
    """
    try:
        with open(input_path, 'rb') as f:
            plaintext = f.read()
        print(f"Прочитан файл {input_path} ({len(plaintext)} байт)")
    except FileNotFoundError:
        print(f"Ошибка: файл {input_path} не найден.")
        raise
    except IOError as e:
        print(f"Ошибка при чтении файла {input_path}: {e}")
        raise

    iv = os.urandom(16)
    print("Сгенерирован случайный IV (16 байт)")

    try:
        padded_data = pad_data(plaintext)
        print("Добавлен ANSIX923 паддинг")

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        print("Данные зашифрованы AES")
    except Exception as e:
        print(f"Ошибка при шифровании AES: {e}")
        raise

    try:
        with open(output_path, 'wb') as f:
            f.write(iv + ciphertext)
        print(f"Зашифрованные данные сохранены в {output_path}")
    except IOError as e:
        print(f"Ошибка при сохранении файла {output_path}: {e}")
        raise


def decrypt_file(input_path: str, output_path: str, key: bytes) -> None:
    """
    Расшифровывает содержимое файла, зашифрованного алгоритмом AES в режиме CBC.

    Ожидается, что первые 16 байт файла содержат вектор инициализации (IV),
    а оставшаяся часть — шифротекст.

    Args:
        input_path (str): путь к зашифрованному файлу.
        output_path (str): путь для сохранения расшифрованного файла.
        key (bytes): симметричный ключ AES (16, 24 или 32 байта).

    Raises:
        FileNotFoundError: если зашифрованный файл не найден.
        IOError: при ошибках чтения или записи файлов.
        Exception: при ошибках криптографических операций
                   (например, неверный ключ).
    """
    try:
        with open(input_path, 'rb') as f:
            iv = f.read(16)
            if len(iv) < 16:
                raise ValueError("Файл повреждён: не удалось прочитать IV (менее 16 байт)")
            ciphertext = f.read()
        print(f"Прочитан зашифрованный файл {input_path}")
    except FileNotFoundError:
        print(f"Ошибка: файл {input_path} не найден.")
        raise
    except IOError as e:
        print(f"Ошибка при чтении файла {input_path}: {e}")
        raise
    except ValueError as e:
        print(f"Ошибка формата файла {input_path}: {e}")
        raise

    try:
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        print("Данные расшифрованы AES")

        plaintext = unpad_data(padded_data)
        print("Паддинг удалён")
    except Exception as e:
        print(f"Ошибка при расшифровке AES: {e}")
        raise

    try:
        with open(output_path, 'wb') as f:
            f.write(plaintext)
        print(f"Расшифрованные данные сохранены в {output_path}")
    except IOError as e:
        print(f"Ошибка при сохранении файла {output_path}: {e}")
        raise