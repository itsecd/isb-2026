from Ru import ALPHABET, ALPHABET_LEN


def generate_caesar_decrypt_key(shift=10):
    """Генерирует словарь для расшифровки шифра Цезаря"""
    decrypt_key = {}

    for i, original_char in enumerate(ALPHABET):
        encrypted_index = (i + shift) % ALPHABET_LEN
        encrypted_char = ALPHABET[encrypted_index]
        decrypt_key[encrypted_char] = original_char

    return decrypt_key

decrypt_key = generate_caesar_decrypt_key(shift=10)
