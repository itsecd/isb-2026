# -*- coding: utf-8 -*-
"""Functions"""

from constants import RU_ALPHABET


def vigenere_encrypt(text: str, key: str) -> str:
    """Vigenere cipher"""
    encrypted_text: list[str] = []
    key_length: int = len(key)
    text = text.upper()
    
    for i in range(len(text)):
        current_char: str = text[i]
        char_index: int = RU_ALPHABET.find(current_char)
         
        if char_index != -1:
            key_char: str = key[i % key_length]
            key_index: int = RU_ALPHABET.find(key_char.upper())

            new_index: int = (char_index + key_index) % len(RU_ALPHABET)
            encrypted_text.append(RU_ALPHABET[new_index])
        else:
            encrypted_text.append(current_char)

    return ''.join(encrypted_text)


def create_key() -> str:
    """Creating encryption key"""
    return "ПЕПС"


def main() -> None:
    with open('original_text.txt', 'r', encoding='utf-8') as f:
        plain_text = f.read()
    
    plain_text = ' '.join(plain_text.split())
    
    key: str = create_key()
    encrypted_text: str = vigenere_encrypt(plain_text, key)
    
    with open('encrypted_text.txt', 'w', encoding='utf-8') as f:
        f.write(encrypted_text)
        
    with open('encryption_key.txt', 'w', encoding='utf-8') as f:
        f.write(key)
