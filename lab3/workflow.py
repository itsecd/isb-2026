import asymmetrical
import symmetrical
import crypto_storage as storage

def run_key_generation(sym_path: str, priv_path: str, pub_path: str, key_bits: int = 128) -> None:
    """
    Генерирует ключи гибридной криптосистемы и сохраняет их в файлы.
    
    Args:
        sym_path (str): Путь для сохранения зашифрованного симметричного ключа.
        priv_path (str): Путь для сохранения приватного RSA ключа.
        pub_path (str): Путь для сохранения публичного RSA-ключа.
        key_bits (int): Длина ключа Blowfish в битах.
        
    Raises:
        Exception: При ошибке генерации или сохранения ключей.
    """
    try:
        session_key = symmetrical.create_blowfish_key(key_bits)
        priv_key, pub_key = asymmetrical.generate_rsa_keys()
        wrapped_key = asymmetrical.encrypt_sym_key(session_key, pub_key)
        storage.save_binary(sym_path, wrapped_key)
        storage.save_private_key(priv_path, priv_key)
        storage.save_public_key(pub_path, pub_key)
        print("Ключевая пара и сессионный ключ сгенерированы и сохранены.")
    except Exception as err:
        raise Exception(f"Ошибка генерации ключей: {err}") from err

def run_encryption(src_path: str, dst_path: str, sym_path: str, priv_path: str) -> None:
    """
    Выполняет гибридное шифрование файла.
    
    Args:
        src_path (str): Путь к исходному файлу.
        dst_path (str): Путь для сохранения зашифрованного файла.
        sym_path (str): Путь к зашифрованному симметричному ключу.
        priv_path (str): Путь к приватному RSA-ключу.
        
    Raises:
        Exception: При ошибке шифрования.
    """
    try:
        priv_key = storage.open_private_key(priv_path)
        wrapped_key = storage.open_binary(sym_path)
        session_key = asymmetrical.decrypt_sym_key(wrapped_key, priv_key)
        plaintext = storage.open_binary(src_path)
        ciphertext = symmetrical.cipher_blowfish_cbc(plaintext, session_key)
        storage.save_binary(dst_path, ciphertext)
        print("Данные успешно зашифрованы гибридной схемой.")
    except Exception as err:
        raise Exception(f"Ошибка шифрования: {err}") from err

def run_decryption(src_path: str, dst_path: str, sym_path: str, priv_path: str) -> None:
    """
    Выполняет гибридное дешифрование файла.
    
    Args:
        src_path (str): Путь к зашифрованному файлу.
        dst_path (str): Путь для сохранения расшифрованного файла.
        sym_path (str): Путь к зашифрованному симметричному ключу.
        priv_path (str): Путь к приватному RSA-ключу.
        
    Raises:
        Exception: При ошибке дешифрования.
    """
    try:
        priv_key = storage.open_private_key(priv_path)
        wrapped_key = storage.open_binary(sym_path)
        session_key = asymmetrical.decrypt_sym_key(wrapped_key, priv_key)
        ciphertext = storage.open_binary(src_path)
        plaintext = symmetrical.decipher_blowfish_cbc(ciphertext, session_key)
        storage.save_binary(dst_path, plaintext)
        print("Данные успешно расшифрованы.")
    except Exception as err:
        raise Exception(f"Ошибка дешифрования: {err}") from err
