# crypto/hybrid.py
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
    """Генерация всех ключей для гибридной системы."""
    try:
        match camellia_key_size:
            case 128 | 192 | 256:
                pass
            case _:
                return False, f"Недопустимый размер ключа: {camellia_key_size} бит. Допустимы: 128, 192, 256"
        
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
    """Гибридное шифрование файла."""
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
    """Гибридное расшифрование файла."""
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