'''Модуль гибридной криптосистемы RSA + 3DES.

Объединяет симметричное шифрование (3DES) и асимметричное (RSA):
- Сообщение шифруется алгоритмом 3DES в режиме CBC.
- Ключ 3DES шифруется открытым ключом RSA (OAEP, SHA-256).
'''

import os
import key_utils
import des3_utils
import rsa_utils


def read_file(path: str) -> bytes:
    '''Читает содержимое файла.

    Args:
        path (str): Путь к файлу.

    Returns:
        bytes: Содержимое файла.

    Raises:
        FileNotFoundError: Если файл не найден.
    '''
    try:
        with open(path, "rb") as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {path}")


def write_file(path: str, data: bytes) -> None:
    '''Записывает данные в файл.

    Папка создаётся автоматически, если её не существует.

    Args:
        path (str): Путь к файлу.
        data (bytes): Данные для записи.

    Raises:
        OSError: Если не удалось создать папку или записать файл.
    '''
    try:
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(path, "wb") as f:
            f.write(data)
    except OSError as e:
        raise OSError(f"Ошибка записи файла {path}: {e}")


def generate_all_keys(enc_key_path: str, pub_path: str, priv_path: str, key_size: int) -> None:
    '''Генерирует ключи гибридной системы.

    Создаёт ключ 3DES заданной длины, пару ключей RSA (2048 бит),
    шифрует ключ 3DES открытым ключом RSA и сохраняет все ключи.

    Args:
        enc_key_path (str): Путь для сохранения зашифрованного ключа 3DES.
        pub_path (str): Путь для сохранения открытого ключа RSA.
        priv_path (str): Путь для сохранения закрытого ключа RSA.
        key_size (int): Размер ключа 3DES в битах (64, 128 или 192).

    Raises:
        Exception: Если не удалось сгенерировать или сохранить ключи.
    '''
    try:
        des3_key = key_utils.generate_symmetric_key(key_size)
        private_key, public_key = key_utils.generate_asymmetric_keys()

        key_utils.save_private_key(private_key, priv_path)
        key_utils.save_public_key(public_key, pub_path)

        encrypted_des3_key = rsa_utils.encrypt_key(des3_key, public_key)
        key_utils.save_encrypted_symmetric_key(encrypted_des3_key, enc_key_path)
    except Exception as e:
        raise Exception(f"Ошибка генерации ключей: {e}")


def encrypt_file(input_path: str, pub_key_path: str, enc_key_path: str, output_path: str) -> None:
    '''Шифрует файл гибридной системой.

    Генерирует новый ключ 3DES, шифрует им файл (CBC, паддинг ANSI X.923),
    шифрует ключ 3DES открытым ключом RSA и сохраняет результаты.

    Args:
        input_path (str): Путь к исходному файлу.
        pub_key_path (str): Путь к открытому ключу RSA.
        enc_key_path (str): Путь для сохранения зашифрованного ключа 3DES.
        output_path (str): Путь для сохранения зашифрованного файла.

    Raises:
        FileNotFoundError: Если исходный файл или открытый ключ не найдены.
        Exception: Если не удалось зашифровать файл.
    '''
    try:
        public_key = rsa_utils.load_public_key(pub_key_path)
        des3_key = key_utils.generate_symmetric_key()

        encrypted_des3_key = rsa_utils.encrypt_key(des3_key, public_key)
        key_utils.save_encrypted_symmetric_key(encrypted_des3_key, enc_key_path)

        data = read_file(input_path)
        padded = des3_utils.pad_data(data)
        iv, encrypted = des3_utils.encrypt(padded, des3_key)
        write_file(output_path, iv + encrypted)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Не удалось найти файл: {e}")
    except Exception as e:
        raise Exception(f"Ошибка шифрования файла: {e}")


def decrypt_file(input_path: str, priv_key_path: str, enc_key_path: str, output_path: str) -> None:
    '''Расшифровывает файл гибридной системы.

    Расшифровывает ключ 3DES закрытым ключом RSA,
    затем расшифровывает файл ключом 3DES (CBC) и убирает паддинг.

    Args:
        input_path (str): Путь к зашифрованному файлу.
        priv_key_path (str): Путь к закрытому ключу RSA.
        enc_key_path (str): Путь к зашифрованному ключу 3DES.
        output_path (str): Путь для сохранения расшифрованного файла.

    Raises:
        FileNotFoundError: Если зашифрованный файл или ключи не найдены.
        Exception: Если не удалось расшифровать файл.
    '''
    try:
        private_key = rsa_utils.load_private_key(priv_key_path)
        encrypted_des3_key = read_file(enc_key_path)
        des3_key = rsa_utils.decrypt_key(encrypted_des3_key, private_key)

        data = read_file(input_path)
        iv = data[:8]
        encrypted = data[8:]

        decrypted_padded = des3_utils.decrypt(encrypted, des3_key, iv)
        decrypted = des3_utils.unpad_data(decrypted_padded)
        write_file(output_path, decrypted)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Не удалось найти файл: {e}")
    except Exception as e:
        raise Exception(f"Ошибка расшифрования файла: {e}")