"""Объединяющий модуль для гибридной криптосистемы"""

import os
from typing import Dict, Any, Tuple

from crypt_symmetric import generate_camellia_key, encrypt_file_camellia, decrypt_file_camellia
from crypt_assymmetric import (
    generate_rsa_keys, save_rsa_private_key, save_rsa_public_key,
    load_rsa_private_key, encrypt_with_rsa, decrypt_with_rsa
)
from file_utils import read_binary_file, write_binary_file


def generate_hybrid_keys(settings: Dict[str, Any], camellia_key_size: int) -> Tuple[bool, str]:
    """Генерирует все ключи для гибридной системы.
    
    Создает симметричный ключ Camellia и пару RSA ключей.
    Сохраняет приватный и публичный ключи RSA, а также
    зашифрованный публичным ключом симметричный ключ.
    
    Args:
        settings: Словарь с путями к файлам (private_key, public_key, symmetric_key_encrypted)
        camellia_key_size: Размер ключа Camellia (128, 192 или 256)
    
    Returns:
        Tuple[bool, str]: (успех, сообщение)
    """
    try:
        match camellia_key_size:
            case 128 | 192 | 256:
                pass
            case _:
                return False, f"Недопустимый размер ключа: {camellia_key_size} бит"
        
        sym_key = generate_camellia_key(camellia_key_size)
        private_key, public_key = generate_rsa_keys()
        
        save_rsa_private_key(private_key, settings["private_key"])
        save_rsa_public_key(public_key, settings["public_key"])
        
        encrypted_sym_key = encrypt_with_rsa(sym_key, public_key)
        write_binary_file(settings["symmetric_key_encrypted"], encrypted_sym_key)
        
        return True, f"Ключи успешно сгенерированы (Camellia-{camellia_key_size})"
        
    except Exception as e:
        return False, f"Ошибка генерации ключей: {str(e)}"


def encrypt_hybrid(settings: Dict[str, Any]) -> Tuple[bool, str]:
    """Выполняет гибридное шифрование файла.
    
    Расшифровывает симметричный ключ с помощью приватного RSA ключа,
    затем шифрует исходный файл этим ключом (Camellia-CBC).
    
    Args:
        settings: Словарь с путями (initial_file, encrypted_file, 
                  private_key, symmetric_key_encrypted)
    
    Returns:
        Tuple[bool, str]: (успех, сообщение)
    """
    try:
        match os.path.exists(settings.get("initial_file", "")):
            case False:
                return False, f"Исходный файл не найден: {settings['initial_file']}"
            case _:
                pass
        
        match os.path.exists(settings.get("private_key", "")):
            case False:
                return False, f"Приватный ключ не найден: {settings['private_key']}"
            case _:
                pass
        
        match os.path.exists(settings.get("symmetric_key_encrypted", "")):
            case False:
                return False, f"Зашифрованный симметричный ключ не найден: {settings['symmetric_key_encrypted']}"
            case _:
                pass
        
        private_key = load_rsa_private_key(settings["private_key"])
        encrypted_sym_key = read_binary_file(settings["symmetric_key_encrypted"])
        sym_key = decrypt_with_rsa(encrypted_sym_key, private_key)
        
        encrypt_file_camellia(settings["initial_file"], settings["encrypted_file"], sym_key)
        
        return True, f"Файл успешно зашифрован: {settings['encrypted_file']}"
        
    except Exception as e:
        return False, f"Ошибка шифрования: {str(e)}"


def decrypt_hybrid(settings: Dict[str, Any]) -> Tuple[bool, str]:
    """Выполняет гибридное расшифрование файла.
    
    Расшифровывает симметричный ключ с помощью приватного RSA ключа,
    затем расшифровывает файл этим ключом (Camellia-CBC).
    
    Args:
        settings: Словарь с путями (encrypted_file, decrypted_file,
                  private_key, symmetric_key_encrypted)
    
    Returns:
        Tuple[bool, str]: (успех, сообщение)
    """
    try:
        match os.path.exists(settings.get("encrypted_file", "")):
            case False:
                return False, f"Зашифрованный файл не найден: {settings['encrypted_file']}"
            case _:
                pass
        
        match os.path.exists(settings.get("private_key", "")):
            case False:
                return False, f"Приватный ключ не найден: {settings['private_key']}"
            case _:
                pass
        
        match os.path.exists(settings.get("symmetric_key_encrypted", "")):
            case False:
                return False, f"Зашифрованный симметричный ключ не найден: {settings['symmetric_key_encrypted']}"
            case _:
                pass
        
        private_key = load_rsa_private_key(settings["private_key"])
        encrypted_sym_key = read_binary_file(settings["symmetric_key_encrypted"])
        sym_key = decrypt_with_rsa(encrypted_sym_key, private_key)
        
        decrypt_file_camellia(settings["encrypted_file"], settings["decrypted_file"], sym_key)
        
        return True, f"Файл успешно расшифрован: {settings['decrypted_file']}"
        
    except Exception as e:
        return False, f"Ошибка расшифрования: {str(e)}"